from datetime import datetime
from sqlalchemy.schema import Column, ForeignKey
from sqlalchemy.types import String, DateTime, Text, UUID

from backend.app.core.db import Base


class Todo_Item(Base):
    __tablename__ = "todo_item"
    id = Column("id", UUID, primary_key= True, index= True)
    name = Column("name", String(25), nullable=False, unique=True)
    description = Column("description", Text, nullable=False)
    status = Column("status", String, default="Todo")
    created_time = Column("created_time", DateTime, default=datetime.now())
    created_by = Column("created_by", UUID, ForeignKey("user.id"), nullable=False)
    category_id = Column("category_id", UUID, ForeignKey("category.id"), nullable=True)
