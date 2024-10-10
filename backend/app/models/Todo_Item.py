import enum
from sqlalchemy.schema import Column, ForeignKey
from sqlalchemy.types import String, Text, UUID, Enum
from sqlalchemy.orm import relationship, mapped_column , Mapped

from .Category import Category
from .User import User

from .Model_Base import BaseModel

class item_status(enum.Enum):
    Todo = 'To do'
    Processing = 'Processing'
    Done = 'Done'

class Todo_Item(BaseModel):
    __tablename__ = "todo_item"
    
    name = Column("name", String(25), nullable=False)
    description = Column("description", Text, nullable=False)
    status = Column(Enum(item_status), nullable=False, default=item_status.Todo)

    created_by:Mapped[str] = mapped_column(UUID, ForeignKey("user.id"), nullable=False)
    category_id:Mapped[str] = mapped_column(UUID, ForeignKey("category.id"), nullable=True)
    
    user:Mapped["User"] = relationship(back_populates="todo_item", cascade="all, delete-orphan")
    categories:Mapped["Category"] = relationship(back_populates="todo_item", cascade="all, delete-orphan")
