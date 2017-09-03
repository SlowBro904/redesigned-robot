def status():
    '''Tells whether the door is in the up or down position'''
    from err import ErrCls
    from machine import Pin
    from config import config
    
    err = ErrCls()
    
    up_pin_cfg = config.conf['DOOR_REED_UP_PIN']
    dn_pin_cfg = config.conf['DOOR_REED_DN_PIN']
    
    up = Pin(up_pin_cfg, mode = Pin.IN, pull = Pin.PULL_UP)
    dn = Pin(dn_pin_cfg, mode = Pin.IN, pull = Pin.PULL_UP)
    
    status = 'between'
    if up and not dn:
        status = 'up'
    elif dn and not up:
        status = 'dn'
    elif up and dn:
        err.error('Door reed switch malfunction.')
    
    return status