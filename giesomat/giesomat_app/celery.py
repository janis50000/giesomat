import os
from celery import Celery
#from celery.schedules import crontab

#Default Settings
app = Celery('giesomat_app')

app.config_from_object('django.conf:settings', namespace='CELERY')

#Load task modules from all registered Django apps
app.autodiscover_tasks()