from sqlalchemy.schema import Column
from sqlalchemy.types import String, Text
from sqlalchemy.orm import relationship

from .Model_Base import BaseModel
from .User_Category import User_Category


class Category(BaseModel):
    __tablename__ = "category"
    
    name = Column("name", String(25), nullable=False, unique=True)
    description = Column("description", Text, nullable=False)
    
    created_by = relationship("User", secondary=User_Category, back_populates="category", cascade="all, delete-orphan")
    