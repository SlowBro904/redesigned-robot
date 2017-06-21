class ERRORS(object):
    from machine import Pin, deepsleep
    from time import sleep
    from wdt import wdt

    def __init__(self, config):
        self.config     = config
        self.good_LED   = self.Pin(self.config['GOOD_LED_PIN'],  mode = self.Pin.OUT)
        self.warn_LED   = self.Pin(self.config['WARN_LED_PIN'],  mode = self.Pin.OUT)
        self.error_LED  = self.Pin(self.config['ERROR_LED_PIN'], mode = self.Pin.OUT)
        self.warnings   = set()
    
    
    def hard_error(self):
        """ Turns on the error LED, waits one second, stops the watchdog timer, and puts the device into indefinite deep sleep. """
        self.good_LED(False)
        self.warn_LED(False)
        self.error_LED(True)
        self.sleep(1)
        # TODO Can I combine?
        self.wdt.feeder().stop()
        self.wdt.stop()
        self.deepsleep()
    
    
    def warning(self, message)
        """ Turns on the warning LED and adds the message to the warning set """
        if not self.warn_LED:
            self.good_LED(False)
            self.warn_LED(True)
        
        self.warnings.add(warning)