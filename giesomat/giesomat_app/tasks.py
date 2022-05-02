from celery import shared_task
from .backend_logic.make_plants_thirsty import make_plants_thirsty
from celery import app



#ToDo Jan: Add 3 tasks: Read sensors, water plants based on sensor values and water plants based on schedule

#@shared_task(name="read_plant_humidity", bind=True, default_retry_delay=300, max_retries=3)
@shared_task(name="read_plant_humidity", bind=True, default_retry_delay=300, max_retries=3)
def read_plant_humidity(self):
    try:
        print("Read plant humidity.")
        return

    except Exception:
        read_plant_humidity.retry()


@shared_task(name="water_all_thirsty_plants", bind=True, default_retry_delay=300, max_retries=3)
def water_all_thirsty_plants(self):
    try:
        print("Water plants based on humidity.")
        return

    except Exception:
        water_all_thirsty_plants.retry()


@shared_task(name="make_plants_thirsty_on_schedule", bind=True, default_retry_delay=300, max_retries=3)
def make_plants_thirsty_on_schedule(self):
    try:
        make_plants_thirsty()
        print("Water plants based on schedule.")
        return

    except Exception:
        make_plants_thirsty_on_schedule.retry()