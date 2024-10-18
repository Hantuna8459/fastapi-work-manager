from datetime import datetime, timedelta, timezone
from typing import Any

from passlib.context import CryptContext
from sqlalchemy.orm import Session
from fastapi import Depends
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer
from pydantic import ValidationError

from backend.app.crud.user_crud import get_user_by_email_or_username
from backend.app.models import User
from backend.app.schema.token_schema import TokenPayload
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
def get_current_user(token: str = Depends(oauth2_scheme),
                     session: Session = Depends(get_db)
                     )->User:
    try:
        payload =jwt.decode(
            token, settings.SECRET_KEY, algorithm=settings.ALGORITHM
        )
        token_data = TokenPayload(**payload)# unpacks the dictionary payload into keyword arguments
    except(JWTError, ValidationError):
        raise CredentialsException()
    user = session.get(User, token_data.sub)
    if not user:
        raise CredentialsException()
    if not user.is_active:
        raise UserNotActiveException()
    return user

def authenticate(*, session:Session = Depends(get_db), identifier: str, password: str)->User|None:
    db_user = get_user_by_email_or_username(
        session=session,
        email=identifier,
        username=identifier,
        )
    if not db_user:
        return None
    if not verify_password(password, db_user.password):
        return None
    return db_user