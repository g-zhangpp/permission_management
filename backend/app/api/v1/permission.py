from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.schemas.permission import Permission, PermissionCreate, PermissionUpdate
from app.services.permission_service import PermissionService
from app.middlewares.auth import get_current_active_user
from app.models.user import User as UserModel


router = APIRouter(prefix="", tags=["permission"])


@router.get("/permissions", response_model=List[Permission], description="获取权限列表")
def get_permissions(skip: int = 0, limit: int = 10000, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_active_user)):
    """获取权限列表"""
    # 检查用户是否有获取权限列表的权限
    has_permission = any("permissions:get_permissions" in [p.code for p in role.permissions] for role in current_user.roles)
    is_admin = any(role.name == "admin" for role in current_user.roles)
    
    if not has_permission and not is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Permission denied"
        )
    
    # 如果不是管理员，只返回自己的权限
    user_id = None if is_admin else current_user.id
    permissions = PermissionService.get_permissions(db, skip=skip, limit=limit, user_id=user_id)
    return permissions


@router.post("/permissions", response_model=Permission, status_code=status.HTTP_201_CREATED, description="创建权限")
def create_permission(permission: PermissionCreate, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_active_user)):
    """创建权限"""
    # 检查用户是否有创建权限的权限
    has_permission = any("permissions:create_permission" in [p.code for p in role.permissions] for role in current_user.roles)
    is_admin = any(role.name == "admin" for role in current_user.roles)
    
    if not has_permission and not is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Permission denied"
        )
    
    return PermissionService.create_permission(db=db, permission_create=permission)


@router.get("/permissions/{permission_id}", response_model=Permission, description="获取权限详情")
def get_permission(permission_id: int, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_active_user)):
    """获取权限详情"""
    # 检查用户是否有获取权限详情的权限
    has_permission = any("permissions:get_permission" in [p.code for p in role.permissions] for role in current_user.roles)
    is_admin = any(role.name == "admin" for role in current_user.roles)
    
    # 检查用户是否拥有该权限
    has_permission_access = any(permission.id == permission_id for role in current_user.roles for permission in role.permissions)
    
    if not has_permission and not is_admin and not has_permission_access:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Permission denied"
        )
    
    db_permission = PermissionService.get_permission_by_id(db, permission_id=permission_id)
    if db_permission is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Permission not found"
        )
    return db_permission


@router.put("/permissions/{permission_id}", response_model=Permission, description="修改权限信息")
def update_permission(permission_id: int, permission: PermissionUpdate, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_active_user)):
    """修改权限信息"""
    # 检查用户是否有更新权限的权限
    has_permission = any("permissions:update_permission" in [p.code for p in role.permissions] for role in current_user.roles)
    is_admin = any(role.name == "admin" for role in current_user.roles)
    
    if not has_permission and not is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Permission denied"
        )
    
    db_permission = PermissionService.update_permission(db=db, permission_id=permission_id, permission_update=permission)
    if db_permission is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Permission not found"
        )
    return db_permission


@router.delete("/permissions/{permission_id}", status_code=status.HTTP_204_NO_CONTENT, description="删除权限")
def delete_permission(permission_id: int, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_active_user)):
    """删除权限"""
    # 检查用户是否有删除权限的权限
    has_permission = any("permissions:delete_permission" in [p.code for p in role.permissions] for role in current_user.roles)
    is_admin = any(role.name == "admin" for role in current_user.roles)
    
    if not has_permission and not is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Permission denied"
        )
    
    success = PermissionService.delete_permission(db=db, permission_id=permission_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Permission not found"
        )
    return None
