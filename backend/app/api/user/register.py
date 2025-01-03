from typing import Any
from fastapi import APIRouter, Depends
from backend.app.utils import generate_register_mail, send_mail
from backend.app.crud import user
from backend.app.schema.user import UserRegisterRequest, UserResponse
from backend.app.core.database import get_db
from backend.app.core.exception import (
    EmailDuplicateException,
    UsernameDuplicateException,
    UnmatchedPasswordException,
    SomeThingWentWrong
)
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()


async def validate_user_data(session: AsyncSession, user_in: UserRegisterRequest):
    # check if email or username already registed
    existing_email = await user.get_user_by_email(
        session=session, email=user_in.email,
    )
    if existing_email:
        raise EmailDuplicateException
    
    existing_username = await user.get_user_by_username(
        session=session, username=user_in.username,
    )
    if existing_username:
        raise UsernameDuplicateException

    # check unmatched password
    if not user_in.password_confirm == user_in.password:
        raise UnmatchedPasswordException


@router.post("/signup", response_model=UserResponse)
async def register_user(*, user_in: UserRegisterRequest,
                        session: AsyncSession = Depends(get_db)) -> Any:
    await validate_user_data(session, user_in)

    user_data = UserRegisterRequest.model_validate(user_in)
    new_user = await user.register_request(session=session, request=user_data)

    # send email
    if new_user:
        email_data = generate_register_mail(email_to=user_in.email, username=user_in.username)
        try:
            send_mail(
                email_to=user_in.email,
                subject=email_data.subject,
                html_content=email_data.html_content,
            )
        except RuntimeError as e:
            return SomeThingWentWrong
    return new_user