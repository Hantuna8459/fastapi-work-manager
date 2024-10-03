from datetime import datetime
from sqlalchemy.schema import Column, ForeignKey
from sqlalchemy.types import String, Integer, DateTime, Text, UUID

from backend.app.core.db import Base


class User_Category(Base):
    __tablename__ = "user_category"
    id = Column("id", Integer, primary_key= True, index= True)
    user_id = Column("user_id", UUID, ForeignKey("user.id"), nullable=False)
    category_id = Column("category_id", UUID, ForeignKey("category.id"), nullable=False)
    created_time = Column("created_time", DateTime, default=datetime.now())