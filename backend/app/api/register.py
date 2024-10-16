from typing import Any
from fastapi import APIRouter, Depends
from backend.app.utils import generate_register_mail, send_mail
from backend.app.crud import user_crud
from backend.app.schema.user_schema import UserRegister, UserResponse, UserCreate
from backend.app.core.database import get_db
from backend.app.core.auth import verify_password
from backend.app.core.exception import(
    EmailDuplicateException,
    UsernameDuplicateException,
    UnmatchedPasswordException,
)
from sqlalchemy.orm import Session

router = APIRouter()

@router.post("/signup", response_model=UserResponse)
def register_user(*, user_in:UserRegister, session:Session = Depends(get_db))->Any:
    # check if email or username already existed
    user = user_crud.get_user_by_email_or_username(
        session=session,
        email=user_in.email,
        username=user_in.username
        )
    if user:
        if user.email == user_in.email:
            raise EmailDuplicateException()
        if user.username == user_in.username:
            raise UsernameDuplicateException()
    # check password input
    if not verify_password(user_in.password, user_in.password_confirm):
        raise UnmatchedPasswordException()
    
    user_create = UserCreate.model_validate(user_in)
    user = user_crud.user_create(session=session, user_create=user_create)
    
    # send email
    email_data = generate_register_mail(email_to=user_in.email, username=user_in.username)
    send_mail(
        email_to=user_in.email,
        subject=email_data.subject,
        html_content=email_data.html_content,
    )
    return user