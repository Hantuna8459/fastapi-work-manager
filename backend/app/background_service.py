from asyncio import run
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger   
from backend.app.utils import send_daily_email

# Set up the scheduler
scheduler = BackgroundScheduler()
trigger = CronTrigger(hour=17, minute=0)
scheduler.add_job(lambda:run (send_daily_email()), trigger)

    