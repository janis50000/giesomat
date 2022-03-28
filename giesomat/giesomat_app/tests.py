from django.test import TestCase

#Imports for the State Machine Tests
from .models import Plant
from django_fsm import TransitionNotAllowed

#Import for the RPI Tests
from .rpi.raspberry_gpio_control import setpin_high, setpin_low, read_pin

#Imports for the Celery Beat Tests
from django.test import TransactionTestCase, SimpleTestCase
from .tasks import read_plant_humidity, water_all_thirsty_plants, make_plants_thirsty_on_schedule
from celery.contrib.testing.worker import start_worker
from .celery import app as celery_app


'''
class PlantStateMachineTests(TestCase):

    #3 States => 3^2 state transitions possible = 9 test cases

    #Test allowed transitions
    def test_initial_state_initiated(self):
        plant = create_plant("Test Plant")
        self.assertEqual(plant.current_status, Plant.PLANT_STATE_HAPPY)

    def test_happy_to_happy_state(self):
        plant = create_plant("Test Plant")
        plant.is_happy()
        self.assertEqual(plant.current_status, Plant.PLANT_STATE_HAPPY)

    def test_happy_to_thirsty_state(self):
        plant = create_plant("Test Plant")
        plant.is_thirsty()
        self.assertEqual(plant.current_status, Plant.PLANT_STATE_THIRSTY)

    def test_thirsty_to_thirsty_state(self):
        plant = create_plant("Test Plant")
        plant.is_thirsty() #a plant gets always initalized in happy state.
        plant.is_thirsty()
        self.assertEqual(plant.current_status, Plant.PLANT_STATE_THIRSTY)

    def test_happy_to_watered_state(self):
        plant = create_plant("Test Plant")
        plant.is_thirsty() #a plant gets always initalized in happy state.
        plant.is_watered()
        self.assertEqual(plant.current_status, Plant.PLANT_STATE_WATERED)

    def test_watered_to_thirsty_state(self):
        plant = create_plant("Test Plant")
        plant.is_thirsty() #a plant gets always initalized in happy state.
        plant.is_watered()
        plant.is_still_thirsty()
        self.assertEqual(plant.current_status, Plant.PLANT_STATE_THIRSTY)

    def test_full_state_transition(self):
        plant = create_plant("Test Plant")
        plant.is_thirsty() #a plant gets always initalized in happy state.
        plant.is_watered()
        plant.is_happy()
        self.assertEqual(plant.current_status, Plant.PLANT_STATE_HAPPY)

    #Test forbidden transitions
    def test_happy_to_watered_state(self):
        plant = create_plant("Test Plant")
        self.assertRaises(TransitionNotAllowed, plant.is_watered)

    def test_thirsty_to_happy_state(self):
        plant = create_plant("Test Plant")
        plant.is_thirsty()
        self.assertRaises(TransitionNotAllowed, plant.is_happy)

    def test_watered_to_watered_state(self):
        plant = create_plant("Test Plant")
        plant.is_thirsty() #a plant gets always initalized in happy state.
        plant.is_watered()
        self.assertRaises(TransitionNotAllowed, plant.is_watered)

def create_plant(plant_name):
    return Plant.objects.create(plant_name=plant_name)

class GpioTests(TestCase):
    def test_rpi_test_utility_for_pin_high(self):
        setpin_high(5)
        self.assertEqual(1,1)

    def test_rpi_test_utility_for_pin_low(self):
        setpin_low(5)
        self.assertEqual(1,1)

    def test_rpi_test_utility_for_read_pin_even(self):
        self.assertEqual(read_pin(2),0)

    def test_rpi_test_utility_for_read_pin_odd(self):
        self.assertEqual(read_pin(3),1000)

'''

#class CeleryBeatTaskTests(TransactionTestCase):

class CeleryBeatTaskTests(SimpleTestCase):
    databases = '__all__'

    
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.celery_worker = start_worker(celery_app, perform_ping_check=False)
        cls.celery_worker.__enter__()

    @classmethod
    def tearDownClass(cls):
        super.tearDownClass()
        cls.celery_worker.__exit__(None,None,None)

    '''
    def test_setUp(self):
        super.setUp()
        self.task = read_plant_humidity
        self.results = self.task.get()
    '''

    '''
    def test_setUp2(self):
        super.setUp()
        self.task = read_plant_humidity
        self.results = self.task.get()
        self.assertEqual(self.task.status, "blabla")
    '''

    def test_my_task(self):
        read_plant_humidity('bla', 'bla').delay()

    '''
    def test(self):
        #self.assertEqual(self.read_plant_humidity.state, "SUCCESS")
        self.assertEqual(self.task.state, "SUCCESS")
    '''

    #This works from a test perspective but throws errors:
    '''
    def test_another_test(self):
        #Given
        #settings.CELERY_TASK_ALWAYS_EAGER = True
        task = read_plant_humidity('bla', 'bla')
        results = task.get()
        self.assertEqual(task.status, "SUCCESS")
    '''


#ToDo: Test Cases for Celery Tasks:
#https://www.reddit.com/r/django/comments/npe8ny/how_to_unit_test_a_simple_celerybeat_healthcheck/
#https://www.distributedpython.com/2018/05/01/unit-testing-celery-tasks/
