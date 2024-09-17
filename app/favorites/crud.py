from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException, status
from app.favorites.models import Favorite
from sqlalchemy.orm import joinedload, selectinload
from app.favorites.models import Favorite

async def add_favorite(session: AsyncSession, user_id: int, post_id: int) -> Favorite:
    favorite = Favorite(user_id=user_id, post_id=post_id)
    session.add(favorite)
    await session.commit()
    await session.refresh(favorite)
    return favorite                  

async def remove_favorite(session: AsyncSession, user_id: int, post_id: int) -> bool:
    result = await session.execute(select(Favorite).filter_by(user_id=user_id, post_id=post_id))
    favorite = result.scalars().first()
    
    if not favorite:
        raise HTTPException(status_code=404, detail="Пост не найден в избранном")
    
    await session.delete(favorite)
    await session.commit()
    return True

async def get_user_favorites(session: AsyncSession, user_id: int):                  
    result = await session.execute(select(Favorite).filter_by(user_id=user_id).options(joinedload(Favorite.post)))
    return result.scalars().all()
