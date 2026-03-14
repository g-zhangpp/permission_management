from fastapi import APIRouter, Depends, HTTPException, status, Form
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.user import User, UserLogin, Token
from app.services.auth_service import AuthService
from app.middlewares.auth import get_current_active_user
from app.models.user import User as UserModel


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=Token, description="用户登录")
def login(username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    """用户登录"""
    user_login = UserLogin(username=username, password=password)
    token = AuthService.login(db, user_login)
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return token


@router.post("/logout", description="用户登出")
def logout(current_user: UserModel = Depends(get_current_active_user)):
    """用户登出"""
    # 这里可以实现token黑名单等逻辑
    return {"message": "Successfully logged out"}


@router.post("/refresh", response_model=Token, description="刷新token")
def refresh_token(current_user: UserModel = Depends(get_current_active_user), db: Session = Depends(get_db)):
    """刷新token"""
    # 这里可以实现刷新token的逻辑
    from app.core.security import create_access_token
    from datetime import timedelta
    from app.core.config import settings
    
    access_token_expires = timedelta(minutes=settings.jwt["access_token_expire_minutes"])
    access_token = create_access_token(
        data={"sub": str(current_user.id)},
        expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


@router.get("/me", response_model=User, description="获取当前用户信息")
def get_current_user_info(current_user: UserModel = Depends(get_current_active_user)):
    """获取当前用户信息"""
    return current_user
