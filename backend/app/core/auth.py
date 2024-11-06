from datetime import datetime, timedelta, timezone
from typing import Any
from uuid import UUID

from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer
from pydantic import ValidationError

from backend.app.crud.user import (
    get_user_by_email,
    get_user_by_username,
    read_user_private_by_user_id,)
from backend.app.models import User
from backend.app.schema.token import TokenPayload
from backend.app.schema.user import UserPrivate
from backend.app.core.config import settings
from backend.app.core.database import get_db
from .password import verify_password
from .exception import (
    CredentialsException,
    UserNotActiveException,
)

# ADMIN_SECRET = settings.ADMIN_SECRET
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES
REFRESH_TOKEN_EXPIRE_MINUTES = settings.REFRESH_TOKEN_EXPIRE_MINUTES

oauth2_scheme = OAuth2PasswordBearer(tokenUrl = "login")

pwd_context= CryptContext(schemes=[settings.CRYPTCONTEXT_SCHEME], deprecated="auto")

def create_access_token(subject: str | Any, expires_delta: timedelta) -> str:
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

# vertify user and information form token
async def get_current_user(token: str = Depends(oauth2_scheme),
                     session: AsyncSession = Depends(get_db)
                     )\
        ->UserPrivate:

    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=settings.ALGORITHM,
        )
        token_data = TokenPayload(**payload)# unpacks the dictionary payload into keyword arguments
    except(JWTError, ValidationError):
        raise CredentialsException
    user = await read_user_private_by_user_id(session=session, user_id=UUID(token_data.sub) )
    if not user:
        raise CredentialsException
    if not user.is_active:
        raise UserNotActiveException
    return user

async def authenticate(*, session:AsyncSession, identifier: str,
                       password: str)\
        ->User|None:
    db_user = await get_user_by_username(
        session=session,
        # email=identifier,
        username=identifier,
    )
    if not db_user:
        db_user = await get_user_by_email(session=session, email=identifier)
    if not db_user:
        return None
    if not verify_password(password, db_user.password):
        return None
    return db_user