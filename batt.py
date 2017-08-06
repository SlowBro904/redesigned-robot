from err import ErrCls
from machine import ADC
from config import config
from maintenance import maint

class BattCls(object):
    def __init__(self):
        '''Configures our battery class'''
        pass
        maint()
        self.errors = ErrCls()
        self.batt_pin = config.conf['BATTERY_VOLT_SENSE_PIN']
        self.crit_batt = config.conf['CRITICAL_BATTERY_LEVEL']
    
    
    def check_charge(self):
        '''Checks if the battery charge is less than CRITICAL_BATTERY_LEVEL in
        the config file and if so, throws a hard error.
       
        The ADC runs at ATTN_11DB which allows measuring up to 3.3V.
       
        To get the value for CRITICAL_BATTERY_LEVEL divide 3.3 by 4096, which
        is the default ADC bit resolution of 12 bits. Then divide your target 
        value (1.8) by the number you got in the last step. Round to no decimal
        places.
      
        Example:
        3.3 / 4096 = 0.0008056640625
        1.8 / 0.0008056640625 = 2,234.181818181818
        Rounded, it equals 2234.
        '''        
        # TODO Calculate the value for CRITICAL_BATTERY_LEVEL here so the
        # config file can be more natural (1.8 instead of 2234)
        if self.charge <= self.crit_batt:
            error = "Battery too low. ('battery.py', 'check_charge')"
            self.errors.err(error)
    
    
    @property
    def charge(self):
        '''Returns the value of the battery charge.
       
        Note that this does not return the actual voltage. See the note in
        check_charge().
        '''
        maint()
        
        #try:
        # Read the value of the voltage on the battery volt sense pin using 
        # ADC.ATTN_11DB which allows a range of 0-3.3V.
        return ADC().channel(pin = self.batt_pin, attn = ADC.ATTN_11DB).value()
        #except:
           # FIXME Warnings and errors everywhere
           #warning = "Cannot get the battery charge. ('battery.py', 'charge')"
           #self.err.warning(warning)
           #return False