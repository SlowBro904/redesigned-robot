class Errors(object):
    import sys
    from os import remove
    from datastore import DataStore
    
    try:
        from leds import leds
        from json import dump, load
        from machine import deepsleep
        from maintenance import maintenance
    except ImportError:
        # Testing
        pass
    
    
    def __init__(self):
        '''A class for dealing with different error messages'''
        datastore = self.DataStore('error_log')
        self.log = set()
    
    
    def timestamp(self):
        '''Returns a datetime.now() object, whether we're on the WiPy or a
        desktop
        '''
        try:
            from machine import RTC
            rtc = self.RTC()
            datetime = rtc.datetime()
        except ImportError:
            # For testing on a desktop
            from datetime import datetime
        
        return datetime.now()
    
    
    def error(self, message):
        '''Things got real bad. Stop everything.'''
        from time import sleep
        
        from main import (schedule, pin_deepsleep_wakeup, wake_pins,
            WAKEUP_ANY_HIGH)
        
        # Add the error to the ongoing in-memory log and save to the datastore
        log_entry = (self.timestamp(), 'error', {'message': message})
        self.log.add(log_entry)
        self.datastore.update(log_entry)
        self.DataStore().save_all()
                
        # Steady red LED
        # TODO The pattern is awkward. See if we can pass only a single pattern
        # by doing some kind of detection.
        self.leds.blink(run = True, pattern = ((self.leds.err, True, None)))
        
        self.wdt.stop()
        
        self.sleep(3)
        
        pin_deepsleep_wakeup(pins = wake_pins, mode = WAKEUP_ANY_HIGH)
        
        self.deepsleep()
    
    
    def warning(self, message):
        '''Turns on the warning LED, adds the warning to the log set, and saves
        it to the datastore
        '''
        self.maintenance()
        
        log_entry = (self.timestamp(), 'warning', {'message': message})
        self.log.add(log_entry)
        self.datastore.update(log_entry)
        
        # Blink for 500 ms, off for 1500 ms, and set this as the default
        self.leds.blink(run = True, pattern = (
                        (self.leds.warn, True, 500),
                        (self.leds.warn, False, 1500)),
                        default = True)
    
    
    # FIXME Everywhere I use self. in defaults, remove the self.
    def exception(self, args = None):
        '''Log uncaught exceptions.
        
        Ugly but necessary, since Pycom's WiPy 2.0 (as of version 1.7.6.b1) 
        doesn't seem to have a working sys.print_exception() and sys.excepthook
        is completely missing from all MicroPython implementations.
        
        args is a dict that can optionally include:
        'file': The file name such as __file__
        'class': The class name such as self.__class__.__name__
        'func': The function we are in such as '__init__'
        'action': A human-readable string describing the action we were taking
            such as "Testing exception logging"
        'log_file': Change the log file from the default
        '''
        # TODO Also optionally allow the exception to flow through to stderr
        if args:
            content = args
        
        content['exc_type'] = str(self.sys.exc_info()[0])
        content['error'] = str(self.sys.exc_info()[1]).strip()
        
        # TODO And what about the exc_num like in OSError? For now,
        # investigate by hand and later, by allowing an exception argument 
        # to this module.
        
        log_entry = (self.timestamp(), 'exception', content)
        self.log.add(log_entry)
        self.datastore.update(log_entry)
        
        self.sys.exit(1)