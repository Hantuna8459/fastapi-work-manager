from asyncio import run
from typing import Any, List, Dict
from collections import defaultdict
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger   
from backend.app.crud.user import get_user_with_todo_item_detail
from backend.app.utils import send_mail, generate_daily_status_mail

from collections import defaultdict

def process_task_details_result(result) -> List[Dict[str, Any]]:
    """
    This function processes the query result into a list of users, each containing 
    a list of task_data aggregated by category.
    """
    users = defaultdict(lambda: {"email": None, "username": None, "task_data": []})

    for row in result:
        email = row["email"]
        username = row["username"]
        task_count = row["task_count"]
        category_name = row["category_name"]
        task_name = row["task_name"]
        # Initialize user entry if not already
        user = users[email]
        user["email"] = email
        user["username"] = username

        # Append task data grouped by category
        user["task_data"].append({
            "task_count": task_count,
            "category_name": category_name,
            "task_name": task_name
        })

    # Convert defaultdict to list
    return list(users.values())

  
async def send_daily_email()->Any:
    """
    Email to inform user about unfinished item
    """
    query_data = await get_user_with_todo_item_detail()
    formatted_data = process_task_details_result(query_data)
    
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

#Set up the scheduler
scheduler = BackgroundScheduler()
trigger = CronTrigger(hour=17, minute=0)
scheduler.add_job(lambda:run (send_daily_email()), trigger)

    