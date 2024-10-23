from fastapi import APIRouter, BackgroundTasks
from pydantic import EmailStr

from backend.app.utils import (
    send_mail,
    send_mass_mail_background,
    generate_test_email,
)

router = APIRouter()

@router.post("/test-email/asynchronous")
def test_email(email_to:EmailStr)->str:
    email_data = generate_test_email(email_to=email_to)
    send_mail(
        email_to=email_to,
        subject=email_data.subject,
        html_content=email_data.html_content,
    )
    return 'success'

@router.post("/test-email/background")
async def send_mass_email_background(background_tasks:BackgroundTasks, email_to:EmailStr)->str:
    email_data = generate_test_email(email_to=email_to)
    background_tasks.add_task(
        send_mass_mail_background,
        email_to=email_to,
        subject=email_data.subject,
        html_content=email_data.html_content,
    )
    return 'success'
# @router.get("/health-check/")
# async def health_check() -> bool:
#     return True