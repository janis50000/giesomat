from ..models import Plant, PlantTechnical, Pump, Valve
import types
#from types import SimpleNamespace
from .giesomat_utility import pump_on, pump_off, open_valve, close_valve

from django.utils import timezone
import time
#debug imports
import json
from django.core import serializers

def water_thirsty_plants():
    #ToDo: Only Active Plants!
    plants_to_water = Plant.objects.exclude(is_active=False).filter(current_status=Plant.PLANT_STATE_THIRSTY)
    for plant in plants_to_water:
        #Do the state transition first. This will throw an error if it is not legitimate.
        plant.is_watered()
        plant.save()
        results= water_plant(plant)

        #ToDo: Record Results
    return


def water_plant(plant):

    try:
        result_set = types.SimpleNamespace()
        result_set.pump_time_seconds = 0
        result_set.water_amount = 0
        plant_technicals = PlantTechnical.objects.filter(plant=plant.pk) #Should be 1:1 but technically can be 1:n
        #print(json.dumps(plant_technicals))
        print(plant_technicals)
        #print(str(plant_technicals))

        #count_plant_technicals = plant_technicals.count() 
        #print(plant_technicals.count() )
        #water_need = plant.water_need/ count_plant_technicals #Get specific water need if there is more than one pum/valve assigned for a plant.
        if plant_technicals.exists():
            count_plant_technicals = plant_technicals.count() 
            print(plant_technicals.count() )
            water_need = plant.water_need/ count_plant_technicals #Get specific water need if there is more than one pum/valve assigned for a plant.

            for plant_technical in plant_technicals.iterator():
                #print(plant_technical)
                print(plant_technical.pk)
                #Fetch all data
                pump = Pump.objects.get(pk=plant_technical.pump.pk)
                valve = Valve.objects.get(pk=plant_technical.valve.pk)
                result_set.timestamp = timezone.now()
                pump_time = pump_time_seconds (plant.water_need, pump.water_flow_per_minute)
                result_set.pump_time_seconds = result_set.pump_time_seconds + pump_time

                #water the plant
                pump_on(pump.gpio_pin)
                open_valve(valve.gpio_pin)
                #wait...
                time.sleep(pump_time)
                #Done watering
                pump_off(pump.gpio_pin)
                #Wait to flush the remaining water from the piping/valve
                time.sleep(valve.time_offset)
                close_valve(valve.gpio_pin)
                result_set.water_amount = result_set.water_amount + water_need
                print(result_set.water_amount)
                return result_set
    except:
    #except AttributeError:
        return 
    #except TypeError:
    #    return     

def pump_time_seconds(water_need, water_flow_per_minute):
    return water_need / water_flow_per_minute * 60