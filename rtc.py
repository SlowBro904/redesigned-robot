class RTC(object):
    from wdt import wdt
    from config import config
    from machine import RTC as system_clock
    
    def __init__(self):
        """ A class for the RTC functionality. Can update the system clock and sets up an NTP synchronization """
        from errors import ERRORS
        self.errors = ERRORS()
    
    
    def start_ntp_daemon(self, ntp_server = None)
        """ Start an NTP sync daemon in the background """
        # TODO If not syncing try another server
        # TODO Check the status in main.py
        
        if not ntp_server:
            ntp_server = self.config['NTP_SERVER']
        
        self.wdt.feed()
        
        self.system_clock.ntp_sync(ntp_server)
    
    
    def ntp_status(self):
        """ Returns the status of NTP synchronization """
        return self.system_clock.synced()
    
    
    def now(self):
        """ Returns the current time in seconds since epoch """
        from utime import mktime
        return mktime(self.system_clock.now())