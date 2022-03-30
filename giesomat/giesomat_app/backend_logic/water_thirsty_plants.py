from ..models import Plant, PlantTechnical, Pump, Valve, PlantHistoryWater
from .giesomat_utility import pump_on, pump_off, open_valve, close_valve
from django.utils import timezone
import time


def water_thirsty_plants():
    measurement_pks = []
    #Get all thirsty plants that are active.
    plants_to_water = Plant.objects.exclude(is_active=False).filter(current_status=Plant.PLANT_STATE_THIRSTY)
    for plant in plants_to_water:
        #Do the state transition first. This will throw an error if it is not legitimate.
        plant.is_watered()
        plant.save()
        measurement_pk = water_plant_entry(plant)

        measurement_pks.append(measurement_pk)

    return measurement_pks

def water_plant_entry(plant):
    water_volume = 0
    #Get all plant technicals for the plant.
    plant_technicals = PlantTechnical.objects.filter(plant=plant.pk) #Should be 1:1 but technically can be 1:n
    for plant_technical in plant_technicals:
        #Get pump and valve for the plant technical.
        pump = Pump.objects.get(pk=plant_technical.pump.pk)
        valve = Valve.objects.get(pk=plant_technical.valve.pk)
        #create pump time if there are multiple plant technicals.
        #pump_time = pump_time_seconds (plant.water_need/plant_technicals.count() , pump.water_flow_per_minute)
        pump_time = pump_time_seconds (plant.water_need/len(plant_technicals) , pump.water_flow_per_minute)
        water_volume = water_volume + (pump_time*pump.water_flow_per_minute/60)
        water_plant(pump_time, pump, valve)
    
    measurement_pk = add_measurement(plant, water_volume, timezone.now())
    return measurement_pk

def pump_time_seconds(water_need, water_flow_per_minute):
    return water_need / water_flow_per_minute * 60

def water_plant(pump_time, pump, valve):
    pump_on(pump.gpio_pin)
    open_valve(valve.gpio_pin)
    #wait...
    time.sleep(int(pump_time))
    #Done watering
    pump_off(pump.gpio_pin)
    #Wait to flush the remaining water from the piping/valve
    time.sleep(int(valve.time_offset))
    close_valve(valve.gpio_pin)
    return

def add_measurement(plant, water_volume, timestamp):
        measurement = PlantHistoryWater.objects.create(plant=plant, water_volume = water_volume, timestamp = timestamp)
        return measurement.pk