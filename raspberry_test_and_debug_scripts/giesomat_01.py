import RPi.GPIO as GPIO
import time

from raspberry_gpio_control import init_gpio, setpin_high, setpin_low

#initialize pins
PIN_SENSOR = 24 
PIN_PUMP = 26
PINS_VALVE = [5, 6, 13, 19] #GND => 26 => 19 => 13 => 6 => 5
ID_VALVE = [1,2,3,4] #

init_gpio([PIN_SENSOR], [PIN_PUMP], [PIN_VALVE])


while True:
    print(GPIO.input(24))
    if GPIO.input(24) == 0:
        # Ausschalten
        GPIO.output(23, GPIO.LOW)
    else:
        # Einschalten
        GPIO.output(23, GPIO.HIGH)
    
    time.sleep(0.5)



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





