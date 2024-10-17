from datetime import datetime
import uuid
from sqlalchemy import Column, UUID, DateTime
from core.database import Base
    
class BaseModel(Base):
    __abstract__ = True
    
    id = Column("id", UUID, primary_key= True, index= True, default=uuid.uuid4)
    created_at = Column("created_at", DateTime, default=datetime.now())
    updated_at = Column("updated_at", DateTime, default=datetime.now(), onupdate=datetime.now())