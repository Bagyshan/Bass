
from datetime import datetime
from typing import Optional

from pydantic import BaseModel


from datetime import datetime
from pydantic import BaseModel
from typing import Optional

class PostBase(BaseModel):
    title: str
    body: str
    image: str
    lat: float
    lng: float

class PostCreate(PostBase):
    owner: int

class PostUpdate(PostBase):
    pass