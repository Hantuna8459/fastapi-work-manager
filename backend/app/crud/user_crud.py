from backend.app.models.User import User
from backend.app.schema.user_schema import UserRegisterRequest
from backend.app.core.password import get_hashed_password
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.core.database import DatabaseExecutionException
from .Crud_Core import *


async def read_user_by_user_id(session: AsyncSession, user_id: str):
    try:
        query = select(User).where(User.id.__eq__(user_id))
        result = await session.execute(query)
        user = result.scalar_one_or_none()
        return user
    except SQLAlchemyError as e:
        raise DatabaseExecutionException(str(e))

async def get_user_by_email_or_username(*, session: AsyncSession, email:str, username:str)\
        ->User | None:
    """
    retrieve both email and username
    """
    statement = select(User).where(
        (User.email == email) | (User.username == username)
    )
    session_user = await session.execute(statement)
    user = session_user.scalar_one_or_none()
    return user
    
async def register_request(*, session:AsyncSession, request:UserRegisterRequest)\
        ->User | None:

    new_user = User(
        email = request.email,
        username = request.username,
        password = get_hashed_password(request.password),
        is_active=True,
    )
    return await execute_with_refresh(session=session, object_add=new_user)