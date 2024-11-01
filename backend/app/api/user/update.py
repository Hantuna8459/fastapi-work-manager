import logging
from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.core.database import DatabaseExecutionException
from backend.app.crud import user
from backend.app.schema.user import (
    UsernameUpdateRequest, 
    FullnameUpdateRequest,
    UserUpdatePassword,
    UserResponse,
)
from backend.app.models.user import User
from backend.app.core.database import get_db
from backend.app.core.auth import get_current_user
from backend.app.core.password import verify_password
from backend.app.core.exception import (
    UsernameDuplicateException,
    UnmatchedPasswordException,
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()
    
@router.patch("/user/{user_id}/update_username", response_model=UserResponse,
            response_model_exclude={"email"})
async def user_update_username(*,
                                session: AsyncSession = Depends(get_db),
                                user_in: UsernameUpdateRequest,
                                current_user:User = Depends(get_current_user),
                                )->Any:
    
    existed_username = await user.get_user_by_username(
        session=session,
        username=user_in.username
    )
    if existed_username:
        raise UsernameDuplicateException
    
    updated_user = await user.user_update_username(session=session,
                                                   user_id=current_user.id,
                                                   request=user_in)
    return updated_user

@router.patch("/user/{user_id}/update_fullname")
async def user_update_fullname(*,
                                session: AsyncSession = Depends(get_db),
                                user_in: FullnameUpdateRequest,
                                current_user:User = Depends(get_current_user),
                                ) ->Any:
    try:
        await user.user_update_fullname(session=session,
                                        user_id=current_user.id,
                                        request=user_in)
    except DatabaseExecutionException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
    return JSONResponse(jsonable_encoder({"status": "OK"}))

@router.patch("/user/{user_id}/update_password")
async def user_update_password(*,
                               session: AsyncSession = Depends(get_db),
                               body: UserUpdatePassword,
                               current_user:User = Depends(get_current_user),
                               ) ->Any:
    
    if not verify_password(body.current_password, current_user.password):
        raise HTTPException(
            status_code=400,
            detail="Incorrect password",
        )
    if body.current_password == body.new_password:
        raise HTTPException(
            status_code=400,
            detail="New password cannot be the same as the current one",
        )
    if not body.password_confirm == body.new_password:
        raise UnmatchedPasswordException

    await user.user_update_password(session=session,
                                    user_id=current_user.id,
                                    request=body)
    return JSONResponse(jsonable_encoder({"status": "OK"}))