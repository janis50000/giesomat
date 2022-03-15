import RPi.GPIO as GPIO
import time

from raspberry_gpio_control import init_gpio
from giesomat_utility import pump_on, pump_off, open_valve, close_valve


#initialize pins
PIN_SENSOR = 24 
PIN_PUMP = 26
PINS_VALVE = [19, 13, 6, 5] #GND => 26 => 19 => 13 => 6 => 5 (left to right in RPI)
ID_VALVE = [1,2,3,4] #

TIME = 2 # seconds
TEST_RUNS = 100 # number of test runs

init_gpio([PIN_SENSOR], [PIN_PUMP, PINS_VALVE])

i = 0

while i<= TEST_RUNS:

    pump_on()    
    time.sleep(TIME)
    pump_off()

    for valve in ID_VALVE:
        open_valve(valve)
        time.sleep(TIME)
        close_valve(valve)

    i = i +1





