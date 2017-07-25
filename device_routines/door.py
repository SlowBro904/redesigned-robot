def operate(direction):
    '''Takes 'up' or 'dn' and moves the door in that direction'''
    from maintenance import maint
    
    maint()
    
    motor = MOTOR()
    motor.run(direction)