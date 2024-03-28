from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import declared_attr, Mapped, mapped_column
from sqlalchemy.ext.asyncio import async_sessionmaker

from .config import settings

Base = declarative_base()

class CustomBase(Base):
    __abstract__ = True
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower() + 's'

    id: Mapped[int] = mapped_column(primary_key=True)

engine = create_async_engine(settings.DATABASE_URL, echo=True)

async_session_maker = async_sessionmaker(
    engine,
    expire_on_commit=False,
    class_=AsyncSession  
)

async def get_db():
    async with async_session_maker() as session:
        yield session
