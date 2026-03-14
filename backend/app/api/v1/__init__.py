from fastapi import APIRouter
from .auth import router as auth_router
from .user import router as user_router
from .role import router as role_router
from .permission import router as permission_router
from .menu import router as menu_router

router = APIRouter()

router.include_router(auth_router)
router.include_router(user_router)
router.include_router(role_router)
router.include_router(permission_router)
router.include_router(menu_router)
