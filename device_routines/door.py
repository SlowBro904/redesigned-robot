def operate(direction):
    """Takes 'up' or 'dn' and moves the door in that direction"""
    from time import sleep_ms
    from config import config
    import door_reed_switches
    from machine import Pin, Timer
    from maintenance import maintenance
    
    maintenance()
    
    up_motor_cfg = 'P' + config['UP_MOTOR_PIN']
    dn_motor_cfg = 'P' + config['DN_MOTOR_PIN']
    
    up_motor = Pin(up_motor_cfg, mode = Pin.OUT, pull = PULL_DOWN)
    dn_motor = Pin(dn_motor_cfg, mode = Pin.OUT, pull = PULL_DOWN)
    
    # FIXME Measure motor voltage. Should I put the motor in a separate object?

    if direction = 'dn':
        motor = dn_motor()
    else:
        motor = up_motor()
    
    # Whichever direction we are going, go ahead
    motor(True)
    
    motor_check_interval = config['MOTOR_CHECK_INTERVAL']
    timeout = config['MOTOR_TIMEOUT']
    
    timer = Timer.Chrono()
    timer.start()
    
    while True:
        timer.reset()
        
        # If the status shows we are completely in the direction requested
        if door_reed_switch.status == direction:
            motor(False)
            break
        
        maintenance()
        sleep_ms(motor_check_interval)
        
        if timer.read() >= timeout:
            timer.stop()
            return False