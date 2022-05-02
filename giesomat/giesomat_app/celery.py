import os
from celery import Celery
import django
#from celery.schedules import crontab
from django.conf import settings

#os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'giesomat_app.celeryconfig')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'giesomat_app.settings')

#django.setup()

#app = Celery('tasks', broker='amqp://guest@localhost//')

#Rabbit MQ Broker is configured in overall settings.
app = Celery('giesomat_app')

#app.config_from_object('giesomat_app.celeryconfig')
app.config_from_object('django.conf:settings', namespace='CELERY')

#Load task modules from all registered Django apps
#app.autodiscover_tasks()
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)



if __name__ == '__main__':
    app.start()