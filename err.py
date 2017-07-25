class Err(object):
    import sys
    from rtc import RTC
    from os import remove
    from leds import leds
    from json import dump, load
    from machine import deepsleep
    from datastore import DataStore
    from maintenance import maint
    
    
    def __init__(self, datastore = None):
        '''A class for dealing with different error messages'''
        self.rtc = RTC()
        self.log = list()
        if not datastore:
            datastore = self.DataStore('error_log')
    
    
    def log_entry(self, mytype, content):
        '''Returns a log entry tuple'''
        # Needed for testing
        return (self.rtc.now(), mytype, content)
    
    
    def message(self, mytype, message):
        '''Adds a message of a certain type to the ongoing in-memory log and
        saves it to the datastore
        '''
        # FIXME This won't work yet
        # Add the error to the ongoing in-memory log and save to the datastore
        self.log.append(self.log_entry(mytype = mytype,
                        content = {'message': message}))
        return self.datastore.update(log_entry)
    
    
    def warning(self, message):
        '''Turns on the warning LED, adds the warning to the log set, and saves
        it to the datastore
        '''
        # FIXME Do a code review, ensure I do maint() everywhere
        self.maint()
        
        self.message('warning', message)
        
        # Blink for 500 ms, off for 1500 ms, and set this as the default
        self.leds.blink(run = True, pattern = (
                        (self.leds.warn, True, 500),
                        (self.leds.warn, False, 1500)),
                        default = True)
    
    
    def error(self, message):
        '''Things got real bad. Stop everything.'''
        from time import sleep
        from main import (schedule, pin_deepsleep_wakeup, wake_pins,
            WAKEUP_ANY_HIGH)
        
        self.message('error', message)
        self.datastore.update(log_entry)
        
        # FIXME Is that enough time?
        sleep(3)
        
        # Whatever hasn't been sent, save it to flash
        self.DataStore().save_all()
        
        # Steady red LED
        # TODO The pattern is awkward. See if we can pass only a single pattern
        # by doing some kind of detection.
        self.leds.blink(run = True, pattern = ((self.leds.err, True, None)))
        self.wdt.stop()
        pin_deepsleep_wakeup(pins = wake_pins, mode = WAKEUP_ANY_HIGH)
        self.deepsleep()
    
    
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
        
        log_entry = (self.rtc.now(), 'exception', content)
        self.log.append(log_entry)
        self.datastore.update(log_entry)
        
        self.sys.exit(1)