class RTC(object):
    from machine import RTC
    from errors import ERRORS
    from config import config
    from maintenance import maintenance
    
    def __init__(self):
        """A class for the RTC functionality.
        
        Can update the system clock and sets up an NTP synchronization.
        """
        self.errors = ERRORS()
        self.system_clock = RTC()
    
    
    def start_ntp_daemon(self, ntp_server = self.config['NTP_SERVER'])
        """Start an NTP sync daemon in the background"""
        # TODO If not syncing try another server
        # TODO Check the status in main.py
        
        self.maintenance()
        
        return self.system_clock.ntp_sync(ntp_server)
    
    
    def ntp_status(self):
        """Returns the status of NTP synchronization"""
        return self.system_clock.synced()
    
    
    def now(self):
        """Returns the current time in seconds since epoch"""
        from time import mktime
        return mktime(self.system_clock.now())
    
    
    def check_system_clock(self):
        """Check that the system clock has been set at least once.
        
        If not connected to get NTP sync and RTC time has not yet been set the 
        RTC year will be 1970. This is bad news, because our schedule won't 
        run. Throw a hard error.
        
        This should only be run if we're not able to connect to the network.
        """
        from wifi import wifi
        
        if wifi.isconnected():
            if not self.ntp_status():
                # Wait 10 seconds
                sleep(10)
       
            # Try again. If NTP is running we're good.
            if self.ntp_status():
                return True
        
        this_year = self.rtc.now()[0]
        
        if this_year == 1970:
            self.errors.hard_error(
                'Cannot setup clock so I cannot run the schedule')