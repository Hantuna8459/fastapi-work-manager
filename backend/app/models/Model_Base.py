from datetime import datetime
import uuid
from sqlalchemy import Column, UUID, DateTime
from sqlalchemy.ext.declarative import as_declarative, declared_attr

@as_declarative()
class Base:
    __abstract__ = True
    __name__: str

    # (optional) auto generate table name
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()
    
class BaseModel(Base):
    __abstract__ = True
    
    id = Column("id", UUID, primary_key= True, index= True, default=uuid.uuid4)
    created_at = Column("created_at", DateTime, default=datetime.now())
    updated_at = Column("updated_at", DateTime, default=datetime.now(), onupdate=datetime.now())