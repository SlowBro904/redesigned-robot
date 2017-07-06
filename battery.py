class BATTERY(object):
    from wdt import wdt
    from machine import ADC
    from errors import ERRORS
    from config import config
        
    def check_charge(self):
        """Checks if the battery charge is less than CRITICAL_BATTERY_LEVEL in
        the config file and if so, throws a hard error.
        
        The ADC runs at ATTN_11DB which allows measuring up to 3.3V.
        
        To get the value for CRITICAL_BATTERY_LEVEL divide 3.3 by 4096, which is
        the default ADC bit resolution of 12 bits. Then divide your target value
        (1.8) by the number you got in the last step. Round to no decimal
        places.
        
        Example:
        3.3 / 4096 = 0.0008056640625
        1.8 / 0.0008056640625 = 2,234.181818181818
        Rounded, it equals 2234.
        """
        self.errors = self.ERRORS()
        
        # TODO Calculate the value for CRITICAL_BATTERY_LEVEL here so the config
        # file can be more natural (1.8 instead of 2234)
        if self.charge <= self.config['CRITICAL_BATTERY_LEVEL']:
            self.errors.hard_error()
    
    
    @property
    def charge(self):
        """Returns the value of the battery charge.
        
        Note that this does not return the actual voltage. See the note in
        check_charge().
        """
        self.wdt.feed()
        
        battery_pin = self.config['BATTERY_VOLT_SENSE_PIN']
        
        # Read the value of the voltage on the battery volt sense pin using 
        # ADC.ATTN_11DB which allows a range of 0-3.3V.
        return ADC().channel(pin = battery_pin, attn = ADC.ATTN_11DB)