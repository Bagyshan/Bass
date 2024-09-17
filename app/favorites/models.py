from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship
from ..database import Base
from app.users.models import User
from app.posts.models import Post

class Favorite(Base):
    __tablename__ = "favorites"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    post_id = Column(Integer, ForeignKey("posts.id"), nullable=False)

    user = relationship("User", back_populates="favorites")
    post = relationship("Post")