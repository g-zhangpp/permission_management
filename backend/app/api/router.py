from fastapi import APIRouter
from app.api.v1 import auth, user, role, permission, menu


api_router = APIRouter(prefix="/api")

# 注册认证路由
api_router.include_router(auth.router)

# 注册用户路由
api_router.include_router(user.router)

# 注册角色路由
api_router.include_router(role.router)

# 注册权限路由
api_router.include_router(permission.router)

# 注册菜单路由
api_router.include_router(menu.router)