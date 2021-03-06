import debugging
import door_reed_switches
from config import config
from maintenance import maint
from time import sleep, sleep_ms
from machine import Pin, Timer, ADC

debug = debugging.printmsg

class MotorCls(object):
    timeout = config.conf['MOTOR_TIMEOUT']
    low_voltage = config.conf['MOTOR_LOW_VOLTAGE']
    high_voltage = config.conf['MOTOR_HIGH_VOLTAGE']
    check_interval = config.conf['MOTOR_CHECK_INTERVAL']
    up = Pin(config.conf['MOTOR_UP_PIN'], mode = Pin.OUT, pull = Pin.PULL_DOWN)
    dn = Pin(config.conf['MOTOR_DN_PIN'], mode = Pin.OUT, pull = Pin.PULL_DOWN)
    volt_pin = config.conf['MOTOR_VOLT_PIN']
    
    def __init__(self, timeout = None, check_interval = None):
        '''Sets up the motor object'''
        maint()

        if timeout:
            self.timeout = timeout
        
        if check_interval:
            self.check_interval = check_interval
        
        self.stop()
    
    
    def run(self, direction, timeout = None):
        '''Starts the motor in the requested direction.
        
        It will stop on its own based on the door reed switces.
        '''
        maint()
        
        if not timeout:
            timeout = self.timeout
        
        if direction == 'up':
            debug("Direction is up.")
            debug("Before setting:")
            debug("self.up.value(): '" + str(self.up.value()) + "'")
            debug("self.dn.value(): '" + str(self.dn.value()) + "'")
            self.up.value(True)
            self.dn.value(False)
            debug("After setting:")
            debug("self.up.value(): '" + str(self.up.value()) + "'")
            debug("self.dn.value(): '" + str(self.dn.value()) + "'")
        else:
            debug("Direction is dn.")
            debug("Before setting:")
            debug("self.up.value(): '" + str(self.up.value()) + "'")
            debug("self.dn.value(): '" + str(self.dn.value()) + "'")
            self.dn.value(True)
            self.up.value(False)
            debug("After setting:")
            debug("self.up.value(): '" + str(self.up.value()) + "'")
            debug("self.dn.value(): '" + str(self.dn.value()) + "'")
        
        timer = Timer.Chrono()
        timer.start()
        
        while True:
            # If the status shows we are completely in the direction requested
            if door_reed_switches.status() == direction:
                debug("door_reed_switches.status() == direction. Stopping.")
                debug("self.up.value(): '" + str(self.up.value()) + "'")
                debug("self.dn.value(): '" + str(self.dn.value()) + "'")
                timer.stop()
                self.stop()
                break
            
            # Constantly monitor the voltage and if it is out of range stop,
            # reverse for three seconds, then try again
            if not self.low_voltage < self.voltage < self.high_voltage:
                debug("We are outside of voltage range, reversing.")
                self.stop()
                
                if direction == 'up':
                    reverse = 'dn'
                else:
                    reverse = 'up'
                
                timer.reset()
                # FIXME What if we're jammed in both directions? Prevent
                # infinite recursion
                self.run(direction = reverse, timeout = 3)
            
            maint()
            sleep_ms(self.check_interval)
            
            if timer.read() >= timeout:
                debug("Motor timed out")
                timer.stop()
                return False
    
    
    def stop(self):
        '''Stops all motors'''
        debug("Before stopping:")
        debug("self.up.value(): '" + str(self.up.value()) + "'")
        debug("self.dn.value(): '" + str(self.dn.value()) + "'")
        self.up.value(False)
        self.dn.value(False)
        debug("After stopping:")
        debug("self.up.value(): '" + str(self.up.value()) + "'")
        debug("self.dn.value(): '" + str(self.dn.value()) + "'")
    
    
    @property
    def voltage(self):
        '''Gets our motor voltage'''
        # Read the value of the voltage on the battery volt sense pin using 
        # ADC.ATTN_11DB which allows a range of 0-3.3V.
        return ADC().channel(pin = self.volt_pin, attn = ADC.ATTN_11DB).value()