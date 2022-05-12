import RPi.GPIO as GPIO
from raspberry_gpio_control import init_gpio

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)


#Hard code, while init script is still buggy.
PIN_PUMP = 26
PINS_VALVE = [19, 13, 6, 5] #GND => 26 => 19 => 13 => 6 => 5 (left to right in RPI)


init_gpio([], [PIN_PUMP, PINS_VALVE])