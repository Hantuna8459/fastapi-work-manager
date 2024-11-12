from fastapi import APIRouter, Depends
from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.utils import (
    send_mail,
    generate_test_email, 
    generate_daily_status_mail,
    process_query_result,
    )
from backend.app.crud.user import get_user_with_todo_item_detail


router = APIRouter()

@router.post("/test-email/send-one")
def test_email(email_to:EmailStr)->None:
    """
    Test send email to one
    """
    email_data = generate_test_email(email_to=email_to, username=None)
    send_mail(
        email_to=email_to,
        subject=email_data.subject,
        html_content=email_data.html_content,
    )

@router.post("/test-email/send-all")
async def send_daily_email()->None:
    """
    Email to inform user about unfinished item
    """
    query_data = await get_user_with_todo_item_detail()
    organized_data = process_query_result(query_data)
    
    for user_data in organized_data:
        email = user_data["email"]
        username = user_data["username"]
        task_data = user_data["task_data"]
    
        email_data = generate_daily_status_mail(email_to=email,
                                                username=username,
                                                task_data=task_data,)
    
        send_mail(email_to = email,
                subject=email_data.subject,
                html_content=email_data.html_content)