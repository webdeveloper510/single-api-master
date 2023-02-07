from celery.task.schedules import crontab
from celery.decorators import periodic_task
import datetime
from .models import Chat
from Admin.models import Setting
from chat import celery_module




@periodic_task(run_every=(crontab(minute=0, hour='*/1')))
def check_chat_reminder():
    return "success", celery_module.check_chat_reminder()


@periodic_task(run_every=(crontab(minute='*/5')))
def check_chat_active():
    return "success", celery_module.check_chat_active()


@periodic_task(run_every=(crontab(minute='*/5')))
def check_chat_push():
    return "success", celery_module.check_chat_push()

