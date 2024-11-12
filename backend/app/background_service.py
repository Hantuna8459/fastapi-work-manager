from typing import Any
from asyncio import run
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger   
from backend.app.crud.user import get_user_with_todo_item_detail
from backend.app.utils import (
    process_query_result,
    generate_daily_status_mail,
    send_mail
)

async def send_daily_email()->Any:
    """
    Email to inform user about unfinished todo_item
    """
    query_data = await get_user_with_todo_item_detail()
    formatted_data = process_query_result(query_data)
    
    for user_data in formatted_data:
        email_to = user_data["email"]
        username = user_data["username"]
        task_data = user_data["task_data"]
    
        email_data = generate_daily_status_mail(email_to=email_to,
                                            username=username,
                                            task_data=task_data,)
        send_mail(email_to = email_to,
                    subject=email_data.subject,
                    html_content=email_data.html_content)

# Set up the scheduler
scheduler = BackgroundScheduler()
trigger = CronTrigger(hour=17, minute=0)
scheduler.add_job(lambda:run (send_daily_email()), trigger)

    