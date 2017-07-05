class ERRORS(object):
    from machine import Pin, deepsleep
    from wdt import wdt
    from json import dump, load
    from os import remove
    
    # These must be hard-coded to prevent a recursion issue where config_class.py cannot load the config file and throws an error.
    # TODO Convert this file to a class file then create another file which is just config.py with these values.
    good_LED = self.Pin(10, mode = self.Pin.OUT)
    warn_LED = self.Pin(11, mode = self.Pin.OUT)
    error_LED = self.Pin(12, mode = self.Pin.OUT)
    warnings = set()
    warnings_file = '/flash/warnings.json'

    def __init__(self):
        """ A class for dealing with different error messages """
        warnings = self.load_saved_warnings()
    
    
    def hard_error(self):
        """ Turns on the error LED, waits one second, stops the watchdog timer, and puts the device into indefinite deep sleep. """
        from time import sleep
        
        self.good_LED(False)
        self.warn_LED(False)
        self.error_LED(True)
        
        self.wdt.stop()
        self.sleep(1)
        
        # Indefinite sleep
        self.deepsleep()
    
    
    def warning(self, message)
        """ Turns on the warning LED and adds the message to the warning set """
        if not self.warn_LED:
            self.good_LED(False)
            self.warn_LED(True)
        
        self.wdt.feed()
        
        self.warnings.add(warning)
    
    
    def save_warnings(self):
        """ If we cannot connect to the cloud, let's save the warnings to flash for next time we can connect. """
        self.wdt.feed()
        
        with open(self.warnings_file, 'w') as json_data:
            if not dump(self.warnings, json_data):
                return False
    
    
    def load_saved_warnings(self):
        """ Load the warnings from flash and delete the file. """
        self.wdt.feed()
        
        warnings = list()
        
        with open(self.warnings_file) as json_data:
            warnings = self.load(json_data)
        
        # Only delete the save file if we were successful
        if warnings:
            self.clear_saved_warnings()
        
        return warnings
    
    
    def clear_saved_warnings(self):
        """ Delete the saved warnings file """
        self.wdt.feed()
        return self.remove(self.warnings_file)
    
    
    def clear_warnings(self):
        """ Remove all warnings """
        self.wdt.feed()
        self.warnings = set()
        self.clear_saved_warnings()
    
    
    def flash_yellow_red_start(self):
        """ Flash the yellow and red LEDs alternately to signal important activity """
        # Multithreading so we can get back to the next step in our process
        from _thread import start_new_thread
        start_new_thread(_daemon, ())
    
    
    def flash_yellow_red_stop(self):
        """ Stop flashing the yellow and red LEDs alternately """
        # TODO A kludge until Pycom fixes _thread.exit() from outside the thread
        global run_yellow_red_flash
        run_yellow_red_flash = False
    
    
    def _flash_yellow_red(self):
        """ The actual flashing process. Don't run this directly; use flash_yellow_red_start() instead. """
        from time import sleep
        
        # Start state
        self.good_LED(False)
        self.warn_LED(True)
        self.error_LED(True)
        
        global run_yellow_red_flash
        run_yellow_red_flash = True
        while run_yellow_red_flash:
            sleep(1)
            self.warn_LED.toggle()
            self.error_LED.toggle()