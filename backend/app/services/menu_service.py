from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.menu import Menu
from app.schemas.menu import MenuCreate, MenuUpdate, MenuWithChildren


class MenuService:
    """菜单服务"""
    
    @staticmethod
    def get_menus(db: Session, skip: int = 0, limit: int = 100) -> List[Menu]:
        """获取菜单列表"""
        return db.query(Menu).offset(skip).limit(limit).all()
    
    @staticmethod
    def get_menu_by_id(db: Session, menu_id: int) -> Optional[Menu]:
        """根据ID获取菜单"""
        return db.query(Menu).filter(Menu.id == menu_id).first()
    
    @staticmethod
    def create_menu(db: Session, menu_create: MenuCreate) -> Menu:
        """创建菜单"""
        db_menu = Menu(
            name=menu_create.name,
            path=menu_create.path,
            component=menu_create.component,
            icon=menu_create.icon,
            parent_id=menu_create.parent_id,
            order=menu_create.order
        )
        db.add(db_menu)
        db.commit()
        db.refresh(db_menu)
        return db_menu
    
    @staticmethod
    def update_menu(db: Session, menu_id: int, menu_update: MenuUpdate) -> Optional[Menu]:
        """更新菜单"""
        db_menu = db.query(Menu).filter(Menu.id == menu_id).first()
        if not db_menu:
            return None
        
        update_data = menu_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_menu, field, value)
        
        db.commit()
        db.refresh(db_menu)
        return db_menu
    
    @staticmethod
    def delete_menu(db: Session, menu_id: int) -> bool:
        """删除菜单"""
        db_menu = db.query(Menu).filter(Menu.id == menu_id).first()
        if not db_menu:
            return False
        
        db.delete(db_menu)
        db.commit()
        return True
    
    @staticmethod
    def get_menu_tree(db: Session, user_id: Optional[int] = None) -> List[MenuWithChildren]:
        """获取菜单树"""
        user_permissions = set()
        if user_id:
            # 根据用户ID获取用户的菜单和权限
            from app.models.user import User
            user = db.query(User).filter(User.id == user_id).first()
            if user:
                # 获取用户所有角色的菜单和权限
                user_menu_ids = set()
                for role in user.roles:
                    for menu in role.menus:
                        user_menu_ids.add(menu.id)
                    for permission in role.permissions:
                        user_permissions.add(permission.code)
                
                # 获取用户有权限的菜单
                all_menus = db.query(Menu).filter(Menu.id.in_(user_menu_ids)).order_by(Menu.order).all()
            else:
                all_menus = []
        else:
            # 获取所有菜单
            all_menus = db.query(Menu).order_by(Menu.order).all()
        
        # 构建菜单字典
        menu_dict = {menu.id: MenuWithChildren.model_validate(menu) for menu in all_menus}
        
        # 为每个菜单添加权限信息
        for menu in all_menus:
            menu_obj = menu_dict[menu.id]
            # 根据菜单路径判断所属模块，添加对应的权限
            if '/user/list' in menu.path:
                # 用户管理模块权限
                menu_obj.permissions = [p for p in user_permissions if p.startswith('users:')]
            elif '/user/role' in menu.path:
                # 角色管理模块权限
                menu_obj.permissions = [p for p in user_permissions if p.startswith('roles:')]
            elif '/user/permission' in menu.path:
                # 权限管理模块权限
                menu_obj.permissions = [p for p in user_permissions if p.startswith('permissions:')]
            elif '/user/menu' in menu.path:
                # 菜单管理模块权限
                menu_obj.permissions = [p for p in user_permissions if p.startswith('menus:')]
            else:
                # 其他模块权限
                menu_obj.permissions = []
        
        # 构建菜单树，确保只有父菜单存在时，子菜单才会显示
        menu_tree = []
        for menu in all_menus:
            if menu.parent_id is None:
                # 根菜单
                menu_tree.append(menu_dict[menu.id])
            else:
                # 子菜单，只有当父菜单在用户菜单中时才添加
                if menu.parent_id in menu_dict:
                    # 确保子菜单本身也在用户权限列表中
                    menu_dict[menu.parent_id].children.append(menu_dict[menu.id])
        
        # 过滤掉没有子菜单的父菜单（可选）
        # menu_tree = [menu for menu in menu_tree if menu.children or menu.path]
        
        return menu_tree
