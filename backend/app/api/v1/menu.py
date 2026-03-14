from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.schemas.menu import Menu, MenuCreate, MenuUpdate, MenuWithChildren
from app.services.menu_service import MenuService
from app.middlewares.auth import get_current_active_user
from app.models.user import User as UserModel


router = APIRouter(prefix="", tags=["menu"])


@router.get("/menus", response_model=List[Menu], description="获取菜单列表")
def get_menus(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_active_user)):
    """获取菜单列表"""
    menus = MenuService.get_menus(db, skip=skip, limit=limit)
    return menus


@router.post("/menus", response_model=Menu, status_code=status.HTTP_201_CREATED, description="创建菜单")
def create_menu(menu: MenuCreate, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_active_user)):
    """创建菜单"""
    return MenuService.create_menu(db=db, menu_create=menu)


@router.get("/menus/tree", response_model=List[MenuWithChildren], description="获取菜单树")
def get_menu_tree(db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_active_user)):
    """获取菜单树"""
    return MenuService.get_menu_tree(db, user_id=current_user.id)


@router.get("/menus/{menu_id}", response_model=Menu, description="获取菜单详情")
def get_menu(menu_id: int, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_active_user)):
    """获取菜单详情"""
    db_menu = MenuService.get_menu_by_id(db, menu_id=menu_id)
    if db_menu is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Menu not found"
        )
    return db_menu


@router.put("/menus/{menu_id}", response_model=Menu, description="修改菜单信息")
def update_menu(menu_id: int, menu: MenuUpdate, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_active_user)):
    """修改菜单信息"""
    db_menu = MenuService.update_menu(db=db, menu_id=menu_id, menu_update=menu)
    if db_menu is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Menu not found"
        )
    return db_menu


@router.delete("/menus/{menu_id}", status_code=status.HTTP_204_NO_CONTENT, description="删除菜单")
def delete_menu(menu_id: int, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_active_user)):
    """删除菜单"""
    success = MenuService.delete_menu(db=db, menu_id=menu_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Menu not found"
        )
    return None
