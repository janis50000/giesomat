import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.OUT)
GPIO.setup(24, GPIO.IN)

while True:
    if GPIO.input(24) == 0:
        # Ausschalten
        #GPIO.output(23, GPIO.LOW)
        GPIO.output(23, GPIO.HIGH)
    else:
        # Einschalten
        #GPIO.output(23, GPIO.HIGH)
        GPIO.output(23, GPIO.LOW)

'''
for i in range(5):
    GPIO.output(23, GPIO.HIGH)
    time.sleep(0.5)
    GPIO.output(23, GPIO.LOW)
    time.sleep(0.5)
'''


