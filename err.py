import sys
import debugging
from rtc import RTC
from os import remove
from leds import leds
from machine import deepsleep
from maintenance import maint
from data_store import DataStore

class ErrCls(object):
    def __init__(self, testing = False, debug = False, debug_level = 0):
        '''A class for dealing with different error messages'''
        maint()
        debugging.enabled = debug
        debugging.default_level = debug_level
        self.debug = debugging.printmsg
        
        # FIXME Remove
        print("debugging.enabled: '" + str(debugging.enabled) + "'")
        print("debugging.default_level: '" + str(debugging.default_level) + "'")
        print("type(self.debug): '" + str(type(self.debug)) + "'")
        print("self.debug: '" + str(self.debug) + "'")
        
        self.testing = testing
        self.rtc = RTC()
        self.log = list()
        self.data_store = DataStore('error_log', testing = testing)
    
    
    def msg(self, mytype, message):
        '''Adds a message of a certain type to the ongoing in-memory log and
        saves it to the data_store
        '''
        # Add the error to the ongoing in-memory log and save to the data_store
        self.debug("In Err.msg(), message: '" + str(message) + "'")
        log_entry = (self.rtc.now(), mytype, {'message': message})
        self.log.append(log_entry)
        return self.data_store.update(log_entry)
    
    
    def warn(self, msg):
        '''Turns on the warning LED, adds the warning to the log set, and saves
        it to the data_store
        '''
        # FIXME Do a code review, ensure I do maint() everywhere
        maint()
        
        # FIXME Remove
        print("debugging.enabled: '" + str(debugging.enabled) + "'")
        print("debugging.default_level: '" + str(debugging.default_level) + "'")
        print("type(self.debug): '" + str(type(self.debug)) + "'")
        print("self.debug: '" + str(self.debug) + "'")
        
        self.debug("self.msg(msg): '" + str(msg) + "'")
        self.msg('warning', msg)
        
        # TODO Not working
        ## Blink for 500 ms, off for 1500 ms, and set this as the default
        #leds.blink(run = True, pattern = (
        #            (self.leds.warn, True, 500),
        #            (self.leds.warn, False, 1500)),
        #            default = True)
        leds.LED('warn', default = True)
    
    
    def err(self, message):
        '''Things got real bad. Stop everything.'''
        from time import sleep
        from main import (schedule, pin_deepsleep_wakeup, wake_pins,
            WAKEUP_ANY_HIGH)
        
        self.msg('error', message)
        
        # FIXME Is that enough time? Maybe wait for a completion flag. But time
        # that out.
        sleep(3)
        
        # Whatever hasn't been sent, save it to flash
        DataStore().save_all()
        
        # Steady red LED
        # TODO Not working
        # TODO The pattern is awkward. See if we can pass only a single pattern
        # by doing some kind of detection.
        #leds.blink(run = True, pattern = ((leds.err, True, None)))
        leds.LED('err', default = True)
        
        # TODO How can I test this as part of a suite?
        if not self.testing:
            wdt.stop()
            pin_deepsleep_wakeup(pins = wake_pins, mode = WAKEUP_ANY_HIGH)
            deepsleep()
    
    
    def exc(self, args = None):
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
        '''
        # TODO Also optionally allow the exception to flow through to stderr
        if args:
            content = args
        
        content['exc_type'] = str(sys.exc_info()[0])
        content['error'] = str(sys.exc_info()[1]).strip()
        
        # TODO And what about the exc_num like in OSError? For now,
        # investigate by hand and later, by allowing an exception argument 
        # to this module.
        
        self.msg('exception', content)
        sys.exit(1)