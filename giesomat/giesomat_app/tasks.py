from celery import shared_task
from .backend_logic.make_plants_thirsty import make_plants_thirsty
from .backend_logic.water_thirsty_plants import water_thirsty_plants

#from giesomat_app.celery import app

#@shared_task(name="read_plant_humidity", bind=True, default_retry_delay=300, max_retries=3)
#@app.task(name="read_plant_humidity", bind=True, default_retry_delay=300, max_retries=3)
@shared_task(name="read_plant_humidity", bind=True, default_retry_delay=300, max_retries=3)
def read_plant_humidity(self):
    try:
        #ToDo
        print("Read plant humidity.")
        return

    except Exception:
        read_plant_humidity.retry()


@shared_task(name="water_all_thirsty_plants", bind=True, default_retry_delay=300, max_retries=3)
def water_all_thirsty_plants(self):
    try:
        water_thirsty_plants()
        return

    except Exception:
        water_all_thirsty_plants.retry()


@shared_task(name="make_plants_thirsty_on_schedule", bind=True, default_retry_delay=300, max_retries=3)
def make_plants_thirsty_on_schedule(self):
    try:
        make_plants_thirsty()
        return

    except Exception:
        make_plants_thirsty_on_schedule.retry()