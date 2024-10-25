import uuid
from sqlalchemy import Column, UUID, DateTime
from sqlalchemy.sql import func

from ..core.database import Base


class BaseModel(Base):
    __abstract__ = True
    
    id = Column("id", UUID, primary_key= True, index= True, default=uuid.uuid4)
    created_at = Column("created_at", DateTime, server_default=func.now())
    updated_at = Column("updated_at", DateTime, nullable=True,
                        server_onupdate=func.now())