class Errors(object):
    import sys
    from os import remove
    
    try:
        from leds import leds
        from json import dump, load
        from machine import deepsleep
        from maintenance import maintenance
        error_log_file = '/flash/errors.json'
        exceptions_log_file = '/flash/exception_log.json'
    except ImportError:
        # Testing
        error_log_file = '/cygdrive/c/Temp/errors.json'
        exceptions_log_file = '/cygdrive/c/Temp/exception_log.json'
    
    log = set()
    
    def __init__(self):
        """A class for dealing with different error messages"""
        self.log = self.load_saved_log()
    
    
    def error(self, message):
        """Called when things get real bad. Stop everything.
        
        Adds the message to the log, if possible to upload the log and schedule
        status it does, if not it saves the log and schedule status, stops any 
        LEDs that may be blinking, turns on the error LED, stops the watchdog 
        timer, waits three seconds, and puts the device into indefinite deep
        sleep.
        """
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
                        (self.leds.warn, False, 1500)),
                        default = True)
    
    
    def save_log(self):
        """If we cannot connect to the cloud, let's save the log to flash for 
        next time we can connect.
        """
        # We don't want to always save the log because that causes more writes 
        # to the flash, which has a limited life. Only save when we cannot
        # connect, or have a hard error.
        self.maintenance()
        
        with open(self.error_log_file, 'w') as json_data:
            if not dump(self.log, json_data):
                return False
    
    
    def load_saved_log(self):
        """Load the log from flash and delete the file"""
        # FIXME Uncomment
        #self.maintenance()
        
        log = set()
        
        try:
            with open(self.error_log_file) as json_data:
                log = self.load(json_data)
        except (OSError, IOError):
            # Ignore if it doesn't exist
            pass
        
        # Only delete the save file if we were successful
        if log:
            self.clear_saved_log()
        
        return log
    
    
    def clear_saved_log(self):
        """Delete the saved log file"""
        self.maintenance()
        return self.remove(self.error_log_file)
    
    
    def clear_log(self):
        """Remove the log both from memory and flash"""
        self.maintenance()
        self.log = set()
        self.clear_saved_log()

        
    def timestamp(self):
        '''Gives a timestamp that's works with both MicroPython and regular'''
        try:
            from machine import RTC
            rtc = self.RTC()
            datetime = rtc.datetime()
        except ImportError:
            # For testing on a desktop
            from datetime import datetime
        
        return datetime.now()
    
    
    # FIXME Everywhere I use self. in defaults, remove the self.
    # FIXME Anti-pattern spotted.
    #   https://docs.quantifiedcode.com/python-anti-patterns/correctness/mutable_default_value_as_argument.html
    def log_exception(self, args = None):
        """Log uncaught exceptions in JSON format to memory.
        
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
        """
        # TODO Also optionally allow the exception to flow through to stderr
        if entry is None:
            entry = dict()
        
        entry = args
        entry['timestamp'] = self.timestamp()
        entry['exc_type'] = str(self.sys.exc_info()[0])
        entry['error'] = str(self.sys.exc_info()[1]).strip()
                
        # TODO And what about the exc_num like in OSError? For now,
        # investigate by hand and later, by allowing an exception argument 
        # to this module.
        
        self.entries.append(entry)
        
        self.sys.exit(1)
    
    
    def save_exception_log(self, log_file = exceptions_log_file):
        # FIXME Upload
        # FIXME Load on start just like error log
        # FIXME Can I just combine with the error log?
        with open(log_file, 'w') as log:
            return dump(self.entries, log)