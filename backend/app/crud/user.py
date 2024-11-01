from typing import List, Any
from uuid import UUID
from backend.app.models.user import User
from backend.app.crud.core import (
    execute_with_refresh,
    execute_with_select,
    execute_with_no_refresh,)
from backend.app.schema.user import (
    UserRegisterRequest,
    UsernameUpdateRequest,
    FullnameUpdateRequest,
    UserUpdatePassword,
    UserPrivate,
)
from backend.app.core.password import get_hashed_password
from sqlalchemy import select, func, update
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.core.database import DatabaseExecutionException
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def read_list_email_by_list_user_id(session: AsyncSession, list_user_id: list[UUID],
                                          pagesize: int , page: int) \
        -> list[str] | None:

    limit = pagesize
    offset = (page - 1) * pagesize

    query = (select(User.email)
             .where(User.id.in_(list_user_id))
             .limit(limit).offset(offset))

    res = await execute_with_select(session, query)
    email_list = res.fetchall()

    if not email_list:
        return None

    lst = []
    for email in email_list:
        lst.append(email[0])

    return lst

async def read_user_private_by_user_id(session: AsyncSession, user_id: UUID) \
        -> UserPrivate | None:

    try:
        query = select(User.id, User.password, User.is_active).where(User.id.__eq__(user_id))
        result = await session.execute(query)
        user = result.fetchone()
    except SQLAlchemyError as e:
        raise DatabaseExecutionException(str(e))

    if not user:
        return None

    return UserPrivate(id=user[0], password=user[1], is_active=user[2])

async def get_user_by_email(*, session: AsyncSession, email:str)\
        ->User|None:
    """
    retrieve email, stop when found one
    """
    query = (select(User).where(User.email.__eq__(email)))

    result = await session.execute(query)
    user = result.scalar_one_or_none()
    return user

async def get_user_by_username(*, session: AsyncSession, username:str)\
        ->User|None:
    """
    retrieve username, stop when found one
    """
    query = (select(User).where(User.username.__eq__(username)))

    result = await session.execute(query)
    user = result.scalar_one_or_none()
    return user

async def get_all_email(session: AsyncSession)->List[str]:
    query = select(User.email)
    result = await execute_with_select(session, query)
    list = result.fetchall()
    emails = []
    for x in list:
        emails.append(x[0])
    return emails

async def register_request(*, session: AsyncSession, request: UserRegisterRequest)\
    ->Any:

    new_user = User(
        email = request.email,
        username = request.username,
        password = get_hashed_password(request.password),
        is_active = True,# Todo: change to false when verify email
    )
    user = await execute_with_refresh(session, new_user)
    return user

async def user_update_username(*, session: AsyncSession,
                               user_id:UUID,
                               request: UsernameUpdateRequest)\
    ->Any:

    query = (update(User)
             .where(User.id == user_id)
             .values(username=request.username)
             .execution_options(synchronize_session="fetch"))
    await execute_with_no_refresh(session, query)

    result = await session.execute(select(User).where(User.id == user_id))
    return result.scalar_one_or_none()

async def user_update_fullname(*, session: AsyncSession,
                               user_id:UUID,
                               request: FullnameUpdateRequest)\
    ->Any:

    query = (update(User)
             .where(User.id == user_id)
             .values(**request.__dict__)
             .execution_options(synchronize_session="fetch"))
    await execute_with_no_refresh(session, query)

async def user_update_password(*, session: AsyncSession,
                               user_id:UUID,
                               request: UserUpdatePassword)\
    -> Any:

    hashed_password = get_hashed_password(request.new_password)

    query = (update(User)
             .where(User.id == user_id)
             .values(password=hashed_password)
             .execution_options(synchronize_session="fetch"))
    await execute_with_no_refresh(session, query)