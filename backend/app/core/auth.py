from datetime import datetime, timedelta
from typing import Optional

from passlib.context import CryptContext
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status, Request
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer

from backend.app.models import User
from .config import settings
from .database import get_db
from .exception import CredentialsException

ADMIN_SECRET = settings.ADMIN_SECRET
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
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes = ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm = ALGORITHM)
    return encoded_jwt

# create refresh token
def create_refresh_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes = REFRESH_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encode_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm = ALGORITHM)
    return encode_jwt

# get user from database
def get_user(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()

# vertify user and information form token
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credeentials_exception = HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail = "Could not validate credentials", headers = {"WWW-Authenticate": "Bearer"}, )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms = [ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credeentials_exception
    except JWTError:
        raise credeentials_exception
    user = get_user(db, username = username)
    if user is None:
        raise credeentials_exception
    return user

def get_old_refresh_token(request: Request):
    refresh_token = request.cookies.get("refresh_token")
    if refresh_token is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh token missing")
    else:
        return refresh_token

def make_new_access_token(request: Request, db = Depends(get_db)):
    # claim refresh token
    refresh_token = get_old_refresh_token(request)

    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise CredentialsException
    except JWTError:
        raise CredentialsException

    # is user in DB
    user = get_user(db, username=username)
    if user is None:
        raise CredentialsException

    # make new access token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)

    return {"access_token": access_token, "token_type": "bearer"}
