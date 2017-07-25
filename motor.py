class Motor(object):
    from config import config
    import door_reed_switches
    from time import sleep, sleep_ms
    from machine import Pin, Timer, ADC
    from maintenance import maint
    
    up = Pin(config.conf['MOTOR_UP_PIN'], mode = Pin.OUT, pull = PULL_DOWN)
    dn = Pin(config.conf['MOTOR_DN_PIN'], mode = Pin.OUT, pull = PULL_DOWN)
    volt_pin = Pin(config.conf['MOTOR_VOLT_PIN'], mode = Pin.IN,
                    pull = PULL_DOWN)
    low_voltage = config.conf['MOTOR_LOW_VOLTAGE']
    high_voltage = config.conf['MOTOR_HIGH_VOLTAGE']
    
    def __init__(self, timeout = self.config.conf['MOTOR_TIMEOUT'],
                    check_interval = self.config.conf['MOTOR_CHECK_INTERVAL']):
        '''Sets up the motor object'''
        self.maint()
        self.timeout = timeout
        self.check_interval = check_interval
        self.stop()
    
    def run(self, direction, timeout = self.timeout):
        '''Starts the motor in the requested direction.
        
        It will stop on its own based on the door reed switces.
        '''
        self.maint()
        
        if direction == 'up':
            self.up(True)
        else:
            self.dn(True)

        timer = self.Timer.Chrono()
        timer.start()
    
        while True:
            timer.reset()
        
            # If the status shows we are completely in the direction requested
            if self.door_reed_switches.status == direction:
                self.stop()
                break
            
            # Constantly monitor the voltage and if it is out of range stop,
            # reverse for three seconds, then try again
            if not self.low_voltage < self.voltage < self.high_voltage:
                self.stop()
                
                if direction == 'up':
                    reverse = 'dn'
                else:
                    reverse = 'up'
                
                timer.reset()
                self.run(direction = reverse, timeout = 3)
            
            self.maint()
            self.sleep_ms(self.check_interval)
            
            if timer.read() >= timeout:
                timer.stop()
                return False
    
    
    def stop(self):
        '''Stops all motors'''
        self.up(False)
        self.dn(False)
    
    
    @property
    def voltage(self):
        '''Gets our motor voltage'''
        # Read the value of the voltage on the battery volt sense pin using 
        # ADC.ATTN_11DB which allows a range of 0-3.3V.
        return self.ADC().channel(pin = self.volt_pin, attn = ADC.ATTN_11DB)