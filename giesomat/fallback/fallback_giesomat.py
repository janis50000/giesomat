import RPi.GPIO as GPIO
import time

from raspberry_gpio_control import init_gpio
from giesomat_utility import pump_on, pump_off, open_valve, close_valve


GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)


#Hard code, while init script is still buggy.
PIN_PUMP = 26
#PINS_VALVE = [19, 13, 6, 5] #GND => 26 => 19 => 13 => 6 => 5 (left to right in RPI)
PINS_VALVE = [19]

## Jans Pin Config:
#Pump: 26
#Valve 1: 19
#Valve 2: 13
#Valve 3: 6
#Valve 4: 5


init_gpio([], [PIN_PUMP, PINS_VALVE])

TIME = 10 # seconds
GIESOMAT_RUNS = 1 # number of test runs

water_need = 100 #ml
water_flow_per_minute = 600 #ml

pump_time_per_plant = water_need/water_flow_per_minute * 60

i = 0

while i< GIESOMAT_RUNS:

    pump_on(PIN_PUMP)    

    for valve in PINS_VALVE:
        open_valve(valve)
        time.sleep(pump_time_per_plant)
        close_valve(valve)
        
    pump_off(PIN_PUMP)
    time.sleep(TIME)
    i = i +1

