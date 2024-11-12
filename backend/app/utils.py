from typing import Any, List, Dict
from pathlib import Path
from collections import defaultdict
from backend.app.core.config import settings
from backend.app.crud.user import get_user_with_todo_item_detail
from jinja2 import Template
import logging
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EmailData:
    def __init__(self, html_content:str, subject:str) -> None:
        self.html_content = html_content
        self.subject = subject
        
def render_email_template(*, template_name:str, context:dict =[str, Any])->str:
    template_str = (Path(__file__).parent/"email_templates"/template_name).read_text()
    html_content = Template(template_str).render(context)
    return html_content

def connect():
    try:
        if settings.MAIL_SSL:
            server = smtplib.SMTP_SSL(settings.MAIL_HOST, settings.MAIL_PORT)
        else:
            server = smtplib.SMTP(settings.MAIL_HOST, settings.MAIL_PORT)
            if settings.MAIL_TLS:
                server.starttls()

        # Log in to the SMTP server
        server.login(settings.MAIL_USER, settings.MAIL_PASSWORD)
        logger.info('Mail services initialized')
        return server

    except Exception as e:
        logger.exception(f"Error connecting to SMTP server: {e}")
        return None


def send_mail(*, email_to: str, subject:str="", html_content:str="")->None:
    server = connect()
    if not server:
        print("SMTP server is not connected. Cannot send email.")
        return
    
    msg = MIMEMultipart()
    msg["From"] = settings.EMAILS_FROM_EMAIL
    msg["To"] = email_to
    msg["Subject"] = subject
    
    msg.attach(MIMEText(html_content, "html"))
    
    try:
        server.send_message(msg)
        logger.info("Email sent successfully!")
    except Exception as e:
        logger.exception(f"Error sending email: {e}")
    finally:
        server.quit()
        
def send_bulk_mail(*, email_to: list[str], subject:str="", html_content:str="")->None:
    server = connect()
    if not server:
        print("SMTP server is not connected. Cannot send email.")
        return
    
    msg = MIMEMultipart()
    msg["From"] = settings.EMAILS_FROM_EMAIL
    msg["Bcc"] = ', '.join(email_to)
    msg["Subject"] = subject
    
    msg.attach(MIMEText(html_content, "html"))
    
    try:
        server.sendmail(msg)
        logger.info("Email sent successfully!")
    except Exception as e:
        logger.exception(f"Error sending email: {e}")
    finally:
        server.quit()
        

def generate_test_email(email_to: str, username:str)->EmailData:

    subject = "Test email"
    html_content = render_email_template(
        template_name="test_email.html",
        context={"email":email_to,
                 "username":username,},
    )
    return EmailData(html_content=html_content, subject=subject)

def generate_register_mail(email_to:str, username:str)->EmailData:
    # project_name = settings.PROJECT_NAME
    subject = "registration successful"
    html_content = render_email_template(
        template_name='new_user_mail.html',
        context={
            "project_name":settings.PROJECT_NAME,
            "username":username,
            "email":email_to,
            #todo: add link to return to login page
        }
    ) 
    return EmailData(html_content=html_content, subject=subject)


def generate_update_status_mail(email_to: str)->EmailData:

    subject = "TodoItem Status Change"
    html_content = render_email_template(
        template_name='update_item_status.html',
        context={
            "project_name":settings.PROJECT_NAME,
            "email":email_to,
        }
    )
    return EmailData(html_content=html_content, subject=subject)

def generate_daily_status_mail(email_to: str, username: str, task_data: List[Dict[str, Any]])->EmailData:
    subject = "Todo reminder"

    html_content = render_email_template(
        template_name="daily_todo_item.html",
        context={
            "project_name":settings.PROJECT_NAME,
            "email":email_to,
            "username": username,
            "task_data": task_data,
        }
    )
    return EmailData(html_content=html_content, subject=subject)

def process_query_result(response_data: List[Dict]) -> List[Dict[str, Any]]:
    """
    This function processes the query result into a list of users, each containing 
    a list of task_data aggregated by category.
    """
    users = defaultdict(lambda: {"email": None, "username": None, "task_data": []})

    for row in response_data:
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