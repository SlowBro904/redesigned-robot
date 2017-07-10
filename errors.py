class ERRORS(object):
    from os import remove
    from json import dump, load
    from machine import Pin, deepsleep
    from maintenance import maintenance
    
    # These must be hard-coded to prevent a recursion issue where
    # config_class.py cannot load the config file and throws an error.
    # TODO Do I need this now? I don't think I'm running any errors in 
    # config_class.py. But I am pretty sure I will be soon.
    good_LED = Pin(10, mode = self.Pin.OUT)
    warn_LED = Pin(11, mode = self.Pin.OUT)
    error_LED = Pin(12, mode = self.Pin.OUT)
    
    warnings = set()
    warnings_file = '/flash/warnings.json'

    def __init__(self):
        """ A class for dealing with different error messages """
        warnings = self.load_saved_warnings()
    
    
    def hard_error(self):
        """ Turns on the error LED, waits one second, stops the watchdog timer,
        and puts the device into indefinite deep sleep. """
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
        
        self.maintenance()
        
        self.warnings.add(warning)
    
    
    def save_warnings(self):
        """If we cannot connect to the cloud, let's save the warnings to flash
        for next time we can connect.
        """
        self.maintenance()
        
        with open(self.warnings_file, 'w') as json_data:
            if not dump(self.warnings, json_data):
                return False
    
    
    def load_saved_warnings(self):
        """ Load the warnings from flash and delete the file. """
        self.maintenance()
        
        warnings = list()
        
        with open(self.warnings_file) as json_data:
            warnings = self.load(json_data)
        
        # Only delete the save file if we were successful
        if warnings:
            self.clear_saved_warnings()
        
        return warnings
    
    
    def clear_saved_warnings(self):
        """ Delete the saved warnings file """
        self.maintenance()
        return self.remove(self.warnings_file)
    
    
    def clear_warnings(self):
        """ Remove all warnings """
        self.maintenance()
        self.warnings = set()
        self.clear_saved_warnings()
    
    
    def flash_LEDs(self, LEDs, command = 'stop', delay = 1):
        """Flash the requested LEDs alternately to signal important activity.
        
        Send a list of LEDs ('good', 'warn'. 'error') and it will flash them in
        the order given. Send the 'start' or 'stop' command to control the 
        process. Defaults to stop. Use a delay to give some delay between 
        flashes, defaults to 1 second.
        """
        self.maintenance()
        if command == 'start':
            # Multithreading so we can get back to the next step in our process
            from _thread import start_new_thread
            start_new_thread(_flash_LEDs, (LEDs, delay))
        else:
            # TODO A kludge until Pycom fixes _thread.exit() from outside the
            # thread
            global run_flash
            run_flash = False
    
    
    def _flash_LEDs(self, LEDs, delay):
        """The actual flashing process.
        
        Don't run this directly, use flash_LEDs() instead.
        """
        from time import sleep
        
        all_LEDs = [self.good_LED, self.good_LED, self.good_LED]
        
        # Record the current state of all of our LEDs then turn them all off
        current_LED_states = dict()
        for LED in all_LEDs:
            self.maintenance()
            current_LED_states[LED] = LED.value()
            LED(False)
        
        global run_flash
        run_flash = True
        while run_flash:
            for LED in LEDs:
                LED(True)
                self.maintenance()
                sleep(delay)
                LED(False)
        
        self.maintenance()

        # Restore our state
        for LED in all_LEDs:
            LED = current_LED_states[LED]