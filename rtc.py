class RTC(object):
    from machine import RTC as system_clock
    from errors import hard_error, warning
    from main import config
    from urtc import DS3231 # From https://github.com/adafruit/Adafruit-uRTC/blob/master/urtc.py
    
    rtc = False
    ntp_server = None
    
    def __init__(self, i2c):
      """ A class for the RTC functionality. Can update the system clock, the RTC clock, sets up an NTP synchronization, and can even check the temperature. """
      try: self.rtc = self.DS3231(i2c)
      except: # TODO Get specific about exceptions all over
        self.warning('RTC_connection_error')
      
      # Start an NTP sync daemon in the background
      # FIXME If not syncing try another server
      # FIXME Check the status in main.py
      self.ntp_server = self.config['NTP_SERVER']
      self.system_clock.ntp_sync(self.ntp_server)
    
    
    def rtc_to_system(self):
      """ Copies the RTC time to the system clock """
      # TODO This may not be necessary. I might be able to run self.__del__()
      if not self.rtc: return False
      
      rtc_datetime_tuple = (
        self.rtc.datetime.year,
        self.rtc.datetime.month,
        self.rtc.datetime.day,
        self.rtc.datetime.hour,
        self.rtc.datetime.minute,
        self.rtc.datetime.second
      )
      
      if not self.system_clock.init(rtc_datetime_tuple):
        self.warning('Cannot_update_system_clock_from_RTC')
        return False
    
    
    def system_to_rtc(self):
      """ Copies the system clock time to the RTC """
      if not self.rtc: return False
      
      right_now = self.system_clock.now()
      
      system_datetime_tuple = (
        year    = right_now[0],
        month   = right_now[1],
        day     = right_now[2],
        hour    = right_now[3],
        minute  = right_now[4],
        second  = right_now[5]
      )

      if not self.rtc.datetime(system_datetime_tuple):
        self.warning('Cannot_update_RTC_from_system_clock')
        return False
    
    
    def check_ntp(self):
      """ Returns the status of NTP synchronization """
      return self.system_clock.synced()
    
    
    def check_temp(self):
      """ Checks if the temperature as measured by the RTC is greater than CRITICAL_TEMP in the config file and if so, throws a hard error. """
      if self.temp >= self.config['CRITICAL_TEMP']:
        self.hard_error()
    
    
    @property
    def temp(self):
      """ Temperature as measured by the RTC in Celcius """
      # FIXME Finish
      pass