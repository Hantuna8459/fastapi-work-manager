from fastapi import Depends, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from backend.app.core.auth import verify_password
from backend.app.core.database import get_db
from backend.app.core.exception import InvalidUser
from backend.app.core import auth
from backend.app.schema.TokenBaseSchema import TokenBase
from backend.app.schema.UserLoginSchema import UserLogin

login_router = APIRouter()

def login(db, user: UserLogin):
    
    db_user = auth.get_user(db, user.username)
    if (not db_user) or (not verify_password(user.password, db_user.password)):
        raise InvalidUser
    
    token = auth.create_access_token({"id": user.id})
    refresh_token = auth.create_refresh_token({"id": user.id})
                       
    return {"access_token": token, "refresh_token": refresh_token}

@login_router.post("/login")
async def auth_login(user = Depends(OAuth2PasswordRequestForm),
                     db = Depends(get_db)):

    dct = login(db, user)
    access_token = dct.get("access_token")
    refresh_token = dct.get("refresh_token")
    jwt_token = TokenBase(access_token=access_token,token_type="bearer")

    response = JSONResponse(jsonable_encoder(jwt_token))
    response.set_cookie(key="token",value=access_token,max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES,
                        httponly=True,secure=True,samesite="strict")
    response.set_cookie(key="refresh_token", value=refresh_token, max_age=settings.REFRESH_TOKEN_EXPIRE_MINUTES,
                        httponly=True, secure=True, samesite="strict")
    return response
