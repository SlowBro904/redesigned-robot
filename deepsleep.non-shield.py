def deepsleep(secs = None):
    '''Takes an optional number of seconds to the next wakeup event and deep
    sleeps the device. If no seconds are given, deep sleep indefinitely.
    '''
    import debugging
    from config import config
    from machine import WAKEUP_ANY_HIGH, deepsleep, pin_deepsleep_wakeup, Pin
    
    debug = debugging.printmsg
    testing = debugging.testing
    debugging.default_level = 1
    
    microsecs = None
    if secs:
        microsecs = secs*1000
    
    # FIXME Ensure these are on P2, P3, P4, P6, P8 to P10 or P13 to P23 per the
    # documentation.
    up_pin = Pin(config.conf['DOOR_REED_UP_PIN'], mode = Pin.IN,
                    pull = Pin.PULL_UP)
    dn_pin = Pin(config.conf['DOOR_REED_DN_PIN'], mode = Pin.IN,
                    pull = Pin.PULL_UP)
    aux_pin = Pin(config.conf['AUX_WAKE_PIN'], mode = Pin.IN,
                    pull = Pin.PULL_UP)
    
    wake_pins = [up_pin, dn_pin, aux_pin]
    
    debug("wake_pins: '" + str(wake_pins) + "'", level = 1)
    
    pin_deepsleep_wakeup(pins = wake_pins, mode = WAKEUP_ANY_HIGH,
                            enable_pull = True)
    
    if testing:
        if secs:
            debug("Simulating deep sleep of " + str(secs) + " seconds.")
        else:
            debug("Simulating deep sleep of indefinite length.")
    else:
        deepsleep(microsecs)