class GPIO():
    IN = 1
    OUT = 0
    BCM = 'TEST_CONSTANT'
    HIGH = 1
    LOW = 0

    def setwarnings(bool_param):
        return

    def setmode(bcm):
        return
    
    def setup(pin, gpio_mode):
        return
    
    def output(pin, value):
        return
    
    def input(pin):
        #some logic to enable test cases
        if(pin % 2 ) == 0:
            return 0 # return 0 for even pins
        else:
            return 1000 #return 1000 for odd pins

        return

    def cleanup():
        return