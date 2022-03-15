import RPi.GPIO as GPIO
import time

from raspberry_gpio_control import init_gpio, setpin_high, setpin_low

#initialize pins
PIN_SENSOR = 24 
PIN_PUMP = 26
PINS_VALVE = [5, 6, 13, 19] #GND => 26 => 19 => 13 => 6 => 5
ID_VALVE = [1,2,3,4] #

TIME = 2 # seconds
TEST_RUNS = 100 # number of test runs

init_gpio([PIN_SENSOR], [PIN_PUMP], [PINS_VALVE])

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


def pump_on():
    setpin_high(PIN_PUMP)
    return

def pump_off():
    setpin_low(PIN_PUMP)
    return

def open_valve(valve_id):
    setpin_low(PINS_VALVE[valve_id-1]) #set pin low because of opocoupler
    return

def close_valve(valve_id):
    setpin_high(PINS_VALVE[valve_id-1]) #set pin low because of opocoupler
    return





