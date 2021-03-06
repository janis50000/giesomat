from django.test import TestCase

#Imports for the State Machine Tests
from .models import Plant, Pump, Valve, PlantTechnical, PlantHistoryWater,Sensor
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
from .backend_logic.water_thirsty_plants import water_thirsty_plants,water_plant_entry, water_plant, add_measurement
from .backend_logic.initialize import initialize_hardware, get_plant_output_pins, get_plant_input_pins


from django.utils import timezone




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

class PlantHistoryWaterTests(TestCase):
    def test_create_measurement(self):
        water_need = 500
        plant = create_full_plant(plant_name = "Test Plant", water_mode = Plant.WATER_MODE_CYCLICAL, is_active= True, water_need = water_need)
        now = timezone.now()
        water_volume = 100
        measurement_pk = add_measurement(plant, water_volume, now)

        #plant.add_measurement(plant=plant, timestamp = now, water_volume= water_volume)
        measurement_read = PlantHistoryWater.objects.get(pk=measurement_pk)
        self.assertEqual(plant, measurement_read.plant)

class BackendTestsWaterPlants(TestCase):

    def test_water_plant_no_data(self):
        water_need = 500
        plant = create_full_plant(plant_name = "Test Plant", water_mode = Plant.WATER_MODE_CYCLICAL, is_active= True, water_need = water_need)
        self.assertRaises(Exception, water_plant_entry(plant))

    def test_water_thirsty_plants_no_data(self):
        measurement_pks = water_thirsty_plants()
        self.assertEquals(len(measurement_pks), 0)
        self.assertEquals(measurement_pks,[])            

    def test_water_thirsty_plants_none_is_Active(self):
        water_need1 = 500
        plant1 = create_full_plant(plant_name = "Test Plant1", water_mode = Plant.WATER_MODE_CYCLICAL, is_active= False, water_need = water_need1)
        plant1.is_thirsty()
        plant1.save()
        pump= create_pump(1, 5000000) #Some high value to speed up the tests.
        valve1 = create_valve(2, 0)
        create_plant_technical(plant1, None, pump, valve1)
        water_need2 = 1000
        plant2 = create_full_plant(plant_name = "Test Plant2", water_mode = Plant.WATER_MODE_CYCLICAL, is_active= False, water_need = water_need2)
        plant2.is_thirsty()
        plant2.save()
        valve2 = create_valve(2, 0)
        create_plant_technical(plant2, None, pump, valve2)

        measurement_pks = water_thirsty_plants()
        self.assertEquals(len(measurement_pks), 0)
        self.assertEquals(measurement_pks,[])            
     
    
    def test_water_one_thirsty_plants_happy_path(self):
        water_need = 500
        plant = create_full_plant(plant_name = "Test Plant", water_mode = Plant.WATER_MODE_CYCLICAL, is_active= True, water_need = water_need)
        plant.is_thirsty()
        plant.save()
        pump= create_pump(1, 5000000) #Some high value to speed up the tests.
        valve = create_valve(2, 0)
        create_plant_technical(plant, None, pump, valve)

        measurement_pks = water_thirsty_plants()
        self.assertEquals(len(measurement_pks), 1)

        for measurement_pk in measurement_pks:
            measurement_read = PlantHistoryWater.objects.get(pk=measurement_pk)

            self.assertEquals(water_need,measurement_read.water_volume)            
        
    def test_water_two_thirsty_plants_happy_path(self):
        water_need1 = 500
        plant1 = create_full_plant(plant_name = "Test Plant1", water_mode = Plant.WATER_MODE_CYCLICAL, is_active= True, water_need = water_need1)
        plant1.is_thirsty()
        plant1.save()
        pump= create_pump(1, 5000000) #Some high value to speed up the tests.
        valve1 = create_valve(2, 0)
        create_plant_technical(plant1, None, pump, valve1)
        water_need2 = 1000
        plant2 = create_full_plant(plant_name = "Test Plant2", water_mode = Plant.WATER_MODE_CYCLICAL, is_active= True, water_need = water_need2)
        plant2.is_thirsty()
        plant2.save()
        valve2 = create_valve(2, 0)
        create_plant_technical(plant2, None, pump, valve2)

        measurement_pks = water_thirsty_plants()
        self.assertEquals(len(measurement_pks), 2)

        measurement_read1 = PlantHistoryWater.objects.get(pk=measurement_pks[0])
        self.assertEquals(water_need1,measurement_read1.water_volume)            
        measurement_read2 = PlantHistoryWater.objects.get(pk=measurement_pks[1])
        self.assertEquals(water_need2,measurement_read2.water_volume)        

    def test_water_two_thirsty_plants_two_plant_technicals(self):
        water_need1 = 500
        plant1 = create_full_plant(plant_name = "Test Plant1", water_mode = Plant.WATER_MODE_CYCLICAL, is_active= True, water_need = water_need1)
        plant1.is_thirsty()
        plant1.save()
        pump= create_pump(1, 5000000) #Some high value to speed up the tests.
        valve1 = create_valve(2, 0)
        create_plant_technical(plant1, None, pump, valve1)
        create_plant_technical(plant1, None, pump, valve1)
        water_need2 = 1000
        plant2 = create_full_plant(plant_name = "Test Plant2", water_mode = Plant.WATER_MODE_CYCLICAL, is_active= True, water_need = water_need2)
        plant2.is_thirsty()
        plant2.save()
        valve2 = create_valve(2, 0)
        create_plant_technical(plant2, None, pump, valve2)
        create_plant_technical(plant1, None, pump, valve1)

        measurement_pks = water_thirsty_plants()
        self.assertEquals(len(measurement_pks), 2)

        measurement_read1 = PlantHistoryWater.objects.get(pk=measurement_pks[0])
        self.assertEquals(water_need1,measurement_read1.water_volume)            
        measurement_read2 = PlantHistoryWater.objects.get(pk=measurement_pks[1])
        self.assertEquals(water_need2,measurement_read2.water_volume)        


    def test_water_two_thirsty_plants_one_is_switched_off(self):
        water_need1 = 500
        plant1 = create_full_plant(plant_name = "Test Plant1", water_mode = Plant.WATER_MODE_CYCLICAL, is_active= True, water_need = water_need1)
        plant1.is_thirsty()
        plant1.save()
        pump= create_pump(1, 5000000) #Some high value to speed up the tests.
        valve1 = create_valve(2, 0)
        create_plant_technical(plant1, None, pump, valve1)
        water_need2 = 1000
        plant2 = create_full_plant(plant_name = "Test Plant2", water_mode = Plant.WATER_MODE_CYCLICAL, is_active= False, water_need = water_need2)
        plant2.is_thirsty()
        plant2.save()
        valve2 = create_valve(2, 0)
        create_plant_technical(plant2, None, pump, valve2)

        measurement_pks = water_thirsty_plants()
        self.assertEquals(len(measurement_pks), 1)

        measurement_read1 = PlantHistoryWater.objects.get(pk=measurement_pks[0])
        self.assertEquals(water_need1,measurement_read1.water_volume)            

    def test_water_plant_multiple_plant_technicals(self):
        water_need = 500
        plant = create_full_plant(plant_name = "Test Plant", water_mode = Plant.WATER_MODE_CYCLICAL, is_active= True, water_need = water_need)
        #plant.is_thirsty()
        #plant.save()
        pump= create_pump(1, 5000000) #Some high value to speed up the tests.
        pump2= create_pump(1, 5000000) #Some high value to speed up the tests.

        valve = create_valve(2, 0)
        create_plant_technical(plant, None, pump, valve)
        create_plant_technical(plant, None, pump2, valve)
        create_plant_technical(plant, None, pump, valve)
        create_plant_technical(plant, None, pump, valve)
        create_plant_technical(plant, None, pump, valve)

        measurement_pk = water_plant_entry(plant)
        measurement_read = PlantHistoryWater.objects.get(pk=measurement_pk)

        self.assertEquals(water_need,measurement_read.water_volume)

    def test_water_plant_happy_path(self):
        water_need = 500
        plant = create_full_plant(plant_name = "Test Plant", water_mode = Plant.WATER_MODE_CYCLICAL, is_active= True, water_need = water_need)
        #plant.is_thirsty()
        #plant.save()
        pump= create_pump(1, 5000000) #Some high value to speed up the tests.
        valve = create_valve(2, 0)
        create_plant_technical(plant, None, pump, valve)
        measurement_pk = water_plant_entry(plant)
        measurement_read = PlantHistoryWater.objects.get(pk=measurement_pk)

        self.assertEquals(water_need,measurement_read.water_volume)

    def test_water_plant_plain(self):
        pump= create_pump(1, 5000000) #Some high value to speed up the tests.
        valve = create_valve(2, 0)
        water_plant(0.01, pump, valve)
        self.assertEqual(1,1)        #NO nice assert but I just want to see that there is no error. 


class BackendTestsInitialize(TestCase):
    def test_get_plant_output_pins_one_plant(self):
        water_need = 500
        plant = create_full_plant(plant_name = "Test Plant", water_mode = Plant.WATER_MODE_CYCLICAL, is_active= True, water_need = water_need)
        pump= create_pump(1, 5000000) #Some high value to speed up the tests.
        valve = create_valve(2, 0)
        plant_technical = create_plant_technical(plant, None, pump, valve)
        plant_technicals = PlantTechnical.objects.filter(pk = plant_technical.pk) #Should be 1:1 but technically can be 1:n
        output_pins = get_plant_output_pins(plant_technicals)
        self.assertIn('1',''.join(str(e) for e in output_pins))
        self.assertIn('2',','.join(str(e) for e in output_pins))

    def test_get_plant_output_pins_two_plants(self):
        water_need = 500
        plant = create_full_plant(plant_name = "Test Plant", water_mode = Plant.WATER_MODE_CYCLICAL, is_active= True, water_need = water_need)
        pump1= create_pump(1, 5000000) #Some high value to speed up the tests.
        valve1 = create_valve(999, 0)
        plant_technical1 = create_plant_technical(plant, None, pump1, valve1)
        pump2= create_pump(1111, 5000000) #Some high value to speed up the tests.
        valve2 = create_valve(2, 0)
        plant_technical2 = create_plant_technical(plant, None, pump2, valve2)
        plant_technicals = PlantTechnical.objects.filter(plant = plant.pk) #Should be 1:1 but technically can be 1:n
        output_pins = get_plant_output_pins(plant_technicals)
        self.assertIn('1',''.join(str(e) for e in output_pins))
        self.assertIn('2',''.join(str(e) for e in output_pins))
        self.assertIn('999',''.join(str(e) for e in output_pins))
        self.assertIn('111',''.join(str(e) for e in output_pins))

    def test_get_plant_input_pins_one_plant(self):
        water_need = 500
        plant = create_full_plant(plant_name = "Test Plant", water_mode = Plant.WATER_MODE_CYCLICAL, is_active= True, water_need = water_need)
        sensor = create_sensor(1, 5000000,5000000,5000000) #Some high value to speed up the tests.
        plant_technical = create_plant_technical(plant, sensor, None, None)
        plant_technicals = PlantTechnical.objects.filter(pk = plant_technical.pk) #Should be 1:1 but technically can be 1:n
        input_pins = get_plant_input_pins(plant_technicals)
        self.assertIn('1',''.join(str(e) for e in input_pins))

    def test_get_plant_input_pins_two_plants(self):
        water_need = 500
        plant = create_full_plant(plant_name = "Test Plant", water_mode = Plant.WATER_MODE_CYCLICAL, is_active= True, water_need = water_need)
        sensor1 = create_sensor(1, 5000000,5000000,5000000) #Some high value to speed up the tests.
        plant_technical1 = create_plant_technical(plant, sensor1, None, None)
        sensor2 = create_sensor(999, 5000000,5000000,5000000) #Some high value to speed up the tests.
        plant_technical2 = create_plant_technical(plant, sensor2, None, None)
        plant_technicals = PlantTechnical.objects.filter(plant = plant.pk) #Should be 1:1 but technically can be 1:n
        input_pins = get_plant_input_pins(plant_technicals)
        self.assertIn('1',''.join(str(e) for e in input_pins))
        self.assertIn('999',''.join(str(e) for e in input_pins))

    def test_initialize_one_plant(self):
        water_need = 500
        plant = create_full_plant(plant_name = "Test Plant", water_mode = Plant.WATER_MODE_CYCLICAL, is_active= True, water_need = water_need)
        sensor1 = create_sensor(1, 5000000,5000000,5000000) #Some high value to speed up the tests.
        pump1= create_pump(2, 5000000) #Some high value to speed up the tests.
        valve1 = create_valve(3, 0)
        plant_technical1 = create_plant_technical(plant, sensor1, pump1, valve1)
        #plant_technicals = PlantTechnical.objects.filter(plant = plant.pk) #Should be 1:1 but technically can be 1:n
        initialize_hardware()
        self.assertEqual(1,1) #test if no error is thrown, checked with print() during programming

    def test_initialize_two_plants(self):
        water_need = 500
        plant1 = create_full_plant(plant_name = "Test Plant1", water_mode = Plant.WATER_MODE_CYCLICAL, is_active= True, water_need = water_need)
        sensor1 = create_sensor(1, 5000000,5000000,5000000) #Some high value to speed up the tests.
        pump1= create_pump(2, 5000000) #Some high value to speed up the tests.
        valve1 = create_valve(3, 0)
        plant_technical1 = create_plant_technical(plant1, sensor1, pump1, valve1)
        plant2 = create_full_plant(plant_name = "Test Plant2", water_mode = Plant.WATER_MODE_CYCLICAL, is_active= True, water_need = water_need)
        sensor2 = create_sensor(1, 5000000,5000000,5000000) #Some high value to speed up the tests.
        pump2= create_pump(2, 5000000) #Some high value to speed up the tests.
        valve2 = create_valve(3, 0)
        plant_technical1 = create_plant_technical(plant2, sensor2, pump2, valve2)
        #plant_technicals = PlantTechnical.objects.filter(plant = plant.pk) #Should be 1:1 but technically can be 1:n
        initialize_hardware()
        self.assertEqual(1,1) #test if no error is thrown, checked with print() during programming


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



def create_pump(gpio_pin, water_flow_per_minute):
    return Pump.objects.create(gpio_pin= gpio_pin, water_flow_per_minute=water_flow_per_minute)

def create_valve(gpio_pin, time_offset):
    return Valve.objects.create(gpio_pin=gpio_pin, time_offset=time_offset)

def create_plant_technical(plant, sensor, pump, valve):
    return PlantTechnical.objects.create(plant=plant, sensor=sensor, pump=pump, valve=valve)

def create_full_plant(plant_name, water_mode,is_active, water_need):
    return Plant.objects.create(plant_name=plant_name, water_mode = water_mode, is_active=is_active, water_need=water_need)

def create_plant(plant_name, water_mode):
    return Plant.objects.create(plant_name=plant_name, water_mode = water_mode)

def read_plant(plant_id):
    return Plant.objects.get(pk=plant_id)

def create_sensor(gpio_pin, max_sensor_value, min_sensor_value,sensor_threshold):
    return Sensor.objects.create(gpio_pin= gpio_pin, max_sensor_value=max_sensor_value, min_sensor_value=min_sensor_value, sensor_threshold=sensor_threshold)
