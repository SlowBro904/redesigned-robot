def status():
    '''Tells whether the door is in the up or down position'''
    import debugging
    from err import ErrCls
    from machine import Pin
    from config import config
    from maintenance import maint
    
    debug = debugging.printmsg
    
    maint()
    err = ErrCls()
    
    up_pin_cfg = config.conf['DOOR_REED_UP_PIN']
    dn_pin_cfg = config.conf['DOOR_REED_DN_PIN']
    
    up = Pin(up_pin_cfg, mode = Pin.IN, pull = Pin.PULL_UP).value
    dn = Pin(dn_pin_cfg, mode = Pin.IN, pull = Pin.PULL_UP).value
    
    status = 'between'
    # TODO This is awkward. Maybe don't ground reed switches but go high? Or
    # invert the logic.
    #
    # Since we are grounding the reed switches, if the door is up then up()
    # will be 0 and dn() will be 1.
    if dn() and not up():
        status = 'up'
    elif not dn() and up():
        status = 'dn'
    elif not up() and not dn():
        debug('Door reed switch malfunction.')
        err.err('Door reed switch malfunction.')
    
    maint()
    debug("status: '" + str(status) + "'", level = 1)
    return status