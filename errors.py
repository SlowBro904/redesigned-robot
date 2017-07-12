class ERRORS(object):
    from os import remove
    from leds import leds
    from json import dump, load
    from machine import deepsleep
    from maintenance import maintenance
    
    log = set()
    log_file = '/flash/log.json'
    
    def __init__(self):
        """A class for dealing with different error messages"""
        log = self.load_saved_log()
    
    
    def hard_error(self, message):
        """Called when things get real bad. Stop everything.
        
        Adds the message to the log, saves the log, saves the schedule
        status, stops any LEDs that may be blinking, turns on the error LED,
        stops the watchdog timer, waits three seconds, and puts the device into
        indefinite deep sleep."""
        from time import sleep
        from main import schedule
        
        self.log.add(message)
        
        self.save_log()
        schedule.save_status()
        
        # Steady red LED
        self.leds.blink('start', pattern = ((self.leds.err, True, None)))
        
        self.wdt.stop()
        
        self.sleep(3)
        
        self.deepsleep()
    
    
    def warning(self, message)
        """Turns on the warning LED and adds the message to the log set"""
        self.maintenance()
        
        self.log.add(message)
        
        # Blink for 500 ms, off for 1500 ms, and set this as the default
        self.leds.blink(command = 'start', pattern = (
                        (self.leds.warn, True, 500),
                        (self.leds.warn, False, 1500)
                        ), default = True)
    
    
    def save_log(self):
        """If we cannot connect to the cloud, let's save the log to flash for 
        next time we can connect.
        """
        # We don't want to always save the log because that causes more writes 
        # to the flash, which has a limited life. Only save when we cannot
        # connect, or have a hard error.
        self.maintenance()
        
        with open(self.log_file, 'w') as json_data:
            if not dump(self.log, json_data):
                return False
    
    
    def load_saved_log(self):
        """Load the log from flash and delete the file"""
        self.maintenance()
        
        log = set()
        
        with open(self.log_file) as json_data:
            log = self.load(json_data)
        
        # Only delete the save file if we were successful
        if log:
            self.clear_saved_log()
        
        return log
    
    
    def clear_saved_log(self):
        """Delete the saved log file"""
        self.maintenance()
        return self.remove(self.log_file)
    
    
    def clear_log(self):
        """Remove the log both from memory and flash"""
        self.maintenance()
        self.log = set()
        self.clear_saved_log()