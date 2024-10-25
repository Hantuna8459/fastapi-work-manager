# db connect here
# # just for alembic
# from sqlalchemy import create_engine
# from sqlalchemy.schema import MetaData
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker
#
# from .config import settings
#
#
# engine = create_engine(str(settings.SQLALCHEMY_DATABASE_URI))
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# Base = declarative_base(metadata=MetaData())


from typing import AsyncGenerator
from sqlalchemy.schema import MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

from .config import settings


engine = create_async_engine(str(settings.SQLALCHEMY_DATABASE_URI))
SessionLocal = async_sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base(metadata=MetaData())


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as db:
        yield db

class DatabaseExecutionException(Exception):
    def __init__(self, message: str):
        self.message = f"Error executing SQL: {message}"
        super().__init__(self.message)