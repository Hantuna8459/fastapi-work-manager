from datetime import timedelta
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.schema.token import Token
from backend.app.core import auth
from backend.app.core.config import settings
from backend.app.core.database import get_db
from backend.app.core.exception import (
    InvalidUser,
    UserNotActiveException
)

router = APIRouter()

@router.post("/login", response_model=Token,)
async def login_with_token(form_data: OAuth2PasswordRequestForm = Depends(),
                           session:AsyncSession=Depends(get_db)):
    user = await auth.authenticate(
        session=session, identifier=form_data.username, password=form_data.password
    )
    if not user:
        raise InvalidUser
    if not user.is_active:
        raise UserNotActiveException
    user.last_login = func.now()
    await session.commit()
    await session.refresh(user)
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return Token(
        access_token=auth.create_access_token(
            user.id, expires_delta=access_token_expires
        )
    )