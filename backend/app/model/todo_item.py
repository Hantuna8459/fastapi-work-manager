import enum
from sqlalchemy.schema import Column, ForeignKey
from sqlalchemy.types import String, Text, Enum
from sqlalchemy.orm import relationship

from .base_model import BaseModel

class ItemStatus(enum.Enum):
    Todo = 'To do'
    Processing = 'Processing'
    Done = 'Done'

class TodoItem(BaseModel):
    __tablename__ = "todo_item"
    
    name = Column("name", String(25), nullable=False)
    description = Column("description", Text, nullable=False)
    status = Column(Enum(ItemStatus), nullable=False, default=ItemStatus.Todo)
    created_by = Column("created_by",
                        ForeignKey("user.id", ondelete="CASCADE", onupdate="CASCADE"),
                        nullable=False)

    category_id = Column("category_id",
                         ForeignKey("category.id", ondelete="CASCADE", onupdate="CASCADE"),
                         nullable=True)

    category = relationship("Category", back_populates="todo_items")