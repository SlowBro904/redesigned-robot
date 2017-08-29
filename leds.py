import _thread
import debugging
from machine import Pin
from time import sleep_ms
from maintenance import maint

class LEDs(object):
    # These must be hard-coded to prevent a recursion issue where
    # config_class.py cannot load the config file and throws an error.
    # TODO Do I need this now? I don't think I'm running any err in 
    # config_class.py. But I am pretty sure I will be soon. And/or maybe I
    # don't need it now that it's in a separate file?
    good = Pin('P10', mode = Pin.OUT)
    warn = Pin('P11', mode = Pin.OUT)
    err = Pin('P12', mode = Pin.OUT)
    
    
    # TODO Is this needed?
    def __init__(self, debug = False, debug_level = 0):
        debugging.enabled = debug
        debugging.default_level = debug_level
        self.debug = debugging.printmsg
        self.debug("Initialization complete", level = 1)
        self.default = {'good': False, 'warn': False, 'err': False}
    
    
    def run_default(self):
        '''Runs the default LED'''
        self.debug("self.default: '" + str(self.default) + "'", level = 1)
        for LED_name, value in self.default.items():
            if LED_name is 'good':
                self.good(value)
            elif LED_name is 'warn':
                self.warn(value)
            elif LED_name is 'err':
                self.err(value)
    
    
    def LED(self, LED_name = None, default = False):
        '''Shine the LED we specify. If we set a default this is what shines
        even when we turn off the LED. That way for example if we are in a 
        warning state and we run another LED, we want to return to a warning
        state when that is done. Calling default = True will set the last
        called LED as the default.
        '''
        if not LED_name or LED_name is 'default':
            if default:
                self.default = {'good': False, 'warn': False, 'err': False}
            
            self.run_default()
            return
        
        if LED_name is 'good':
            self.good(True)
            self.warn(False)
            self.err(False)
        elif LED_name is 'warn':
            self.good(False)
            self.warn(True)
            self.err(False)
        elif LED_name is 'err':
            self.good(False)
            self.warn(False)
            self.err(True)
        
        if default:
            for this_LED in self.default:
                if this_LED is LED_name:
                    self.default[this_LED] = True
                else:
                    self.default[this_LED] = False
    
            self.debug("self.default: '" + str(self.default) + "'", level = 1)
    
    def blink(self, run = True, pattern = None, default = False, id = None):
        '''Blink the LEDs on a pattern.
        
        NOT CURRENTLY WORKING. Use standard LEDs off and on (no blink) for now.
        
        Takes a run command and a pattern, which is a list of tuples.
        
        The pattern is which LED (self.good, self.warn, or self.err) followed 
        by whether to turn it on (True) or off (False) followed by the delay in 
        number of milliseconds to run that LED. If delay is None, it is always 
        on.
        
        This example will flash the warn and error LEDs every 500 milliseconds:
        blink(run = True, pattern = [
                (self.warn, True, 500),
                (self.warn, False, 0), 
                (self.err, True, 500),
                (self.err, False, 0)])
        
        This example will start the warn LED and leave it on indefinitely:
        blink(run = True, pattern = [(self.warn, True, None)])
        
        This example will start the good LED for 300 milliseconds then off for
        1700 milliseconds and set it as the default:
        blink(run = True, pattern = [
                (self.good, True, 300),
                (self.good, False, 1700)],
                default = True)
        
        This example will stop any currently-running pattern and return to the
        default.
        blink(run = False)
        
        Only one pattern can run at a time. Any pattern currently running is
        stopped when a new one is called.
        
        The default argument, if True, is the pattern displayed when the
        currently-running pattern gets stopped. So if we are in a warning state
        and flashing yellow and it is the default, if another pattern such as 
        red/yellow is initiated, when that pattern stops it returns back to the
        default. Calling blink() multiple times with default = True will set
        the last called pattern as the default.
        '''
        maint()
        
        if not default:
            self.default_pattern = None
        else:
            self.default_pattern = pattern
        
        if run:
            self.debug("Running the _blink thread", level = 1)
            # Multithreading so we can get back to the next step in our process
            _thread.start_new_thread(self._blink, (True, pattern, id))
        else:
            self.debug("Stopping the _blink thread and returning to default", 
                        level = 1)
            global _run
            _run = False
            _thread.start_new_thread(self._blink, (True, self.default_pattern))
    
    
    def _blink(self, run, pattern, id = 0):
        '''The actual blink process.
        
        Don't run this directly, use blink() instead.
        '''
        self.debug("id: " + str(id), level = 1)
        self.debug("pattern: '" + str(pattern) + "'", level = 1)
        
        # TODO A kludge until Pycom fixes _thread.exit() from outside the
        # thread
        global _run
        
        # Stop anything that's currently running
        _run = False
        
        _run = run
        
        if not pattern:
            return
        
        # TODO What other internal variables do we use elsewhere that are not
        # prepended with underscore (private)?
        while _run:
            self.debug("Begin of the while loop, id: " + str(id), level = 0)
            for LED, state, delay in pattern:
                self.debug("LED: '" + str(LED) + "'", level = 2)
                self.debug("state: '" + str(state) + "'", level = 2)
                self.debug("delay: '" + str(delay) + "'", level = 2)
                if debugging.enabled and debugging.default_level > 0:
                    sleep_ms(1000)
                
                maint()
                
                self.debug("Before setting, LED is '" + str(LED.value()) + "'",
                            level = 2)
                
                LED(state)
                
                self.debug("Now LED is set to '" + str(LED.value()) + "'",
                            level = 2)
                
                if not delay or delay < 1:
                    # Always have a little bit of delay. Don't want this to
                    # hammer our little system. 1ms should be imperceptible.
                    delay = 1
                self.debug("Now delay is set to '" + str(delay) + "'", 
                            level = 0)
                
                # TODO Is it better maybe to setup a timer and callback?
                for i in range(delay):
                    self.debug("Delay count: " + str(i), level = 3)
                    if not _run:
                        # TODO Fails to reach here
                        self.debug("_thread.exit()")
                        _thread.exit()
                    
                    sleep_ms(1)
        maint()

# End of class LEDs(object)

leds = LEDs()