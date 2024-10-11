import enum
from sqlalchemy.schema import Column, ForeignKey
from sqlalchemy.types import String, Text, Enum

from .Model_Base import BaseModel

class ItemStatus(enum.Enum):
    Todo = 'To do'
    Processing = 'Processing'
    Done = 'Done'

class Todo_Item(BaseModel):
    __tablename__ = "todo_item"
    
    name = Column("name", String(25), nullable=False)
    description = Column("description", Text, nullable=False)
    status = Column(Enum(ItemStatus), nullable=False, default=ItemStatus.Todo)
    created_by = Column("created_by", ForeignKey("user.id"), nullable=False)
    category_id = Column("category_id", ForeignKey("category.id"), nullable=True)