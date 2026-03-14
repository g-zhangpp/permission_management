from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class PermissionBase(BaseModel):
    """权限基础模型"""
    name: str
    code: str
    description: Optional[str] = None


class PermissionCreate(PermissionBase):
    """创建权限模型"""
    pass


class PermissionUpdate(BaseModel):
    """更新权限模型"""
    name: Optional[str] = None
    code: Optional[str] = None
    description: Optional[str] = None


class PermissionInDB(PermissionBase):
    """数据库中的权限模型"""
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class Permission(PermissionInDB):
    """权限响应模型"""
    pass
