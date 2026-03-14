from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from app.models.base import BaseModel


class Permission(BaseModel):
    """权限模型"""
    __tablename__ = "permissions"

    name = Column(String(50), unique=True, index=True, nullable=False)
    code = Column(String(50), unique=True, index=True, nullable=False)
    description = Column(String(200), nullable=True)

    # 关联关系
    roles = relationship("Role", secondary="role_permissions", back_populates="permissions")
