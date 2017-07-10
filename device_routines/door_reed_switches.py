def status():
    """Tells whether the door is in the up or down position"""
    from machine import Pin
    from config import config
    
    up_pin_cfg = 'P' + config['DOOR_REED_UP_PIN']
    dn_pin_cfg = 'P' + config['DOOR_REED_DN_PIN']
    
    up_pin = Pin(up_pin_cfg, mode = Pin.IN, pull = Pin.PULL_UP)
    dn_pin = Pin(dn_pin_cfg, mode = Pin.IN, pull = Pin.PULL_UP)
    
    status = 'unknown'
    # While in between both extremes both of these will be False
    # TODO What would we do if both are True?
    if up_pin and not dn_pin:
        status = 'up'
    elif dn_pin and not up_pin:
        status = 'dn'
    
    return status