from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.core.database import DatabaseExecutionException


async def execute_with_select(session: AsyncSession, query):
    try:
        result = await session.execute(query)
    except SQLAlchemyError as e:
        raise DatabaseExecutionException(str(e))

    return result


async def execute_with_no_refresh(session: AsyncSession, query):
    try:
        await session.execute(query)
        await session.commit()
    except SQLAlchemyError as e:
        await session.rollback()
        raise DatabaseExecutionException(str(e))


async def execute_with_refresh(session: AsyncSession, object_add):
    try:
        session.add(object_add)
        await session.commit()
        await session.refresh(object_add)
    except SQLAlchemyError as e:
        await session.rollback()
        raise DatabaseExecutionException(str(e))

    return object_add