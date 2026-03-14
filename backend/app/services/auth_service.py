from datetime import timedelta
from typing import Optional
from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserLogin, Token
from app.core.security import verify_password, create_access_token
from app.core.config import settings


class AuthService:
    """认证服务"""
    
    @staticmethod
    def login(db: Session, user_login: UserLogin) -> Optional[Token]:
        """用户登录"""
        user = db.query(User).filter(User.username == user_login.username).first()
        if not user:
            return None
        
        if not verify_password(user_login.password, user.password_hash):
            return None
        
        access_token_expires = timedelta(minutes=settings.jwt["access_token_expire_minutes"])
        access_token = create_access_token(
            data={"sub": str(user.id)},
            expires_delta=access_token_expires
        )
        
        return Token(access_token=access_token, token_type="bearer")
    
    @staticmethod
    def get_current_user_info(db: Session, user_id: int) -> Optional[dict]:
        """获取当前用户信息"""
        user = db.query(User).filter(User.id == user_id).first()
        if user:
            # 获取用户的权限列表
            permissions = set()
            for role in user.roles:
                for permission in role.permissions:
                    permissions.add(permission.code)
            
            # 获取用户的角色列表
            roles = [role.name for role in user.roles]
            
            return {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "created_at": user.created_at,
                "updated_at": user.updated_at,
                "roles": roles,
                "permissions": list(permissions)
            }
        return None
