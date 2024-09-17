from pydantic import BaseModel
from typing import List

class FavoriteBase(BaseModel):
    post_id: int

class FavoriteCreate(FavoriteBase):
    pass

class Favorite(FavoriteBase):
    id: int
    post_id: int

    class Config:
        from_attributes = True
                    