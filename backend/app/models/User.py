from datetime import datetime
from sqlalchemy.schema import Column
from sqlalchemy.types import String, DateTime, UUID

from core.database import Base


class User(Base):
    __tablename__ = "user"
    id = Column("id", UUID, primary_key= True, index= True)
    username = Column("name", String(25), nullable=False, unique=True)
    password = Column("password", String(50), nullable=False)
    email = Column("email", String(50), nullable=False, unique=True)
    created_time = Column("created_time", DateTime, default=datetime.now())
