class ERRORS(object):
    from os import remove
    from json import dump, load
    from machine import Pin, deepsleep
    from maintenance import maintenance
    
    # These must be hard-coded to prevent a recursion issue where
    # config_class.py cannot load the config file and throws an error.
    # TODO Do I need this now? I don't think I'm running any errors in 
    # config_class.py. But I am pretty sure I will be soon.
    good_LED = Pin('P10', mode = self.Pin.OUT)
    warn_LED = Pin('P11', mode = self.Pin.OUT)
    error_LED = Pin('P12', mode = self.Pin.OUT)
    
    log = set()
    log_file = '/flash/log.json'
    
    def __init__(self):
        """A class for dealing with different error messages"""
        log = self.load_saved_log()
        global _run_blink
        _run_blink = False
        self._warn_LED_on = False
    
    
    def hard_error(self, message):
        """Called when things get real bad. Stop everything.
        
        Adds the message to the log, saves the log, saves the schedule
        status, stops any LEDs that may be blinking, turns on the error LED,
        stops the watchdog timer, waits one second, and puts the device into
        indefinite deep sleep."""
        from time import sleep
        from main import schedule
        
        self.log.add(message)
        
        self.save_log()
        schedule.save_status()
        
        self.blink_LEDs('stop')
        
        self.good_LED(False)
        self.warn_LED(False)
        self.error_LED(True)
        
        self.wdt.stop()
        
        self.sleep(1)
        
        self.deepsleep()
    
    
    def warning(self, message)
        """Turns on the warning LED and adds the message to the log set"""
        self.maintenance()
        
        self.log.add(message)
        
        global _run_blink
        if not _run_blink:
            self.good_LED(False)
            self.warn_LED(True)
            self.error_LED(False)
        else:
            self._warn_LED_on = True
    
    
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
    
    
    def blink_LEDs(self, command = 'start', LEDs = None, delay = 500):
        """Blink the requested LEDs alternately.

        Usually used to signal important activity.
        
        Send the 'start' or 'stop' command to control the process. Send a list 
        of LEDs ('good', 'warn'. 'error') and it will blink them in the order 
        given. Use a delay in milliseconds to give some delay between blinks, 
        defaults to 500 ms.
        """
        self.maintenance()
        if command == 'start':
            # Multithreading so we can get back to the next step in our process
            from _thread import start_new_thread
            start_new_thread(_blink_LEDs, (LEDs, delay))
        else:
            # TODO A kludge until Pycom fixes _thread.exit() from outside the
            # thread
            global _run_blink
            _run_blink = False
    
    
    def _blink_LEDs(self, LEDs, delay):
        """The actual blink process.
        
        Don't run this directly, use blink_LEDs() instead.
        """
        from time import sleep_ms
        
        all_LEDs = [self.good_LED, self.good_LED, self.good_LED]
        
        # Record the current state of all of our LEDs then turn them all off
        current_LED_states = dict()
        for LED in all_LEDs:
            self.maintenance()
            current_LED_states[LED] = LED.value()
            LED(False)
        
        # TODO What other internal variables do we use elsewhere that are not
        # prepended with underscore?
        global _run_blink
        _run_blink = True
        while _run_blink:
            for LED in LEDs:
                LED(True)
                self.maintenance()
                sleep_ms(delay)
                LED(False)
                self.maintenance()
                sleep_ms(delay)
        
        self.maintenance()

        # Restore our state
        for LED in all_LEDs:
            LED = current_LED_states[LED]
        
        if self._warn_LED_on:
            # We had turned on a warning after blinking began but before it
            # completed, so turn it back on
            self.good_LED(False)
            self.warn_LED(True)
            self.error_LED(False)