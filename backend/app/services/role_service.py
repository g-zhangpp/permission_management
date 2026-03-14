from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.role import Role
from app.models.permission import Permission
from app.models.menu import Menu
from app.schemas.role import RoleCreate, RoleUpdate


class RoleService:
    """角色服务"""
    
    @staticmethod
    def get_roles(db: Session, skip: int = 0, limit: int = 100, user_id: Optional[int] = None) -> List[Role]:
        """获取角色列表"""
        query = db.query(Role)
        # 如果指定了user_id，只返回该用户拥有的角色
        if user_id:
            from app.models.user import User
            user = db.query(User).filter(User.id == user_id).first()
            if user:
                query = query.filter(Role.id.in_([role.id for role in user.roles]))
            else:
                return []
        return query.offset(skip).limit(limit).all()
    
    @staticmethod
    def get_role_by_id(db: Session, role_id: int) -> Optional[Role]:
        """根据ID获取角色"""
        return db.query(Role).filter(Role.id == role_id).first()
    
    @staticmethod
    def create_role(db: Session, role_create: RoleCreate) -> Role:
        """创建角色"""
        db_role = Role(
            name=role_create.name,
            description=role_create.description
        )
        db.add(db_role)
        db.commit()
        db.refresh(db_role)
        return db_role
    
    @staticmethod
    def update_role(db: Session, role_id: int, role_update: RoleUpdate) -> Optional[Role]:
        """更新角色"""
        db_role = db.query(Role).filter(Role.id == role_id).first()
        if not db_role:
            return None
        
        update_data = role_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_role, field, value)
        
        db.commit()
        db.refresh(db_role)
        return db_role
    
    @staticmethod
    def delete_role(db: Session, role_id: int) -> bool:
        """删除角色"""
        db_role = db.query(Role).filter(Role.id == role_id).first()
        if not db_role:
            return False
        
        db.delete(db_role)
        db.commit()
        return True
    
    @staticmethod
    def get_role_permissions(db: Session, role_id: int) -> List[Permission]:
        """获取角色权限"""
        role = db.query(Role).filter(Role.id == role_id).first()
        if not role:
            return []
        return role.permissions
    
    @staticmethod
    def assign_role_permissions(db: Session, role_id: int, permission_ids: List[int]) -> Optional[Role]:
        """分配角色权限"""
        role = db.query(Role).filter(Role.id == role_id).first()
        if not role:
            return None
        
        permissions = db.query(Permission).filter(Permission.id.in_(permission_ids)).all()
        role.permissions = permissions
        
        db.commit()
        db.refresh(role)
        return role
    
    @staticmethod
    def get_role_menus(db: Session, role_id: int) -> List[Menu]:
        """获取角色菜单"""
        role = db.query(Role).filter(Role.id == role_id).first()
        if not role:
            return []
        return role.menus
    
    @staticmethod
    def assign_role_menus(db: Session, role_id: int, menu_ids: List[int]) -> Optional[Role]:
        """分配角色菜单"""
        role = db.query(Role).filter(Role.id == role_id).first()
        if not role:
            return None
        
        menus = db.query(Menu).filter(Menu.id.in_(menu_ids)).all()
        role.menus = menus
        
        db.commit()
        db.refresh(role)
        return role
