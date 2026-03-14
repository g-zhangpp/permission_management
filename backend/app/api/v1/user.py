from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.schemas.user import User, UserCreate, UserUpdate, UserWithRoles
from app.services.user_service import UserService
from app.middlewares.auth import get_current_active_user
from app.models.user import User as UserModel


router = APIRouter(prefix="", tags=["user"])


@router.get("/users", response_model=List[User], description="获取用户列表")
def get_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_active_user)):
    """获取用户列表"""
    # 检查用户是否有获取用户列表的权限
    has_permission = any("users:get_users" in [p.code for p in role.permissions] for role in current_user.roles)
    is_admin = any(role.name == "admin" for role in current_user.roles)
    
    if not has_permission and not is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Permission denied"
        )
    
    # 如果不是管理员，只返回自己的数据
    user_id = None if is_admin else current_user.id
    users = UserService.get_users(db, skip=skip, limit=limit, user_id=user_id)
    return users


@router.post("/users", response_model=User, status_code=status.HTTP_201_CREATED, description="创建用户")
def create_user(user: UserCreate, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_active_user)):
    """创建用户"""
    # 检查用户是否有创建用户的权限
    has_permission = any("users:create_user" in [p.code for p in role.permissions] for role in current_user.roles)
    is_admin = any(role.name == "admin" for role in current_user.roles)
    
    if not has_permission and not is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Permission denied"
        )
    
    db_user = UserService.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    return UserService.create_user(db=db, user_create=user)


@router.get("/users/{user_id}", response_model=User, description="获取用户详情")
def get_user(user_id: int, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_active_user)):
    """获取用户详情"""
    # 检查用户是否有获取用户详情的权限
    has_permission = any("users:get_user" in [p.code for p in role.permissions] for role in current_user.roles)
    is_admin = any(role.name == "admin" for role in current_user.roles)
    
    if not has_permission and not is_admin and current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Permission denied"
        )
    
    db_user = UserService.get_user_by_id(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return db_user


@router.put("/users/{user_id}", response_model=User, description="修改用户信息")
def update_user(user_id: int, user: UserUpdate, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_active_user)):
    """修改用户信息"""
    # 检查用户是否有更新用户的权限
    has_permission = any("users:update_user" in [p.code for p in role.permissions] for role in current_user.roles)
    is_admin = any(role.name == "admin" for role in current_user.roles)
    
    if not has_permission and not is_admin and current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Permission denied"
        )
    
    db_user = UserService.update_user(db=db, user_id=user_id, user_update=user)
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return db_user


@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT, description="删除用户")
def delete_user(user_id: int, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_active_user)):
    """删除用户"""
    # 检查用户是否有删除用户的权限
    has_permission = any("users:delete_user" in [p.code for p in role.permissions] for role in current_user.roles)
    is_admin = any(role.name == "admin" for role in current_user.roles)
    
    if not has_permission and not is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Permission denied"
        )
    
    success = UserService.delete_user(db=db, user_id=user_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return None


@router.get("/users/{user_id}/roles", response_model=List[UserWithRoles], description="获取用户角色")
def get_user_roles(user_id: int, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_active_user)):
    """获取用户角色"""
    # 检查用户是否有获取用户角色的权限
    has_permission = any("users:get_user_roles" in [p.code for p in role.permissions] for role in current_user.roles)
    is_admin = any(role.name == "admin" for role in current_user.roles)
    
    if not has_permission and not is_admin and current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Permission denied"
        )
    
    db_user = UserService.get_user_by_id(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    roles = UserService.get_user_roles(db=db, user_id=user_id)
    user_with_roles = UserWithRoles.model_validate(db_user)
    user_with_roles.roles = roles
    return [user_with_roles]


@router.post("/users/{user_id}/roles", description="分配用户角色")
def assign_user_roles(user_id: int, role_ids: List[int], db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_active_user)):
    """分配用户角色"""
    # 检查用户是否有分配用户角色的权限
    has_permission = any("users:assign_user_roles" in [p.code for p in role.permissions] for role in current_user.roles)
    is_admin = any(role.name == "admin" for role in current_user.roles)
    
    if not has_permission and not is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Permission denied"
        )
    
    db_user = UserService.assign_user_roles(db=db, user_id=user_id, role_ids=role_ids)
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return {"message": "Roles assigned successfully"}
