# api end point here
from fastapi import APIRouter, Depends, Request
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm

from backend.app.core.config import settings
from backend.app.core.database import get_db
from backend.app.core.exception import *
from .refresh_token import make_new_access_token
from .schema import *
from .login import login

auth_router = APIRouter(prefix="/auth")

@auth_router.post("/login")
async def auth_login(user = Depends(OAuth2PasswordRequestForm),
                     db = Depends(get_db)):

    dct = login(db, user)
    access_token = dct.get("access_token")
    refresh_token = dct.get("refresh_token")
    jwt_token = TokenBase(access_token=access_token,token_type="bearer")

    response = JSONResponse(jsonable_encoder(jwt_token))
    response.set_cookie(key="token",value=access_token,max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES*60,
                        httponly=True,secure=True,samesite="strict")
    response.set_cookie(key="refresh_token", value=refresh_token, max_age=settings.REFRESH_TOKEN_EXPIRE_MINUTES*60,
                        httponly=True, secure=True, samesite="strict")
    return response

@auth_router.get("/logout")
async def auth_logout(request: Request):

    token = request.cookies.get("token")
    if not token:
        raise NotLogin

    response = JSONResponse({"message": "Logout!"})
    response.delete_cookie("token")
    response.delete_cookie("refresh_token")
    return response

@auth_router.post("/refresh-token")
def refresh_access_token (request: Request, db = Depends(get_db)):
    new_access_token = make_new_access_token(request, db)
    return new_access_token