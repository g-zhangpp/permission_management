from sqlalchemy.orm import Session
from app.core.config import settings
from app.models.user import User
from app.models.role import Role
from app.models.permission import Permission
from app.models.menu import Menu
from app.core.security import get_password_hash


def init_data(db: Session):
    """初始化数据"""
    # 1. 初始化角色
    roles_data = settings.init_data.get("roles", [])
    role_map = {}
    for role_data in roles_data:
        role = db.query(Role).filter(Role.name == role_data["name"]).first()
        if not role:
            role = Role(
                name=role_data["name"],
                description=role_data["description"]
            )
            db.add(role)
        role_map[role_data["name"]] = role
    db.commit()
    
    # 2. 初始化权限
    permissions_data = settings.init_data.get("permissions", [])
    permission_map = {}
    for permission_data in permissions_data:
        permission = db.query(Permission).filter(Permission.code == permission_data["code"]).first()
        if not permission:
            permission = Permission(
                name=permission_data["name"],
                code=permission_data["code"],
                description=permission_data["description"]
            )
            db.add(permission)
        permission_map[permission_data["code"]] = permission
    db.commit()
    
    # 3. 初始化菜单
    menus_data = settings.init_data.get("menus", [])
    menu_map = {}
    for i, menu_data in enumerate(menus_data):
        menu = db.query(Menu).filter(Menu.path == menu_data["path"]).first()
        if not menu:
            menu = Menu(
                name=menu_data["name"],
                path=menu_data["path"],
                component=menu_data["component"],
                icon=menu_data["icon"],
                parent_id=menu_data["parent_id"],
                order=menu_data["order"]
            )
            db.add(menu)
        menu_map[i + 1] = menu  # 使用索引作为临时ID
    db.commit()
    
    # 4. 为admin角色分配所有权限和菜单
    admin_role = role_map.get("admin")
    if admin_role:
        # 分配所有权限
        admin_role.permissions = list(permission_map.values())
        # 分配所有菜单
        admin_role.menus = list(menu_map.values())
        db.commit()
    
    # 5. 初始化用户
    users_data = settings.init_data.get("users", [])
    for user_data in users_data:
        user = db.query(User).filter(User.username == user_data["username"]).first()
        if not user:
            user = User(
                username=user_data["username"],
                email=user_data["email"],
                password_hash=get_password_hash(user_data["password"])
            )
            # 分配角色
            user_roles = []
            for role_name in user_data.get("roles", []):
                if role_name in role_map:
                    user_roles.append(role_map[role_name])
            user.roles = user_roles
            db.add(user)
    db.commit()
