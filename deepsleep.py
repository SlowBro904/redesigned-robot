def deepsleep(secs = None):
    '''Takes an optional number of seconds to the next wakeup event and deep
    sleeps the device. If no seconds are given, deep sleep indefinitely.
    '''
    import debugging
    from config import config
    from machine import WAKEUP_ANY_HIGH, deepsleep, pin_deepsleep_wakeup
    
    debug = debugging.printmsg
    testing = debugging.testing
    
    microsecs = None
    if secs:
        microsecs = secs*1000
    
    # FIXME Ensure these are on P2, P3, P4, P6, P8 to P10 or P13 to P23 per the
    # documentation.
    wake_pins = [config.conf['DOOR_REED_UP_PIN'],
                config.conf['DOOR_REED_DN_PIN'],
                config.conf['AUX_WAKE_PIN']]
    
    pin_deepsleep_wakeup(pins = wake_pins, mode = WAKEUP_ANY_HIGH)
    
    if testing:
        if secs:
            debug("Simulating deep sleep of " + str(secs) + " seconds.")
        else:
            debug("Simulating deep sleep of indefinite length.")
    else:
        deepsleep(microsecs)