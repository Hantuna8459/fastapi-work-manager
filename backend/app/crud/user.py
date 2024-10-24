from uuid import UUID
from backend.app.model.user import User
from backend.app.schema.user import UserRegisterRequest
from backend.app.core.password import get_hashed_password
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.core.database import DatabaseExecutionException
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def read_user_by_user_id(session: AsyncSession, user_id: UUID):
    try:
        query = select(User).where(User.id.__eq__(user_id))
        result = await session.execute(query)
        user = result.fetchone()
    except SQLAlchemyError as e:
        raise DatabaseExecutionException(str(e))

    if not user:
        return None

    return user[0]

async def get_user_by_email_or_username(*, session: AsyncSession, email:str, username:str)\
        ->User | None:
    """
    retrieve both email and username
    """
    statement = (select(User)
                 .where((User.email.__eq__(email))
                        or (User.username.__eq__(username))))

    session_user = await session.execute(statement)
    user = session_user.fetchone()
    if not user:
        return None

    return user[0]
    
async def register_request(*, session:AsyncSession, request:UserRegisterRequest)\
        ->User | None:

    new_user = User(
        email = request.email,
        username = request.username,
        password = get_hashed_password(request.password),
        is_active=True,
    )
    try:
        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)
        return new_user
    except SQLAlchemyError as e:
        await session.rollback()
        logger.error(f"SQLAlchemy error occurred: {e}")
        return None
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
        return None