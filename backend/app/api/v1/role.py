from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.schemas.role import Role, RoleCreate, RoleUpdate, RoleWithPermissions, RoleWithMenus
from app.services.role_service import RoleService
from app.middlewares.auth import get_current_active_user
from app.models.user import User as UserModel


router = APIRouter(prefix="", tags=["role"])


@router.get("/roles", response_model=List[Role], description="获取角色列表")
def get_roles(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_active_user)):
    """获取角色列表"""
    # 检查用户是否有获取角色列表的权限
    has_permission = any("roles:get_roles" in [p.code for p in role.permissions] for role in current_user.roles)
    is_admin = any(role.name == "admin" for role in current_user.roles)
    
    if not has_permission and not is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Permission denied"
        )
    
    # 如果不是管理员，只返回自己的角色
    user_id = None if is_admin else current_user.id
    roles = RoleService.get_roles(db, skip=skip, limit=limit, user_id=user_id)
    return roles


@router.post("/roles", response_model=Role, status_code=status.HTTP_201_CREATED, description="创建角色")
def create_role(role: RoleCreate, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_active_user)):
    """创建角色"""
    # 检查用户是否有创建角色的权限
    has_permission = any("roles:create_role" in [p.code for p in role.permissions] for role in current_user.roles)
    is_admin = any(role.name == "admin" for role in current_user.roles)
    
    if not has_permission and not is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Permission denied"
        )
    
    return RoleService.create_role(db=db, role_create=role)


@router.get("/roles/{role_id}", response_model=Role, description="获取角色详情")
def get_role(role_id: int, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_active_user)):
    """获取角色详情"""
    # 检查用户是否有获取角色详情的权限
    has_permission = any("roles:get_role" in [p.code for p in role.permissions] for role in current_user.roles)
    is_admin = any(role.name == "admin" for role in current_user.roles)
    
    # 检查用户是否拥有该角色
    has_role = any(role.id == role_id for role in current_user.roles)
    
    if not has_permission and not is_admin and not has_role:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Permission denied"
        )
    
    db_role = RoleService.get_role_by_id(db, role_id=role_id)
    if db_role is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Role not found"
        )
    return db_role


@router.put("/roles/{role_id}", response_model=Role, description="修改角色信息")
def update_role(role_id: int, role: RoleUpdate, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_active_user)):
    """修改角色信息"""
    # 检查用户是否有更新角色的权限
    has_permission = any("roles:update_role" in [p.code for p in role.permissions] for role in current_user.roles)
    is_admin = any(role.name == "admin" for role in current_user.roles)
    
    if not has_permission and not is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Permission denied"
        )
    
    db_role = RoleService.update_role(db=db, role_id=role_id, role_update=role)
    if db_role is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Role not found"
        )
    return db_role


@router.delete("/roles/{role_id}", status_code=status.HTTP_204_NO_CONTENT, description="删除角色")
def delete_role(role_id: int, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_active_user)):
    """删除角色"""
    # 检查用户是否有删除角色的权限
    has_permission = any("roles:delete_role" in [p.code for p in role.permissions] for role in current_user.roles)
    is_admin = any(role.name == "admin" for role in current_user.roles)
    
    if not has_permission and not is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Permission denied"
        )
    
    success = RoleService.delete_role(db=db, role_id=role_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Role not found"
        )
    return None


@router.get("/roles/{role_id}/permissions", response_model=RoleWithPermissions, description="获取角色权限")
def get_role_permissions(role_id: int, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_active_user)):
    """获取角色权限"""
    # 检查用户是否有获取角色权限的权限
    has_permission = any("roles:get_role_permissions" in [p.code for p in role.permissions] for role in current_user.roles)
    is_admin = any(role.name == "admin" for role in current_user.roles)
    
    # 检查用户是否拥有该角色
    has_role = any(role.id == role_id for role in current_user.roles)
    
    if not has_permission and not is_admin and not has_role:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Permission denied"
        )
    
    db_role = RoleService.get_role_by_id(db, role_id=role_id)
    if db_role is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Role not found"
        )
    permissions = RoleService.get_role_permissions(db=db, role_id=role_id)
    role_with_permissions = RoleWithPermissions.model_validate(db_role)
    role_with_permissions.permissions = permissions
    return role_with_permissions


@router.post("/roles/{role_id}/permissions", description="分配角色权限")
def assign_role_permissions(role_id: int, permission_ids: List[int], db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_active_user)):
    """分配角色权限"""
    # 检查用户是否有分配角色权限的权限
    has_permission = any("roles:assign_role_permissions" in [p.code for p in role.permissions] for role in current_user.roles)
    is_admin = any(role.name == "admin" for role in current_user.roles)
    
    if not has_permission and not is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Permission denied"
        )
    
    db_role = RoleService.assign_role_permissions(db=db, role_id=role_id, permission_ids=permission_ids)
    if db_role is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Role not found"
        )
    return {"message": "Permissions assigned successfully"}


@router.get("/roles/{role_id}/menus", response_model=RoleWithMenus, description="获取角色菜单")
def get_role_menus(role_id: int, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_active_user)):
    """获取角色菜单"""
    # 检查用户是否有获取角色菜单的权限
    has_permission = any("roles:get_role_menus" in [p.code for p in role.permissions] for role in current_user.roles)
    is_admin = any(role.name == "admin" for role in current_user.roles)
    
    # 检查用户是否拥有该角色
    has_role = any(role.id == role_id for role in current_user.roles)
    
    if not has_permission and not is_admin and not has_role:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Permission denied"
        )
    
    db_role = RoleService.get_role_by_id(db, role_id=role_id)
    if db_role is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Role not found"
        )
    menus = RoleService.get_role_menus(db=db, role_id=role_id)
    role_with_menus = RoleWithMenus.model_validate(db_role)
    role_with_menus.menus = menus
    return role_with_menus


@router.post("/roles/{role_id}/menus", description="分配角色菜单")
def assign_role_menus(role_id: int, menu_ids: List[int], db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_active_user)):
    """分配角色菜单"""
    # 检查用户是否有分配角色菜单的权限
    has_permission = any("roles:assign_role_menus" in [p.code for p in role.permissions] for role in current_user.roles)
    is_admin = any(role.name == "admin" for role in current_user.roles)
    
    if not has_permission and not is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Permission denied"
        )
    
    db_role = RoleService.assign_role_menus(db=db, role_id=role_id, menu_ids=menu_ids)
    if db_role is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Role not found"
        )
    return {"message": "Menus assigned successfully"}
