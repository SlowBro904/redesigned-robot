# FIXME Uncomment
#from err import ErrCls
from utime import sleep
from config import config
from maintenance import maint
from machine import RTC as system_clock_cls

class RTC(object):    
    def __init__(self):
        '''A class for the RTC functionality.
        
        Can update the system clock and sets up an NTP synchronization.
        '''
        # FIXME Uncomment
        #self.err = Err()
        self.system_clock = system_clock_cls()
        self.ntp_server = config.conf['NTP_SERVER']
    
    
    def start(self):
        '''Let's get started'''
        # FIXME Do a final code review, ensure I am doing maint()
        # everywhere
        maint()
        self.start_ntp_daemon()
        self.check_system_clock()
    
    
    def start_ntp_daemon(self, ntp_server = None):
        '''Start an NTP sync daemon in the background'''
        # TODO If not syncing try another server
        maint()
        
        if not ntp_server:
            if self.ntp_server:
                ntp_server = self.ntp_server
            else:
                raise RuntimeError("No NTP server selected")
        
        #try:
        return self.system_clock.ntp_sync(ntp_server)
        #except:
        #    warning = ("Cannot sync NTP. Server: ",
        #                ntp_server,
        #                "('rtc.py', 'start_ntp_daemon')")
        #    self.err.warning(warning)
        #    return False
    
    
    def ntp_status(self):
        '''Returns the status of NTP synchronization'''
        return self.system_clock.synced()
    
    
    def now(self):
        '''Returns the current time as a tuple'''
        return self.system_clock.now()
    
    
    def now_secs(self):
        '''Returns the current time in seconds since epoch'''
        from time import mktime
        return mktime(self.system_clock.now())
    
    
    def check_system_clock(self):
        '''Check that the system clock has been set at least once.
        
        If not connected to get NTP sync and RTC time has not yet been set the 
        RTC year will be 1970. This is bad news, because our schedule won't 
        run. Throw a hard error.
        '''
        if not self.ntp_status():
            # Wait 10 seconds
            sleep(10)
        
        # Try again. If NTP is running we're good.
        if self.ntp_status():
            return True
        
        this_year = self.rtc.now()[0]
        
        if this_year == 1970:
            error = ("Cannot setup clock so I cannot run the schedule",
                        "('rtc.py', 'check_system_clock')")
            # FIXME Uncomment
            #self.err.error(error)