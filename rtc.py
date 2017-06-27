class RTC(object):
    from errors import ERRORS
    from config import config
    from machine import RTC as system_clock
    
    rtc = False
    ntp_server = None
    
    def __init__(self):
        """ A class for the RTC functionality. Can update the system clock, the RTC clock, sets up an NTP synchronization, and can even check the temperature. """
        from i2c import i2c
        from urtc import DS3231
        
        try:
            self.rtc = self.DS3231(i2c)
        except: # TODO Get specific about exceptions all over
            # FIXME If not connected destroy this object, return False
            self.warning('RTC_connection_error')
        
        self.errors = self.ERRORS()
    
    
    def ntp_to_system(self, ntp_server = None)
        """ Start an NTP sync daemon in the background """
        # FIXME Update NTP_SERVER in the config
        # TODO If not syncing try another server
        # TODO Check the status in main.py
        
        if not ntp_server:
            ntp_server = self.config['NTP_SERVER']
        
        self.system_clock.ntp_sync(ntp_server)

    
    def rtc_to_system(self):
        """ Copies the RTC time to the system clock """
        rtc_datetime_tuple = (
            self.rtc.datetime.year,
            self.rtc.datetime.month,
            self.rtc.datetime.day,
            self.rtc.datetime.hour,
            self.rtc.datetime.minute,
            self.rtc.datetime.second
        )
      
        if not self.system_clock.init(rtc_datetime_tuple):
            self.errors.warning('Cannot_update_system_clock_from_RTC')
            return False
    
    
    # TODO I think this is redundant
    def system_to_rtc(self):
        """ Copies the system clock time to the RTC """
        if not self.rtc:
            return False
        
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
            self.errors.warning('Cannot_update_RTC_from_system_clock')
            return False
    
    
    def check_ntp(self):
        """ Returns the status of NTP synchronization """
        return self.system_clock.synced()
    
    
    def set_alarm(self, datetime, alarm_num = 2):
        """ Sets the alarm with the datetime, choosing alarm_num 2 as default. The 2nd alarm only offers hour and minute resolution while the 1st alarm offers hour/minute/second resolution. But usually we only need hour and minute resolution. """
        # FIXME Finish
        pass
    
    
    def check_temp(self):
        """ Checks if the temperature in Celcius as measured by the RTC is greater than CRITICAL_TEMP in the config file and if so, throws a hard error. """
        # TODO See if we're regularly getting close to this value
        if self.temp >= self.config['CRITICAL_TEMP']:
            self.errors.hard_error()
    
    
    @property
    def temp(self):
        """ Temperature as measured by the RTC in Celcius """
        # TODO Finish
        pass