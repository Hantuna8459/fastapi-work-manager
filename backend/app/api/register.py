from typing import Any
from fastapi import APIRouter, Depends
from backend.app.utils import generate_register_mail, send_mail
from backend.app.crud import user_crud
from backend.app.schema.user_schema import UserRegister, UserResponse, UserCreate
from backend.app.core.database import get_db
from backend.app.core.auth import verify_password
from backend.app.core.exception import RegisterException, PasswordException
from sqlalchemy.orm import Session

router = APIRouter()

@router.post("/signup", response_model=UserResponse)
def register_user(*, user_in:UserRegister, session:Session = Depends(get_db))->Any:
    user = user_crud.get_user_by_email(session=session, email=user_in.email)
    if user:
        raise RegisterException()
    if not verify_password(user_in.password, user_in.password_confirm):
        raise PasswordException()
    user_create = UserCreate.model_validate(user_in)
    user = user_crud.user_create(session=session, user_create=user_create)
    email_data = generate_register_mail(email_to=user_in.email, username=user_in.username)
    send_mail(
        email_to=user_in.email,
        subject=email_data.subject,
        html_content=email_data.html_content,
    )
    return user