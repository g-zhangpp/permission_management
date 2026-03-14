from fastapi import FastAPI
from sqlalchemy.orm import Session
from app.models.permission import Permission as PermissionModel
from app.models.role import Role as RoleModel
from app.core.database import get_db
from app.core.logger import logger


# def generate_permission_code(method: str, path: str) -> str:
#     """根据HTTP方法和路径生成权限代码"""
#     # 处理路径参数
#     path = path.replace("{id}", ":id")
    
#     # 特殊路由映射
#     special_routes = {
#         "/auth/login": "auth:login",
#         "/auth/logout": "auth:logout",
#         "/auth/refresh": "auth:refresh",
#         "/auth/me": "auth:me",
#     }
    
#     if path in special_routes:
#         return special_routes[path]
    
#     # 提取资源和操作
#     parts = path.strip('/').split('/')
#     if not parts or parts[0] == '':
#         return "unknown:access"
    
#     resource = parts[0]
#     action = method.lower()
    
#     # 处理子资源
#     if len(parts) > 1:
#         if parts[1] == ":id" and len(parts) > 2:
#             # 如 /users/:id/roles
#             sub_resource = parts[2]
#             return f"{resource}:{sub_resource}:{action}"
#         elif parts[1] != ":id":
#             # 如 /users/list
#             return f"{resource}:{parts[1]}:{action}"
    
#     # 标准资源操作
#     if action == "get":
#         if ":id" in path:
#             return f"{resource}:read"
#         else:
#             return f"{resource}:list"
#     elif action == "post":
#         if ":id" in path:
#             return f"{resource}:update"
#         else:
#             return f"{resource}:create"
#     elif action == "put":
#         return f"{resource}:update"
#     elif action == "delete":
#         return f"{resource}:delete"
#     else:
#         return f"{resource}:{action}"


# def get_permission_name(permission_code: str) -> str:
#     """根据权限代码生成权限名称"""
#     parts = permission_code.split(':')
#     if len(parts) == 2:
#         resource, action = parts
#         action_map = {
#             "list": "获取列表",
#             "create": "创建",
#             "read": "获取详情",
#             "update": "更新",
#             "delete": "删除",
#             "login": "登录",
#             "logout": "登出",
#             "refresh": "刷新令牌",
#             "me": "获取当前用户信息"
#         }
#         resource_map = {
#             "auth": "认证",
#             "user": "用户",
#             "role": "角色",
#             "permission": "权限",
#             "menu": "菜单"
#         }
#         resource_name = resource_map.get(resource, resource)
#         action_name = action_map.get(action, action)
#         return f"{resource_name}{action_name}"
#     elif len(parts) == 3:
#         resource, sub_resource, action = parts
#         resource_map = {
#             "auth": "认证",
#             "user": "用户",
#             "role": "角色",
#             "permission": "权限",
#             "menu": "菜单"
#         }
#         action_map = {
#             "list": "获取列表",
#             "create": "创建",
#             "read": "获取详情",
#             "update": "更新",
#             "delete": "删除",
#             "assign": "分配"
#         }
#         resource_name = resource_map.get(resource, resource)
#         sub_resource_name = sub_resource_map.get(sub_resource, sub_resource)
#         action_name = action_map.get(action, action)
#         return f"{resource_name}{sub_resource_name}{action_name}"
#     else:
#         return permission_code

# 子资源名称映射
# sub_resource_map = {
#     "roles": "角色",
#     "permissions": "权限",
#     "menus": "菜单"
# }


def scan_routes(app: FastAPI) -> list:
    """扫描所有路由，生成权限列表"""
    permissions = []
    special_routes = ["/api/auth/login", "/api/auth/logout", "/api/auth/refresh", "/api/auth/me"]
    
    for route in app.routes:
        if hasattr(route, "path") and hasattr(route, "methods") and hasattr(route, "endpoint"):
            path = route.path
            # 跳过非API路由（如静态文件、文档等）、特殊路由所有角色的用户都有权限
            if path.startswith("/api") and path not in special_routes:
                # 移除/api前缀
                api_path = path[4:]
                # 获取路由函数名
                function_name = route.endpoint.__name__
                # 获取路由装饰器中的description参数
                description = getattr(route, "description", None) or ""
                # 如果没有description，则使用路由函数的文档字符串
                if not description and hasattr(route.endpoint, "__doc__"):
                    description = route.endpoint.__doc__ or ""
                
                # 提取资源名（从路径中提取）
                parts = api_path.strip('/').split('/')
                resource = parts[0] if parts and parts[0] else "unknown"
                
                for method in route.methods:
                    if method != "OPTIONS":  # 跳过OPTIONS方法
                        # 生成权限代码：资源:路由函数名
                        permission_code = f"{resource}:{function_name}"
                        # 生成权限名称（优先使用description）
                        permission_name = description.strip() or f"{resource} {function_name}"
                        permissions.append({
                            "code": permission_code,
                            "name": permission_name,
                            "description": permission_name
                        })
    
    # 去重
    unique_permissions = []
    seen_codes = set()
    for perm in permissions:
        if perm["code"] not in seen_codes:
            seen_codes.add(perm["code"])
            unique_permissions.append(perm)
    
    return unique_permissions


def sync_permissions(app: FastAPI, db: Session) -> int:
    """同步权限到数据库"""
    # 扫描路由生成权限
    permissions = scan_routes(app)
    
    logger.info(f"扫描到 {len(permissions)} 个权限")
    for perm in permissions:
        logger.debug(f"权限: {perm['code']} - {perm['name']} - {perm['description']}")
    
    # 同步到数据库
    created_count = 0
    for perm_data in permissions:
        # 检查权限是否已存在
        existing_perm = db.query(PermissionModel).filter(
            PermissionModel.code == perm_data["code"]
        ).first()
        
        if not existing_perm:
            # 创建新权限
            new_perm = PermissionModel(
                name=perm_data["name"],
                code=perm_data["code"],
                description=perm_data["description"]
            )
            db.add(new_perm)
            created_count += 1
            logger.info(f"创建新权限: {perm_data['code']}")
    
    db.commit()
    logger.info(f"权限同步完成，创建了 {created_count} 个新权限")
    
    # 将所有权限与admin角色绑定
    logger.info("开始绑定权限到admin角色")
    # 查找或创建admin角色
    admin_role = db.query(RoleModel).filter(RoleModel.name == "admin").first()
    if not admin_role:
        # 创建admin角色
        admin_role = RoleModel(
            name="admin",
            description="管理员角色，拥有所有权限"
        )
        db.add(admin_role)
        db.commit()
        logger.info("创建了admin角色")
    
    # 获取所有权限
    all_permissions = db.query(PermissionModel).all()
    
    # 清除admin角色的现有权限
    admin_role.permissions.clear()
    
    # 为admin角色添加所有权限
    for perm in all_permissions:
        admin_role.permissions.append(perm)
    
    db.commit()
    logger.info(f"成功将 {len(all_permissions)} 个权限绑定到admin角色")
    
    return created_count
