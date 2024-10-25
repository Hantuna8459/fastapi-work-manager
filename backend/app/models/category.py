from sqlalchemy.schema import Column, ForeignKey
from sqlalchemy.types import String, Text
from sqlalchemy.orm import relationship

from .base_model import BaseModel


class Category(BaseModel):
    __tablename__ = "category"
    
    name = Column("name", String(25), nullable=False, unique=True)
    description = Column("description", Text, nullable=False)
    created_by = Column("created_by",
                        ForeignKey("user.id", ondelete="CASCADE", onupdate="CASCADE"),
                        nullable=False)

    todo_items = relationship("TodoItem",
                              back_populates="category", cascade="all, delete-orphan")

    user_ids = relationship("UserCategory",
                            back_populates="category", cascade="all, delete-orphan")