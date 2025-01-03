from sqlalchemy.schema import Column
from sqlalchemy.types import String, DateTime, Boolean

from .base_model import BaseModel


class User(BaseModel):
    __tablename__ = "user"
    
    username = Column("name", String(30), nullable=False, unique=True)
    password = Column("password", String(100), nullable=False)
    email = Column("email", String(50), nullable=False, unique=True)
    first_name = Column("first_name", String(50), default=None, nullable=True)
    last_name = Column("last_name", String(50), default=None, nullable=True)
    last_login = Column("last_login", DateTime, nullable=True)
    is_active = Column("is_active", Boolean, default=True)