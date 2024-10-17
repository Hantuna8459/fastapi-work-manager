from datetime import datetime, timedelta, timezone

from passlib.context import CryptContext
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status, Request
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer

from backend.app.crud.user_crud import get_user_by_id
from backend.app.models import User
from .config import settings
from .database import get_db
from .exception import UserNotActiveException

# ADMIN_SECRET = settings.ADMIN_SECRET
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES
REFRESH_TOKEN_EXPIRE_MINUTES = settings.REFRESH_TOKEN_EXPIRE_MINUTES

oauth2_scheme = OAuth2PasswordBearer(tokenUrl = "login")

pwd_context= CryptContext(schemes=[settings.CRYPTCONTEXT_SCHEME], deprecated="auto")

# get hash password
def get_hashed_password(password:str):
    return pwd_context.hash(password)

# verify password
def verify_password(password:str, user_password:str):
    return pwd_context.verify(password, user_password)

# create access token
# nhận vào dict có id của user
# trả về token đã đc mã hóa
def create_access_token(payload: dict):
    to_encode = payload.copy()
    expire = (datetime.now(timezone.utc) +
              timedelta(minutes = settings.ACCESS_TOKEN_EXPIRE_MINUTES))

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm = settings.ALGORITHM)
    return encoded_jwt

# vertify user and information form token
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credeentials_exception = HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail = "Could not validate credentials", headers = {"WWW-Authenticate": "Bearer"}, )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms = [ALGORITHM])
        user_id: str = payload.get("id")
        if user_id is None:
            raise credeentials_exception
    except JWTError:
        raise credeentials_exception
    user = get_user_by_id(db, user_id = user_id)
    if user is None:
        raise credeentials_exception
    return user
    
async def get_current_active_user(current_user = Depends(get_current_user)):
    if not current_user.is_active:
        raise UserNotActiveException()

    return current_user