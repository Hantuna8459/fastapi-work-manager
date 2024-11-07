from fastapi import APIRouter, Depends
from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.utils import send_mail, generate_test_email, send_bulk_mail
from backend.app.crud.user import get_all_email
from backend.app.core.database import get_db

router = APIRouter()

@router.post("/test-email/send-one")
def test_email(email_to:EmailStr)->None:
    """
    Test send email to one
    """
    email_data = generate_test_email(email_to=email_to)
    send_mail(
        email_to=email_to,
        subject=email_data.subject,
        html_content=email_data.html_content,
    )

@router.post("/test-email/send-all")
async def test_bulk_email(session:AsyncSession=Depends(get_db))->None:
    """
    Test send email to all user
    """
    email_to =await get_all_email(session)
    email_data = generate_test_email(email_to=email_to)
    send_bulk_mail(
        email_to=email_to,
        subject=email_data.subject,
        html_content=email_data.html_content,
    )