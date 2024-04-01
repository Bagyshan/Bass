
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.engine import Result
from sqlalchemy.orm import joinedload, selectinload
import json
from datetime import datetime, date, time

from .schemas import PostBase
from .models import Post
from . import schemas, models
from ..database import scoped_session_dependency


async def create_post(
        session: AsyncSession, 
        post: schemas.PostBase,
        current_user_id: int,
    ) -> schemas.PostCreate:
    post_data = post.dict()
    post_data["owner"] = current_user_id
    post_data["date"] = date.fromisoformat(str(post_data["date"]))
    post_data["time"] = time.fromisoformat(str(post_data["time"]))
    post = Post(**post_data)
    session.add(post)
    await session.commit()
    return post

async def get_post(session: AsyncSession, post_id: int) -> dict | None:
    stmt = select(Post).options(joinedload(Post.owner_details)).filter(Post.id == post_id)
    result: Result = await session.execute(stmt)
    post = result.scalar()

    if post is not None:
        post_dict = {
            "id": post.id,
            "owner": post.owner_details.username,
            "owner_id": post.owner_details.id,
            "title": post.title, 
            "body": post.body, 
            "image": post.image, 
            "date": post.date,
            "time": post.time, 
            "is_free": post.is_free,
            "lat": post.lat, 
            "lng": post.lng, 
        }
        return post_dict
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found",
        )


async def get_posts(session: AsyncSession) -> list[dict]:
    stmt = select(Post).options(joinedload(Post.owner_details)).order_by(Post.id)
    result: Result = await session.execute(stmt)
    posts = result.scalars().all()
    return [
        {
            "id": post.id, 
            "owner": post.owner_details.username, 
            "owner_id": post.owner_details.id, 
            "title": post.title, 
            "body": post.body, 
            "image": post.image, 
            "date": post.date,
            "time": post.time, 
            "is_free": post.is_free,
            "lat": post.lat, 
            "lng": post.lng, 
        } for post in posts
    ]


# async def update_post(db: AsyncSession, post_id: int, post: schemas.PostUpdate):
#     async with db() as session:
#         db_post = await session.execute(select(Post).filter(Post.id == post_id))
#         if db_post := db_post.scalar():
#             for key, value in post.dict().items():
#                 setattr(db_post, key, value)
#             await session.commit()
#             await session.refresh(db_post)
#         return db_post

# async def delete_post(db: AsyncSession, post_id: int):
#     async with db() as session:
#         db_post = await session.execute(select(Post).filter(Post.id == post_id))
#         if db_post := db_post.scalar():
#             session.delete(db_post)
#             await session.commit()
#         return db_post


async def update_post(
        session: AsyncSession,
        post_id: int,
        post_update: schemas.PostUpdatePatch,
        current_user_id: int,
    ) -> schemas.PostCreate:
    stmt = select(Post).filter(Post.id == post_id)
    result: Result = await session.execute(stmt)
    post = result.scalar()
    if post.owner != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="It's not your post"
        )

    if post is not None:
        post_data = post_update.dict(exclude_unset=True)
        post_data["date"] = date.fromisoformat(str(post_data["date"]))
        post_data["time"] = time.fromisoformat(str(post_data["time"]))
        for key, value in post_data.items():
            setattr(post, key, value)
        await session.commit()
        return post
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found",
        )


async def delete_post(
        session: AsyncSession, 
        post_id: int, 
        current_user_id: int
    ) -> str:
    stmt = select(Post).filter(Post.id == post_id)
    result: Result = await session.execute(stmt)
    post = result.scalar()

    if post.owner != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="It's not your post"
        )
    
    if post is not None:
        await session.delete(post)
        await session.commit()
        return "Post deleted successfully"
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found",
        )