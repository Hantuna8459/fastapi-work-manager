from sqlalchemy.schema import Column, ForeignKey
from sqlalchemy.types import Integer
from sqlalchemy.orm import relationship

from .base_model import Base


class UserCategory(Base):
    __tablename__ = "user_category"
    id = Column("id", Integer, primary_key=True, autoincrement=True)
    user_id = Column("user_id",
                     ForeignKey("user.id", ondelete="CASCADE", onupdate="CASCADE"),
                     nullable=False)

    category_id = Column("category_id",
                         ForeignKey("category.id", ondelete="CASCADE", onupdate="CASCADE"),
                         nullable=False)

    category = relationship("Category", back_populates="user_ids")