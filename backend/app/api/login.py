from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.security import OAuth2PasswordRequestForm

# from backend.app.schema.UserLoginSchema import UserLogin
from backend.app.schema.token_schema import Token
from backend.app.core import auth
from backend.app.core.config import settings
from backend.app.core.database import get_db
from backend.app.core import exception
from backend.app.crud import user_crud

login_router = APIRouter()

@login_router.post("/login")
async def auth_login(user: OAuth2PasswordRequestForm = Depends(),
                     db=Depends(get_db)):
    user = user_crud.authenticate()

    token = auth.create_access_token({"id": user.id})

    jwt_token = Token(access_token=token, token_type="bearer")

    # TO DO: add last login
    
    response = JSONResponse(jsonable_encoder(jwt_token))
    # response.set_cookie(key="token", value=token, max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    #                     httponly=True, secure=True, samesite="strict")
    return response