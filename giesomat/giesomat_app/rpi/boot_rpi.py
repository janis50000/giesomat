import RPi.GPIO as GPIO

def boot_rpi():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)