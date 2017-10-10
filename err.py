import sys
import debugging
from os import remove
from leds import leds
from maintenance import maint
from deepsleep import deepsleep
from data_store import DataStore

debug = debugging.printmsg
testing = debugging.testing

debug("Testing debug()")

class ErrCls(object):
    def __init__(self):
        '''A class for dealing with different error messages'''
        maint()
        debug("ErrCls __init__() start")
        
        self.log = list()
        self.data_store = DataStore('error_log')
        self.data_store.testing = self.testing
        debug("ErrCls __init__() end")
    
    
    def msg(self, mytype, msg):
        '''Adds a message of a certain type to the ongoing in-memory log and
        saves it to the data_store
        '''
        maint()
        debug("ErrCls msg() start")
        from rtc import RTC
        rtc = RTC()
        
        #print("debugging.enabled in msg(): '" + str(debugging.enabled) + "'")
        
        self.debug("In Err.msg(), msg: '" + str(msg) + "'")
        log_entry = (rtc.now(), mytype, {'message': msg})
        self.log.append(log_entry)
        debug("ErrCls msg() end")
        return self.data_store.update(log_entry)
    
    
    def warn(self, msg):
        '''Turns on the warning LED, adds the warning to the log set, and saves
        it to the data_store
        '''
        # FIXME Do a code review, ensure I do maint() everywhere
        maint()
        debug("ErrCls warn() start")

        #print("debugging.enabled in warn(): '" + str(debugging.enabled) + "'")
        
        self.debug("self.msg(msg): '" + str(msg) + "'")
        self.msg('warning', msg)
        
        # TODO Not working
        ## Blink for 500 ms, off for 1500 ms, and set this as the default
        #leds.blink(run = True, pattern = (
        #            (self.leds.warn, True, 500),
        #            (self.leds.warn, False, 1500)),
        #            default = True)
        leds.LED('warn', default = True)
        debug("ErrCls warn() end")
    
    
    def err(self, msg):
        '''Things got real bad. Stop everything.'''
        maint()
        debug("ErrCls err() start")
        from time import sleep
        
        self.msg('error', msg)
        
        # FIXME Is that enough time? Maybe wait for a completion flag. But time
        # that out.
        sleep(3)
        
        # Whatever hasn't been sent, save it to flash
        DataStore.save_all()
        
        # Steady red LED
        # TODO blink() not working. Using LED() instead.
        # TODO The pattern is awkward. See if we can pass only a single pattern
        # by doing some kind of detection.
        #leds.blink(run = True, pattern = ((leds.err, True, None)))
        leds.LED('err', default = True)
        
        if not self.testing:
            wdt.stop()
        
        debug("ErrCls err() end")
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
        maint()
        debug("ErrCls exc() start")
        # TODO Also optionally allow the exception to flow through to stderr
        if args:
            content = args
        
        content['exc_type'] = str(sys.exc_info()[0])
        content['error'] = str(sys.exc_info()[1]).strip()
        
        # TODO And what about the exc_num like in OSError? For now,
        # investigate by hand and later, by allowing an exception argument 
        # to this module.
        
        self.msg('exception', content)
        debug("ErrCls exc() end")
        if not self.testing:
            sys.exit(1)