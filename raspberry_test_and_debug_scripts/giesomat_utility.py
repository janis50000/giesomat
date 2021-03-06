
from raspberry_gpio_control import setpin_high, setpin_low

PIN_PUMP = 26
PINS_VALVE = [19, 13, 6, 5] #GND => 26 => 19 => 13 => 6 => 5 (left to right in RPI)

#ID_VALVE = [1,2,3,4] #


def pump_on():
    setpin_low(PIN_PUMP)
    return

def pump_off():
    setpin_high(PIN_PUMP)
    return

def open_valve(valve_id):
    setpin_low(PINS_VALVE[valve_id-1]) #set pin low because of opocoupler
    return

def close_valve(valve_id):
    setpin_high(PINS_VALVE[valve_id-1]) #set pin low because of opocoupler
    return





