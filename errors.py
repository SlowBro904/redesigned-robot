class Errors(object):
    import sys
    from os import remove
    from machine import deepsleep
    
    try:
        from leds import leds
        from json import dump, load
        from maintenance import maintenance
    except ImportError:
        # Ignore if testing
        pass
    
    log = set()
    log_file = '/flash/errors.json'
    exceptions_log_file = '/flash/exceptions.log'
    
    def __init__(self):
        """A class for dealing with different error messages"""
        self.log = self.load_saved_log()
    
    
    def hard_error(self, message):
        """Called when things get real bad. Stop everything.
        
        Adds the message to the log, if possible to upload the log and schedule
        status it does, if not it saves the log and schedule status, stops any 
        LEDs that may be blinking, turns on the error LED, stops the watchdog 
        timer, waits three seconds, and puts the device into indefinite deep
        sleep."""
        from time import sleep
        from cloud import cloud
        # TODO Should I move these object instantiations into another file? To
        # decouple from main.py.
        from main import (schedule, pin_deepsleep_wakeup, wake_pins,
            WAKEUP_ANY_HIGH)
        
        self.log.add(message)
        
        if cloud.send('log', self.log):
            self.clear_log()
        else:
            self.save_log()
        
        if cloud.send('schedule_status', schedule.status):
            schedule.clear_status()
        else:
            schedule.save_status()
        
        # Steady red LED
        self.leds.blink(run = True, pattern = ((self.leds.err, True, None)))
        
        self.wdt.stop()
        
        self.sleep(3)
        
        pin_deepsleep_wakeup(pins = wake_pins, mode = WAKEUP_ANY_HIGH)
        
        self.deepsleep()
    
    
    def warning(self, message):
        """Turns on the warning LED and adds the message to the log set"""
        self.maintenance()
        
        self.log.add(message)
        
        # Blink for 500 ms, off for 1500 ms, and set this as the default
        self.leds.blink(run = True, pattern = (
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
        # FIXME Uncomment
        #self.maintenance()
        
        log = set()
        
        try:
            with open(self.log_file) as json_data:
                log = self.load(json_data)
        except OSError:
            # Ignore if it doesn't exist
            pass
        
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

    
    def log_exception(self, **kwargs):
        """Log uncaught exceptions.
        
        Ugly but necessary, since Pycom's WiPy 2.0 (as of version 1.7.6.b1) 
        doesn't seem to have a working sys.print_exception() and sys.excepthook
        is completely missing from all MicroPython implementations.
        
        kwargs is a dict that can optionally include:
        myfile: The file name such as __file__
        myclass: The class name such as self.__class__.__name__
        myfunc: The function we are in such as '__init__'
        myaction: A human-readable string describing the action we were taking
            such as "Testing exception logging"
        log_file: Change the log file from the default (/flash/exceptions.log)
        """
        # TODO Also optionally allow the exception to flow through to stderr
        
        exceptions_log_file = self.exceptions_log_file
        if kwargs is not None:
            if 'log_file' in kwargs:
                exceptions_log_file = kwargs['log_file']
        
        with open(exceptions_log_file, 'a') as exceptions_log:
            exceptions_log.write('-'*79 + '\n')
            if kwargs is not None:
                if 'myfile' in kwargs:
                    myfile = str(kwargs['myfile'])
                    exceptions_log.write('File: ' + myfile + '\n')
                
                if 'myclass' in kwargs:
                    myclass = str(kwargs['myclass'])
                    exceptions_log.write('Class: ' + myclass + '\n')        
                
                if 'myfunc' in kwargs:
                    myfunc = str(kwargs['myfunc'])
                    exceptions_log.write('Function: ' + myfunc + '\n')
                
                if 'myaction' in kwargs:
                    myaction = str(kwargs['myaction'])
                    exceptions_log.write('Action: ' + myaction + '\n')
            
            exc_type = str(self.sys.exc_info()[0])
            error = str(self.sys.exc_info()[1]).strip()
            
            exceptions_log.write('Exception type: ' + exc_type + '\n')
            exceptions_log.write('Exception error text: ' + error + '\n')
            # TODO And what about the exc_num like in OSError? For now,
            # investigate by hand and later, by allowing an exception argument 
            # to this module.
        self.sys.exit(1)