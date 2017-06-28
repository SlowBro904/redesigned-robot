class ERRORS(object):
    from machine import Pin, deepsleep
    from wdt import wdt
    
    def __init__(self):
        """ A class for dealing with different error messages """
        # These must be hard-coded to prevent a recursion issue where config_class.py cannot load the config file and throws an error.
        # TODO Convert this file to a class file then create another file which is just config.py with these values.
        self.good_LED = self.Pin(10, mode = self.Pin.OUT)
        self.warn_LED = self.Pin(11, mode = self.Pin.OUT)
        self.error_LED = self.Pin(12, mode = self.Pin.OUT)
        self.warnings = set()
    
    
    def hard_error(self):
        """ Turns on the error LED, waits one second, stops the watchdog timer, and puts the device into indefinite deep sleep. """
        from time import sleep
        
        self.good_LED(False)
        self.warn_LED(False)
        self.error_LED(True)
        
        self.wdt.feed()
        
        self.sleep(1)
        
        self.wdt.stop()
        
        # Indefinite sleep
        self.deepsleep()
    
    
    def warning(self, message)
        """ Turns on the warning LED and adds the message to the warning set """
        if not self.warn_LED:
            self.good_LED(False)
            self.warn_LED(True)
        
        self.wdt.feed()
        
        self.warnings.add(warning)
    
    
    def clear_warnings(self):
        """ Clear our warnings """
        self.wdt.feed()
        self.warnings = set()
    
    
    def process_warnings(self):
        """ If we have anything in self.warnings process it. Show a warning LED and send an alert to the cloud. """
        # TODO If we have a lack of ping we may want to show that in the web console
        self.wdt.feed()
        pass # FIXME Finish