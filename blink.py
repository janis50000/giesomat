import RPi.GPIO as GPIO
import time
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.OUT)
GPIO.output(23, GPIO.HIGH)
time.sleep(0.5)
GPIO.output(23, GPIO.LOW)
time.sleep(0.5)



