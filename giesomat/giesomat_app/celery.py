import os
from celery import Celery
import django
from django.conf import settings
from django.apps import apps 


#Hier sind noch 2 weitere Optionen:
#https://localcoder.org/celery-auto-discovery-does-not-find-tasks-module-in-app

#Funktionierendes Beispiel auf Git:
#https://github.com/Reymond190/django-celery-myex

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'giesomat.settings')
#os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'giesomat_app.settings')
#settings.configure()
#django.setup()
#settings.configure()
#Rabbit MQ Broker is configured in overall settings.
app = Celery('giesomat_app')
#app = Celery('giesomat')


app.config_from_object('django.conf:settings', namespace='CELERY')

#Load task modules from all registered Django apps
app.autodiscover_tasks()
#app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
#app.autodiscover_tasks(lambda: [n.name for n in apps.get_app_configs()])


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
