from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.user import User
from app.models.role import Role
from app.schemas.user import UserCreate, UserUpdate, UserWithRoles
from app.core.security import get_password_hash


class UserService:
    """用户服务"""
    
    @staticmethod
    def get_users(db: Session, skip: int = 0, limit: int = 100, user_id: Optional[int] = None) -> List[User]:
        """获取用户列表"""
        query = db.query(User)
        # 如果指定了user_id，只返回该用户的数据
        if user_id:
            query = query.filter(User.id == user_id)
        return query.offset(skip).limit(limit).all()
    
    @staticmethod
    def get_user_by_id(db: Session, user_id: int) -> Optional[User]:
        """根据ID获取用户"""
        return db.query(User).filter(User.id == user_id).first()
    
    @staticmethod
    def get_user_by_username(db: Session, username: str) -> Optional[User]:
        """根据用户名获取用户"""
        return db.query(User).filter(User.username == username).first()
    
    @staticmethod
    def create_user(db: Session, user_create: UserCreate) -> User:
        """创建用户"""
        hashed_password = get_password_hash(user_create.password)
        db_user = User(
            username=user_create.username,
            email=user_create.email,
            password_hash=hashed_password
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    
    @staticmethod
    def update_user(db: Session, user_id: int, user_update: UserUpdate) -> Optional[User]:
        """更新用户"""
        db_user = db.query(User).filter(User.id == user_id).first()
        if not db_user:
            return None
        
        update_data = user_update.model_dump(exclude_unset=True)
        if "password" in update_data:
            update_data["password_hash"] = get_password_hash(update_data.pop("password"))
        
        for field, value in update_data.items():
            setattr(db_user, field, value)
        
        db.commit()
        db.refresh(db_user)
        return db_user
    
    @staticmethod
    def delete_user(db: Session, user_id: int) -> bool:
        """删除用户"""
        db_user = db.query(User).filter(User.id == user_id).first()
        if not db_user:
            return False
        
        db.delete(db_user)
        db.commit()
        return True
    
    @staticmethod
    def get_user_roles(db: Session, user_id: int) -> List[Role]:
        """获取用户角色"""
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return []
        return user.roles
    
    @staticmethod
    def assign_user_roles(db: Session, user_id: int, role_ids: List[int]) -> Optional[User]:
        """分配用户角色"""
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return None
        
        roles = db.query(Role).filter(Role.id.in_(role_ids)).all()
        user.roles = roles
        
        db.commit()
        db.refresh(user)
        return user
