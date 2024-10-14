from sqlalchemy.schema import Column, ForeignKey
from sqlalchemy.types import Integer

from .Model_Base import Base


class UserCategory(Base):
    __tablename__ = "user_category"
    id = Column("id", Integer, primary_key=True, autoincrement=True)
    user_id = Column("user_id", ForeignKey("user.id"), nullable=False)
    category_id = Column("category_id", ForeignKey("category.id"), nullable=False)