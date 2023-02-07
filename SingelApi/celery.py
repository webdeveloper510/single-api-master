import os
from celery import Celery

__author__ = ""

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SingelApi.settings')

app = Celery('app_rama')

CELERY_TIMEZONE = 'IST'

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()
