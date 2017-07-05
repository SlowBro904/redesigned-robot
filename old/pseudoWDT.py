""" This is a workaround until Pycom implements WDT properly on the WiPy. It sets alarm1 on the DS3231 RTC to the number of seconds in the timeout in the future. If the alarm triggers it resets the board using the reset pin. The watchdog timer must be "fed" regularly resetting the alarm to 'timeout' seconds in the future. """

# FIXME The RTC alarm needs an RC timeout
def stop():
  """ Issues the I2C command necessary to disable alarm1 on the RTC """