from fastapi import APIRouter
from pydantic import EmailStr

from backend.app.utils import send_mail, generate_test_email

router = APIRouter()

@router.post("/test-email/")
def test_email(email_to:EmailStr)->str:
    """
    Test Email
    """
    email_data = generate_test_email(email_to=email_to)
    send_mail(
        email_to=email_to,
        subject=email_data.subject,
        html_content=email_data.html_content,
    )
    return "test email sent"

# @router.get("/health-check/")
# async def health_check() -> bool:
#     return True