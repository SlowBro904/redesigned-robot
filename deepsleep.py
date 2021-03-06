def deepsleep(secs = None):
    '''Takes an optional number of seconds to the next wakeup event and deep
    sleeps the device. If no seconds are given, deep sleep indefinitely.
    
    This is for the WiPy with the deep sleep shield.
    '''
    import debugging
    from config import config
    from lib.deepsleep import DeepSleep
    
    # TODO Can I put this on all Python files? Maybe just import debugging and
    # done?
    debug = debugging.printmsg
    testing = debugging.testing
    debugging.default_level = 0
    
    ds = DeepSleep()
    
    # FIXME Now alter bootup reasons to match ds.get_wake_status()
    # https://docs.pycom.io/chapter/datasheets/boards/deepsleep/api.html

    # FIXME Ensure these are on P2, P3, P4, P6, P8 to P10 or P13 to P23 per the
    # documentation.
    # FIXME Only P10, P17, P18 work
    wake_pins = [   config.conf['DOOR_REED_UP_PIN'],
                    config.conf['DOOR_REED_DN_PIN'],
                    config.conf['AUX_WAKE_PIN']]
    
    debug("wake_pins: '" + str(wake_pins) + "'", level = 1)
    
    ds.enable_pullups(wake_pins)
    ds.enable_wake_on_fall(wake_pins)
    
    if testing:
        if secs:
            debug("Simulating deep sleep of " + str(secs) + " seconds.")
        else:
            debug("Simulating deep sleep of indefinite length.")
    else:
        ds.go_to_sleep(secs)