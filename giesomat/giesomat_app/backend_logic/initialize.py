from ..models import Sensor, Pump, Valve, PlantTechnical,Plant
from ..rpi.raspberry_gpio_control import init_gpio


def initialize_hardware():
    input_pins = []
    output_pins = []
    plants_to_initialize = Plant.objects.exclude(is_active=False)
    for plant in plants_to_initialize:
        print(plant)
        plant_technicals = PlantTechnical.objects.filter(plant=plant.pk) #Should be 1:1 but technically can be 1:n
        plant_output_pins = get_plant_output_pins(plant_technicals)
        output_pins.append(plant_output_pins)
        plant_input_pins = get_plant_input_pins(plant_technicals)
        input_pins.append(plant_input_pins)

    init_gpio(input_pins,output_pins)

def get_plant_output_pins(plant_technicals):
    output_pins = []

    for plant_technical in plant_technicals:
        pump = Pump.objects.get(pk=plant_technical.pump.pk)
        output_pins.append(pump.gpio_pin)
        valve = Valve.objects.get(pk=plant_technical.valve.pk)
        output_pins.append(valve.gpio_pin)
    return(output_pins)

def get_plant_input_pins(plant_technicals):
    input_pins = []

    for plant_technical in plant_technicals:
        sensor = Sensor.objects.get(pk=plant_technical.sensor.pk)
        input_pins.append(sensor.gpio_pin)
    return(input_pins)