from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class MenuBase(BaseModel):
    """菜单基础模型"""
    name: str
    path: str
    component: str
    icon: Optional[str] = None
    parent_id: Optional[int] = None
    order: Optional[int] = 0


class MenuCreate(MenuBase):
    """创建菜单模型"""
    pass


class MenuUpdate(BaseModel):
    """更新菜单模型"""
    name: Optional[str] = None
    path: Optional[str] = None
    component: Optional[str] = None
    icon: Optional[str] = None
    parent_id: Optional[int] = None
    order: Optional[int] = None


class MenuInDB(MenuBase):
    """数据库中的菜单模型"""
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class Menu(MenuInDB):
    """菜单响应模型"""
    pass


class MenuWithChildren(Menu):
    """带子菜单的菜单模型"""
    children: List["MenuWithChildren"] = []
    permissions: List[str] = []


MenuWithChildren.model_rebuild()
