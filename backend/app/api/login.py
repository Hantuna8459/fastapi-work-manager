from fastapi import Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm

from backend.app.core.database import get_db
from backend.app.api.util import verify_password
from backend.app.api.exception import InvalidUser
from backend.app.core import auth
from backend.app.core.config import settings
from backend.app.api.routes import auth_router
from backend.app.api.schema import TokenBase


@auth_router.post("login")
async def auth_login(user = Depends(OAuth2PasswordRequestForm),
                     db = Depends(get_db)):
    
    db_user = auth.get_user(db, user.username)
    if (not db_user) or (not verify_password(user.password, db_user.password)):
        raise InvalidUser
    
    token = auth.create_access_token({"id": user.id})
    jwt_token = TokenBase(access_token=token,token_type="bearer")

    response = JSONResponse(jsonable_encoder(jwt_token))
    response.set_cookie(key="token",value=token,max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES*60,
                        httponly=True,secure=True,samesite="strict")
    return response