import os
from celery import Celery
#from celery.schedules import crontab
from django.conf import settings


#Rabbit MQ Broker is configured in overall settings.
app = Celery('giesomat_app')


app.config_from_object('django.conf:settings', namespace='CELERY')

#Load task modules from all registered Django apps
app.autodiscover_tasks()