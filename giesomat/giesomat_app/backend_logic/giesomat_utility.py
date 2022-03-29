from ..rpi.raspberry_gpio_control import setpin_high, setpin_low, read_pin

def pump_on(pump_gpio):
    setpin_low(pump_gpio)
    return

def pump_off(pump_gpio):
    setpin_high(pump_gpio)
    return

def open_valve(valve_gpio):
    setpin_low(valve_gpio) #set pin low because of opocoupler
    return

def close_valve(valve_gpio):
    setpin_high(valve_gpio) #set pin low because of opocoupler
    return

def read_sensor(sensor_gpio):
    return read_pin(sensor_gpio)
