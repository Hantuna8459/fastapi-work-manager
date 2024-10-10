# api end point here
from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status, Body, Request, Response
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.encoders import jsonable_encoder
from jose import jwt, JWTError
from passlib.context import CryptContext
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from backend.app.core.auth import SECRET_KEY, ALGORITHM, get_user, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from backend.app.core.database import get_db
from backend.app.core.config import settings
from backend.app.core import auth


auth_router = APIRouter(prefix="auth")
pwd_context= CryptContext(schemes=[settings.CRYPTCONTEXT_SCHEME], deprecated="auto")


class TokenBase(BaseModel):
    access_token: str
    token_type: str


def get_hashed_password(password:str):
    return pwd_context.hash(password)

def verify_password(password:str, user_password:str):
    return pwd_context.verify(password, user_password)   

@auth_router.post("login")
async def auth_login(user = Depends(OAuth2PasswordRequestForm),
                     db = Depends(get_db)):
    
    InvalidUser = HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Wrong username or password"
        )
    
    db_user = auth.get_user(db, user.username)
    if (not db_user) or (not verify_password(user.password, db_user.password)):
        raise InvalidUser
    
    token = auth.create_access_token({"id": user.id})
    refresh_token = auth.create_refresh_token({"id": user.id})
    jwt_token = TokenBase(access_token=token,token_type="bearer")

    response = JSONResponse(jsonable_encoder(jwt_token))
    response.set_cookie(key="access_token",value=token,max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES*60,
                        httponly=True,secure=True,samesite="strict")
    response.set_cookie(key="refresh_token", value=refresh_token, max_age=settings.REFRESH_TOKEN_EXPIRE_MINUTES*60,
                        httponly=True, secure=True, samesite="strict")
    return response
        
@auth_router.get("logout")
async def auth_logout(request: Request):

    NotLogin = HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Not login"
    )
    token = request.cookies.get("access_token")
    if not token:
        raise NotLogin
    
    response = JSONResponse({"message": "Logout!"})
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")
    return response

@auth_router.post("refresh-token")
def refresh_token(request: Request, db = Depends(get_db)):
    # Lấy refresh token từ cookies
    refresh_token = request.cookies.get("refresh_token")

    if refresh_token is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh token missing")

    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})

    try:
        # Giải mã refresh token
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    # Kiểm tra xem người dùng có tồn tại không
    user = get_user(db, username=username)
    if user is None:
        raise credentials_exception

    # Tạo access token mới
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)

    return {"access_token": access_token, "token_type": "bearer"}
