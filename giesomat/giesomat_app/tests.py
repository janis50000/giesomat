from django.test import TestCase

#Imports for the State Machine Tests
from .models import Plant, Pump, Valve, PlantTechnical
from django_fsm import TransitionNotAllowed

#Import for the RPI Tests
from .rpi.raspberry_gpio_control import setpin_high, setpin_low, read_pin

#Imports for the Celery Beat Tests
from django.test import TransactionTestCase, SimpleTestCase
from .tasks import read_plant_humidity, water_all_thirsty_plants, make_plants_thirsty_on_schedule
from celery.contrib.testing.worker import start_worker
from .celery import app as celery_app


#Imports for Backend Logic Tests
from .backend_logic.make_plants_thirsty import make_plants_thirsty
from .backend_logic.water_thirsty_plants import water_thirsty_plants, water_plant


class PlantStateMachineTests(TestCase):

    #3 States => 3^2 state transitions possible = 9 test cases

    #Test allowed transitions
    def test_initial_state_initiated(self):
        plant = create_plant(plant_name = "Test Plant", water_mode = Plant.WATER_MODE_HUMIDITY)
        self.assertEqual(plant.current_status, Plant.PLANT_STATE_HAPPY)

    def test_happy_to_happy_state(self):
        plant = create_plant(plant_name = "Test Plant", water_mode = Plant.WATER_MODE_HUMIDITY)
        plant.is_happy()
        self.assertEqual(plant.current_status, Plant.PLANT_STATE_HAPPY)

    def test_happy_to_thirsty_state(self):
        plant = create_plant(plant_name = "Test Plant", water_mode = Plant.WATER_MODE_HUMIDITY)
        plant.is_thirsty()
        self.assertEqual(plant.current_status, Plant.PLANT_STATE_THIRSTY)

    def test_thirsty_to_thirsty_state(self):
        plant = create_plant(plant_name = "Test Plant", water_mode = Plant.WATER_MODE_HUMIDITY)
        plant.is_thirsty() #a plant gets always initalized in happy state.
        plant.is_thirsty()
        self.assertEqual(plant.current_status, Plant.PLANT_STATE_THIRSTY)

    def test_happy_to_watered_state(self):
        plant = create_plant(plant_name = "Test Plant", water_mode = Plant.WATER_MODE_HUMIDITY)
        plant.is_thirsty() #a plant gets always initalized in happy state.
        plant.is_watered()
        self.assertEqual(plant.current_status, Plant.PLANT_STATE_WATERED)

    def test_watered_to_thirsty_state(self):
        plant = create_plant(plant_name = "Test Plant", water_mode = Plant.WATER_MODE_HUMIDITY)
        plant.is_thirsty() #a plant gets always initalized in happy state.
        plant.is_watered()
        plant.is_still_thirsty()
        self.assertEqual(plant.current_status, Plant.PLANT_STATE_THIRSTY)

    def test_full_state_transition(self):
        plant = create_plant(plant_name = "Test Plant", water_mode = Plant.WATER_MODE_HUMIDITY)
        plant.is_thirsty() #a plant gets always initalized in happy state.
        plant.is_watered()
        plant.is_happy()
        self.assertEqual(plant.current_status, Plant.PLANT_STATE_HAPPY)

    #Test forbidden transitions
    def test_happy_to_watered_state(self):
        plant = create_plant(plant_name = "Test Plant", water_mode = Plant.WATER_MODE_HUMIDITY)
        self.assertRaises(TransitionNotAllowed, plant.is_watered)

    def test_thirsty_to_happy_state(self):
        plant = create_plant(plant_name = "Test Plant", water_mode = Plant.WATER_MODE_HUMIDITY)
        plant.is_thirsty()
        self.assertRaises(TransitionNotAllowed, plant.is_happy)

    def test_watered_to_watered_state(self):
        plant = create_plant(plant_name = "Test Plant", water_mode = Plant.WATER_MODE_HUMIDITY)
        plant.is_thirsty() #a plant gets always initalized in happy state.
        plant.is_watered()
        self.assertRaises(TransitionNotAllowed, plant.is_watered)

def create_plant(plant_name, water_mode):
    return Plant.objects.create(plant_name=plant_name, water_mode = water_mode)

def read_plant(plant_id):
    return Plant.objects.get(pk=plant_id)


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

class BackendTestsMakePlantsThirsty(TestCase):
    #ToDo: Plant not active

    def test_make_plants_thirsty_no_plant(self):
        plant = create_plant(plant_name = "Test Plant gets thirsty", water_mode = Plant.WATER_MODE_HUMIDITY)
        make_plants_thirsty()
        updated_plant = read_plant(plant.pk)
        print(updated_plant.current_status)
        self.assertEqual(updated_plant.current_status, Plant.PLANT_STATE_HAPPY)

    def test_make_plants_thirsty(self):
        plant = create_plant(plant_name = "Test Plant gets thirsty", water_mode = Plant.WATER_MODE_CYCLICAL)
        make_plants_thirsty()
        updated_plant = read_plant(plant.pk)
        print(updated_plant.current_status)
        self.assertEqual(updated_plant.current_status, Plant.PLANT_STATE_THIRSTY)

    def test_make_three_plants_thirsty(self):
        plant1 = create_plant(plant_name = "Test Plant gets thirsty", water_mode = Plant.WATER_MODE_CYCLICAL)
        plant2 = create_plant(plant_name = "Test Plant 2 gets thirsty", water_mode = Plant.WATER_MODE_CYCLICAL)
        plant3 = create_plant(plant_name = "Test Plant 2 gets thirsty", water_mode = Plant.WATER_MODE_CYCLICAL)

        make_plants_thirsty()

        updated_plant2 = read_plant(plant2.pk)
        updated_plant1 = read_plant(plant1.pk)
        updated_plant3 = read_plant(plant3.pk)

        self.assertEqual(updated_plant1.current_status, Plant.PLANT_STATE_THIRSTY)
        self.assertEqual(updated_plant2.current_status, Plant.PLANT_STATE_THIRSTY)
        self.assertEqual(updated_plant3.current_status, Plant.PLANT_STATE_THIRSTY)


    def test_make_one_plant_thirsty_one_not(self):
        plant1 = create_plant(plant_name = "Test Plant gets thirsty", water_mode = Plant.WATER_MODE_CYCLICAL)
        plant2 = create_plant(plant_name = "Test Plant 2 gets thirsty", water_mode = Plant.WATER_MODE_CYCLICAL)
        plant2.is_thirsty()
        plant2.save()

        make_plants_thirsty()

        updated_plant2 = read_plant(plant2.pk)
        updated_plant1 = read_plant(plant1.pk)

        self.assertEqual(updated_plant1.current_status, Plant.PLANT_STATE_THIRSTY)
        self.assertEqual(updated_plant2.current_status, Plant.PLANT_STATE_THIRSTY)

class BackendTestsWaterPlants(TestCase):
    #def test_smoke_tests(self):
        #Plant not active
        #No valve
        #no pump
        #no plant technical
        #some values are missing
        #...
        #ToDo

        #Multiple Plant Technicals
        #Test duration

    def test_water_plant_no_data(self):
        water_need = 500
        plant = create_full_plant(plant_name = "Test Plant", water_mode = Plant.WATER_MODE_CYCLICAL, is_active= True, water_need = water_need)
        self.assertRaises(Exception, water_plant(plant))
 
    '''
    #This Test tests water_thirsty_plants()
    def test_water_plant_not_active(self):
        water_need = 500
        plant = create_full_plant(plant_name = "Test Plant", water_mode = Plant.WATER_MODE_CYCLICAL, is_active= False, water_need = water_need)
        plant.is_thirsty()
        plant.save()
        pump= create_pump(1, 5000000) #Some high value to speed up the tests.
        valve = create_valve(2, 0)
        create_plant_technical(plant, None, pump, valve)

        #result = water_plant(plant)

        self.assertEqual(result.water_amount,0)
    '''
    #This Test Case is still not working. THere is something wrong with the for loop.
    def test_water_plant_multiple_plant_technicals(self):
        water_need = 500
        plant = create_full_plant(plant_name = "Test Plant", water_mode = Plant.WATER_MODE_CYCLICAL, is_active= True, water_need = water_need)
        plant.is_thirsty()
        plant.save()
        pump= create_pump(1, 5000000) #Some high value to speed up the tests.
        pump2= create_pump(1, 5000000) #Some high value to speed up the tests.

        valve = create_valve(2, 0)
        create_plant_technical(plant, None, pump, valve)
        create_plant_technical(plant, None, pump2, valve)
        create_plant_technical(plant, None, pump, valve)
        create_plant_technical(plant, None, pump, valve)
        create_plant_technical(plant, None, pump, valve)

        result = water_plant(plant)

        self.assertEqual(result.water_amount,water_need)

    def test_water_plant_happy_path(self):
        water_need = 500
        plant = create_full_plant(plant_name = "Test Plant", water_mode = Plant.WATER_MODE_CYCLICAL, is_active= True, water_need = water_need)
        plant.is_thirsty()
        plant.save()
        pump= create_pump(1, 5000000) #Some high value to speed up the tests.
        valve = create_valve(2, 0)
        create_plant_technical(plant, None, pump, valve)

        result = water_plant(plant)

        self.assertEqual(result.water_amount,water_need)

def create_pump(gpio_pin, water_flow_per_minute):
    return Pump.objects.create(gpio_pin= gpio_pin, water_flow_per_minute=water_flow_per_minute)

def create_valve(gpio_pin, time_offset):
    return Valve.objects.create(gpio_pin=gpio_pin, time_offset=time_offset)

#def create_sensor(gpio_pin, )

def create_plant_technical(plant, sensor, pump, valve):
    return PlantTechnical.objects.create(plant=plant, sensor=sensor, pump=pump, valve=valve)

def create_full_plant(plant_name, water_mode,is_active, water_need):
    return Plant.objects.create(plant_name=plant_name, water_mode = water_mode, is_active=is_active, water_need=water_need)

'''
#This is a full integration test. Make sure that rabbitMQ server runs on your system.
#Connection refused error => The rabbitMQ server is not running.
class CeleryBeatTaskTests(TransactionTestCase):
    databases = '__all__'

    
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.celery_worker = start_worker(celery_app, perform_ping_check=False)
        cls.celery_worker.__enter__()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        cls.celery_worker.__exit__(None,None,None)

#This is a full integration test. Make sure that rabbitMQ server runs on your system.
#Connection refused error => The rabbitMQ server is not running.
    def test_task_read_plant_humidity(self):
        result = read_plant_humidity.delay()
        print(result.state)
        self.assertEqual(result.state, "SUCCESS")

    def test_task_water_all_thirsty_plants(self):
        result = water_all_thirsty_plants.delay()
        print(result.state)
        self.assertEqual(result.state, "SUCCESS")

    def test_task_make_plants_thirsty_on_schedule(self):
        result = make_plants_thirsty_on_schedule.delay()
        print(result.state)
        self.assertEqual(result.state, "SUCCESS")
'''