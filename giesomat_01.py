import RPi.GPIO as GPIO
import time

from raspberry_gpio_control import init_gpio

#initialize pins
PIN_SENSOR = 24 # later as an array
PIN_PUMP = 23
PIN_VALVE = 22 # later as an array

init_gpio([PIN_SENSOR], [PIN_PUMP, PIN_VALVE])


while True:
    print(GPIO.input(24))
    if GPIO.input(24) == 0:
        # Ausschalten
        GPIO.output(23, GPIO.LOW)
    else:
        # Einschalten
        GPIO.output(23, GPIO.HIGH)
    
    time.sleep(0.5)

'''
for i in range(5):
    GPIO.output(23, GPIO.HIGH)
    time.sleep(0.5)
    GPIO.output(23, GPIO.LOW)
    time.sleep(0.5)
'''


