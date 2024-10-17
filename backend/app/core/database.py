# db connect here
from sqlalchemy.schema import MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

from backend.app.core.config import settings

engine = create_async_engine(str(settings.SQLALCHEMY_DATABASE_URI))

SessionLocal = async_sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base(metadata=MetaData())

def get_db() -> AsyncSession: # type: ignore
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

class DatabaseExecutionException(Exception):
    def __init__(self, message: str):
        self.message = f"Error executing SQL: {message}"
        super().__init__(self.message)