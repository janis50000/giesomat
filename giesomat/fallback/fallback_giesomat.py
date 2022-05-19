import RPi.GPIO as GPIO
import time

from raspberry_gpio_control import init_gpio
from giesomat_utility import pump_on, pump_off, open_valve, close_valve


GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)


#Hard code, while init script is still buggy.
PIN_PUMP = 26
#PINS_VALVE = [19, 13, 6, 5] #GND => 26 => 19 => 13 => 6 => 5 (left to right in RPI)
PINS_VALVE = [19,6,5]

## Jans Pin Config:
#Pump: 26
#Valve 1: 19
#Valve 2: 13
#Valve 3: 6
#Valve 4: 5


init_gpio([], [PIN_PUMP, PINS_VALVE])

TIME = 60*60*12 # seconds - twice a day
GIESOMAT_RUNS = 1 # number of runs

water_need = 250 #ml
water_flow_per_minute = 3000 #ml 10 seconds for 500 ml => 3l

#pump_time_per_plant = water_need/water_flow_per_minute * 60
pump_time_per_plant = 8 #currently it is 10 seconds but that is too long. should be 2 times 6 seconds (it takes a bit more than one second until water is in at the valves)
j=0

#while True:
while j< GIESOMAT_RUNS:
    i = 0
    pump_on(PIN_PUMP)    

    for valve in PINS_VALVE:
        open_valve(valve)
        if i==0:
            time.sleep(pump_time_per_plant*1.2)
        else:
            time.sleep(pump_time_per_plant)
        close_valve(valve)
        i = i +1
    pump_off(PIN_PUMP)
    time.sleep(TIME)
    

