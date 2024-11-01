from typing import Any
from pathlib import Path
from .core.config import settings
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
        server.send_message(msg)
        logger.info("Email sent successfully!")
    except Exception as e:
        logger.exception(f"Error sending email: {e}")
    finally:
        server.quit()
        
def generate_test_email(email_to: str)->EmailData:
    subject = "Test email"
    html_content = render_email_template(
        template_name="test_email.html",
        context={"email":email_to},
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