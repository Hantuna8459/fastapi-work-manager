from sqlalchemy.schema import Column, ForeignKey, Table
from sqlalchemy.types import UUID

from .Model_Base import Base


User_Category = Table(
    "user_category",
    Base.metadata,
    
    Column("user_id", UUID, ForeignKey("user.id"), nullable=False),
    Column("category_id", UUID, ForeignKey("category.id"), nullable=False),
)