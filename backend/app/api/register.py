from typing import Any
from fastapi import APIRouter, Depends
from backend.app.utils import generate_register_mail, send_mail
from backend.app.crud import user_crud
from backend.app.schema.user_schema import UserRegisterRequest, UserResponse
from backend.app.core.database import get_db
from backend.app.core.exception import(
    EmailDuplicateException,
    UsernameDuplicateException,
    UnmatchedPasswordException,
)
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()

async def validate_user_data(session:AsyncSession, user_in:UserRegisterRequest):
    # check if email or username already registed
    existed_user = await user_crud.get_user_by_email_or_username(
            session=session,
            email=user_in.email,
            username=user_in.username
            )
    if existed_user:
        if existed_user.email == user_in.email:
            raise EmailDuplicateException
        if existed_user.username == user_in.username:
            raise UsernameDuplicateException

    # check unmatched password
    if not user_in.password_confirm == user_in.password:
        raise UnmatchedPasswordException
    

@router.post("/signup", response_model=UserResponse)
async def register_user(*, user_in:UserRegisterRequest,
                        session:AsyncSession = Depends(get_db))->Any:

    await validate_user_data(session, user_in)
    
    user_data = UserRegisterRequest.model_validate(user_in)
    new_user = await user_crud.register_request(session=session, request=user_data)

    # send email
    if new_user:
        email_data = generate_register_mail(email_to=user_in.email, username=user_in.username)
        send_mail(
            email_to=user_in.email,
            subject=email_data.subject,
            html_content=email_data.html_content,
        )
    return new_user