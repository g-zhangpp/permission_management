from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class RoleBase(BaseModel):
    """角色基础模型"""
    name: str
    description: Optional[str] = None


class RoleCreate(RoleBase):
    """创建角色模型"""
    pass


class RoleUpdate(BaseModel):
    """更新角色模型"""
    name: Optional[str] = None
    description: Optional[str] = None


class RoleInDB(RoleBase):
    """数据库中的角色模型"""
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class Role(RoleInDB):
    """角色响应模型"""
    pass


class RoleWithPermissions(Role):
    """带权限的角色模型"""
    permissions: List["Permission"] = []


class RoleWithMenus(Role):
    """带菜单的角色模型"""
    menus: List["Menu"] = []


from app.schemas.permission import Permission
from app.schemas.menu import Menu
RoleWithPermissions.model_rebuild()
RoleWithMenus.model_rebuild()
