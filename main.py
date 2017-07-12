import web_admin
from rtc import RTC
import factory_reset
from leds import leds
from cloud import CLOUD
from config import config
from errors import ERRORS
from system import SYSTEM
from battery import BATTERY
from schedule import SCHEDULE
from boot_cause import boot_cause
from wifi import wifi, sta, sta_ap
from maintenance import maintenance
from machine import sleep, deepsleep

errors = ERRORS()

# Every two seconds, a green blink. Set this as the default.
leds.blink('start', pattern = (
            (leds.good, True, 300), 
            (leds.good, False, 1700)
            ), default = True)

if boot_cause == 'PwrBtn':
    wifi = sta_ap()
    # FIXME What if we get updates and do a reboot in the middle of running our
    # web admin? Maybe don't reboot if it's running. One of the functionalities
    # is by pressing the button the device pulls the latest updates. Maybe
    # check to see if anyone is connected to the web admin and if so hold on
    # (perhaps send an alert popup) and if not, proceed to reboot as normal but
    # remembering the state for next reboot.
    web_admin.start()
else:
    wifi = sta()

rtc = RTC()
battery = BATTERY()
system = SYSTEM()
schedule = SCHEDULE(system.attached_devices)
cloud = CLOUD()

# Keep our watchdog fed or he'll bite
wdt.start()

# If our charge is too low this will hard error
battery.check_charge()

wifi.connect()
rtc.start_ntp_daemon()
cloud.connect()

# Checking to see if we are first connected reduces running time while we wait
# for connections to time out
if wifi.isconnected() and cloud.isconnected():
    cloud.get_system_updates()
    cloud.send('battery_charge', battery.charge)
    cloud.send('attached_devices', system.attached_devices)
    cloud.send('ntp_status', rtc.ntp_status)
    cloud.get_data_updates()
else:
    # FIXME Will this trigger a WDT? May need to create a mysleep() function
    # that feeds our watchdog.
    sleep(10)
    this_year = rtc.now()[0]
    
    # If not connected to get NTP sync and RTC time has not yet been set the 
    # RTC year will be 1970. This is bad news, because our schedule won't run. 
    # Throw a hard error.
    # TODO Move this into the RTC class? As a check and leave implementation in
    # there.
    if this_year == 1970:
        errors.hard_error('Cannot setup clock so I cannot run the schedule')

schedule.run()

if wifi.isconnected() and cloud.isconnected():
    if cloud.send('schedule_status', schedule.status):
        schedule.clear_status()
    
    if cloud.send('log', errors.log):
        errors.clear_log()
else:
    # FIXME Re-add try/except at the end of the module chain so maybe here.
    # Throw all errors into a log. For production disable the serial port.
    
    # Save our current status for next time we can connect
    schedule.save_status()
    errors.save_log()

# TODO Inside webadmin, a read-only serial console. Or log the console and
# upload it.

wdt.stop()

# FIXME Here, and everywhere deepsleep is used: machine.pin_deepsleep_wakeup(..
# In other words setup our interrupts and wakeup reasons
sleep_microseconds = (schedule.next_event_time - rtc.now())*1000
deepsleep(sleep_microseconds)