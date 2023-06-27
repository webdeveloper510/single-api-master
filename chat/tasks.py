from celery.schedules import crontab

from celery import shared_task

import datetime
from .models import Chat
from Admin.models import Setting
from chat import celery_module




@shared_task(run_every=(crontab(minute=0, hour='*/1')))
def check_chat_reminder():
    return "success", celery_module.check_chat_reminder()


@shared_task(run_every=(crontab(minute='*/5')))
def check_chat_active():
    return "success", celery_module.check_chat_active()


@shared_task(run_every=(crontab(minute='*/5')))
def check_chat_push():
    return "success", celery_module.check_chat_push()

