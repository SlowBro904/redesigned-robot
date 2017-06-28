class RTC(object):
    from config import config
    from machine import RTC as system_clock
    from wdt import wdt
    
    def __init__(self):
        """ A class for the RTC functionality. Can update the system clock and sets up an NTP synchronization """
        from errors import ERRORS
        self.errors = ERRORS()
        
        # FIXME If not connected to NTP and RTC time == 1970 epoch hard error
    
    
    def ntp_to_system(self, ntp_server = None)
        """ Start an NTP sync daemon in the background """
        # TODO If not syncing try another server
        # TODO Check the status in main.py
        
        if not ntp_server:
            ntp_server = self.config['NTP_SERVER']
        
        self.wdt.feed()
        
        self.system_clock.ntp_sync(ntp_server)
    
    
    def check_ntp(self):
        """ Returns the status of NTP synchronization """
        return self.system_clock.synced()
    
    
    def now(self):
        """ Returns the current time in seconds since epoch """
        from utime import mktime
        return mktime(self.system_clock.now())