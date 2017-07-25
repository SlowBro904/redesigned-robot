class LEDs(object):
    from machine import Pin
    
    # These must be hard-coded to prevent a recursion issue where
    # config_class.py cannot load the config file and throws an error.
    # TODO Do I need this now? I don't think I'm running any err in 
    # config_class.py. But I am pretty sure I will be soon. And/or maybe I
    # don't need it now that it's in a separate file?
    good = Pin('P10', mode = Pin.OUT)
    warn = Pin('P11', mode = Pin.OUT)
    err = Pin('P12', mode = Pin.OUT)
    
    def __init__(self):
        pass
    
    
    def blink(self, run = True, pattern = None, default = False):
        '''Blink the LEDs on a pattern.
        
        Takes a run command and a pattern, which is a tuple of tuples.
        
        The pattern is which LED (self.good, self.warn, or self.err) followed 
        by whether to turn it on (True) or off (False) followed by the delay in 
        number of milliseconds to run that LED. If delay is None, it is always 
        on.
        
        This example will flash the warn and error LEDs every 500 milliseconds:
        blink(run = True, pattern = (
                (self.warn, True, 500),
                (self.warn, False, 0), 
                (self.err, True, 500),
                (self.err, False, 0)))
        
        This example will start the warn LED and leave it on indefinitely:
        blink(run = True, pattern = ((self.warn, True, None))
        
        This example will start the good LED for 300 milliseconds then off for
        1700 milliseconds and set it as the default:
        blink(run = True, pattern = (
                (self.good, True, 300),
                (self.good, False, 1700)),
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
        from maintenance import maint
        from _thread import start_new_thread
        
        maint()
        
        if not default:
            self.default_pattern = None
        else:
            self.default_pattern = pattern
        
        if run:
            # Multithreading so we can get back to the next step in our process
            start_new_thread(_blink, (True, pattern))
        else:
            # Go back to our default pattern
            start_new_thread(_blink, (True, self.default_pattern))
    
    def _blink(self, run, pattern):
        '''The actual blink process.
        
        Don't run this directly, use blink() instead.
        '''
        from time import sleep_ms
        
        # TODO A kludge until Pycom fixes _thread.exit() from outside the
        # thread
        global _run
        
        # Stop anything that's currently running
        _run = False
        
        _run = run
        
        # TODO What other internal variables do we use elsewhere that are not
        # prepended with underscore?
        while _run:
            for LED, state, delay in pattern:
                self.maint()
                
                LED(state)
                
                if not delay or delay < 10:
                    # Always have a little bit of delay. Don't want this to
                    # hammer our little system. 10 ms should be imperceptible.
                    delay = 10
                
                # TODO Is it better maybe to setup a timer and callback?
                for i in range(delay):
                    if not _run:
                        break
                    
                    sleep_ms(1)
                
                else:
                    # _run was True during the entire delay loop. Start
                    # on the next outer for loop on the next pattern.
                    continue
                # _run was set to False during the delay loop. Don't run
                # any more outer for loops on any more patterns, and because
                # that variable is now False the while loop will also exit.
                break
        
        self.maint()

# End of class LEDs(object)

leds = LEDs()