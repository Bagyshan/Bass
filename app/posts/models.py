
from datetime import datetime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from ..database import Base


class Post(Base):
    title: Mapped[str]
    body: Mapped[str]
    image: Mapped[str]
    owner: Mapped[str] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'))
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.utcnow, onupdate=datetime.utcnow)
    lat: Mapped[float]
    lng: Mapped[float]