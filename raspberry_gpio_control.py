import RPi.GPIO as GPIO

def init_gpio(input_pins, output_pins_pump, output_pins_valve):
    #read database and set pins
    #here it is still hard coded
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    
    for pin in input_pins:
        GPIO.setup(pin, GPIO.IN)

     for pin in output_pins_pump:
        GPIO.setup(pin, GPIO.OUT)
        #Initialize Output to High.
        GPIO.output(pin, GPIO.LOW)

    for pin in output_pins_valve:
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