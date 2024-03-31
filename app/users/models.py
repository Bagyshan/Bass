from sqlalchemy import Column, Integer, String, Boolean

from ..database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    is_vip = Column(Boolean, default=False)
    is_admin = Column(Boolean, default=False)
    first_name = Column(String, index=True)  
    last_name = Column(String, index=True)   