from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.permission import Permission
from app.schemas.permission import PermissionCreate, PermissionUpdate


class PermissionService:
    """权限服务"""
    
    @staticmethod
    def get_permissions(db: Session, skip: int = 0, limit: int = 100, user_id: Optional[int] = None) -> List[Permission]:
        """获取权限列表"""
        query = db.query(Permission)
        # 如果指定了user_id，只返回该用户拥有的角色所关联的权限
        if user_id:
            from app.models.user import User
            user = db.query(User).filter(User.id == user_id).first()
            if user:
                # 收集用户所有角色的权限
                permission_ids = set()
                for role in user.roles:
                    for permission in role.permissions:
                        permission_ids.add(permission.id)
                if permission_ids:
                    query = query.filter(Permission.id.in_(permission_ids))
                else:
                    return []
            else:
                return []
        return query.offset(skip).limit(limit).all()
    
    @staticmethod
    def get_permission_by_id(db: Session, permission_id: int) -> Optional[Permission]:
        """根据ID获取权限"""
        return db.query(Permission).filter(Permission.id == permission_id).first()
    
    @staticmethod
    def create_permission(db: Session, permission_create: PermissionCreate) -> Permission:
        """创建权限"""
        db_permission = Permission(
            name=permission_create.name,
            code=permission_create.code,
            description=permission_create.description
        )
        db.add(db_permission)
        db.commit()
        db.refresh(db_permission)
        return db_permission
    
    @staticmethod
    def update_permission(db: Session, permission_id: int, permission_update: PermissionUpdate) -> Optional[Permission]:
        """更新权限"""
        db_permission = db.query(Permission).filter(Permission.id == permission_id).first()
        if not db_permission:
            return None
        
        update_data = permission_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_permission, field, value)
        
        db.commit()
        db.refresh(db_permission)
        return db_permission
    
    @staticmethod
    def delete_permission(db: Session, permission_id: int) -> bool:
        """删除权限"""
        db_permission = db.query(Permission).filter(Permission.id == permission_id).first()
        if not db_permission:
            return False
        
        db.delete(db_permission)
        db.commit()
        return True
