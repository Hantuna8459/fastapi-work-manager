from sqlalchemy.schema import Column, ForeignKey
from sqlalchemy.types import String, Text
from sqlalchemy.orm import relationship

from .Model_Base import BaseModel


class Category(BaseModel):
    __tablename__ = "category"
    
    name = Column("name", String(25), nullable=False, unique=True)
    description = Column("description", Text, nullable=False)
    created_by = Column("created_by", ForeignKey("user.id"), nullable=False)

    todo_items = relationship("Todo_Item")
    users = relationship("UserCategory")