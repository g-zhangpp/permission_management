from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import BaseModel


class Menu(BaseModel):
    """菜单模型"""
    __tablename__ = "menus"

    name = Column(String(50), nullable=False)
    path = Column(String(100), nullable=False)
    component = Column(String(100), nullable=False)
    icon = Column(String(50), nullable=True)
    parent_id = Column(Integer, ForeignKey("menus.id"), nullable=True)
    order = Column(Integer, nullable=True, default=0)

    # 关联关系
    roles = relationship("Role", secondary="role_menus", back_populates="menus")
