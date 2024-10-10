# api end point here
from fastapi import APIRouter, Depends, HTTPException, status, Body, Request
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.encoders import jsonable_encoder
from passlib.context import CryptContext
from fastapi.responses import JSONResponse
from pydantic import BaseModel

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
    jwt_token = TokenBase(access_token=token,token_type="bearer")

    response = JSONResponse(jsonable_encoder(jwt_token))
    response.set_cookie(key="token",value=token,max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES*60,
                        httponly=True,secure=True,samesite="strict")
    return response
        
@auth_router.get("logout")
async def auth_logout(request: Request):

    NotLogin = HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Not login"
    )
    token = request.cookies.get("token")
    if not token:
        raise NotLogin
    
    response = JSONResponse({"message": "Logout!"})
    response.delete_cookie("token")
    return response

