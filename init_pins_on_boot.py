#sudo nano /etc/rc.local
#python /home/giesomat/init_pins_on_boot.py


import RPi.GPIO as GPIO
import time

from raspberry_gpio_control import init_gpio

#initialize pins
PIN_SENSOR = 24 
PIN_PUMP = 26
PINS_VALVE = [19, 13, 6, 5] #GND => 26 => 19 => 13 => 6 => 5 (left to right in RPI)

TEST_RUNS = 100 # number of test runs

init_gpio([PIN_SENSOR], [PIN_PUMP, PINS_VALVE])