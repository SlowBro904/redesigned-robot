class BATTERY(object):
  from main import config
  from errors import hard_error
  
  def check_charge(self):
    """ Checks if the battery charge is less than CRITICAL_BATTERY_LEVEL in the config file and if so, throws a hard error. """
    if self.charge <= self.config['CRITICAL_BATTERY_LEVEL']: self.hard_error()
  
  @property
  def charge(self):
    """ Sets the value of the battery charge. Note that this does not return the actual voltage. See the note in the config file. """
    from machine import ADC
    
    battery_pin = self.config['BATTERY_VOLT_SENSE_PIN']
    
    # Read the value of the voltage on the battery volt sense pin using ADC.ATTN_11DB which allows a range of 0-3.3V.
    self.charge = ADC().channel(pin = battery_pin, attn = ADC.ATTN_11DB)