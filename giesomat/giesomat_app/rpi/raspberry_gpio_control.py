#Import RPI libraries when running on target. Import test utilities when running on computer.
try:
    import RPi.GPIO as GPIO
except ImportError:
     from .test_utility import GPIO

def init_gpio(input_pins, output_pins):
    #read database and set pins
    #here it is still hard coded
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    
    for pin in input_pins:
        GPIO.setup(pin, GPIO.IN)

    for pin in output_pins:
        GPIO.setup(pin, GPIO.OUT)
        #Initialize Output to High.
        GPIO.output(pin, GPIO.HIGH)


def setpin_high(pin_id):
    GPIO.output(pin_id, GPIO.HIGH)
    return

def setpin_low(pin_id):
    GPIO.output(pin_id, GPIO.LOW)
    return

def read_pin(pin_id):
    value = GPIO.input(pin_id)
    return value