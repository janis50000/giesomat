CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 30 * 60

CELERY_TASK_ALWAYS_EAGER = True
CELERY_BROKER_URL = "amqp://guest:guest@localhost"
CELERY_IMPORTS = ('giesomat_app.tasks',)

CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'