from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession     
from ..database import get_db
from app.users.auth import get_current_user
from app.users.schemas import User
from typing import List
from app.favorites.crud import remove_favorite, add_favorite, get_user_favorites, Favorite
from app.favorites.shemas import Favorite

router = APIRouter(prefix="/favorites", tags=["favorites"])

@router.post("/", response_model=schemas.Favorite)
async def add_favorite(
    post_id: int,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    favorite = await crud.add_favorite(db, user_id=current_user.id, post_id=post_id)
    return favorite

@router.delete("/", response_model=dict)
async def remove_favorite(
    post_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    await remove_favorite(db, user_id=current_user.id, post_id=post_id)
    return {"message": "Пост успешно удален из избранного"}

@router.get("/", response_model=List[Favorite])
async def get_user_favorites(
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)  
):

    return await get_user_favorites(db, user_id=current_user.id)