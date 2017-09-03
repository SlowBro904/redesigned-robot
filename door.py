def operate(direction):
    '''Takes 'up' or 'dn' and moves the door in that direction'''
    from motor import MotorCls
    from maintenance import maint
    
    maint()
    
    motor = MotorCls()
    motor.run(direction)