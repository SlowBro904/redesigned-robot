from wdt import wdt
from rtc import RTC
import factory_reset
from wifi import wifi
from cloud import CLOUD
from config import config
from errors import ERRORS
from system import SYSTEM
from battery import BATTERY
from machine import deepsleep
from schedule import SCHEDULE
from boot_cause import boot_cause

# FIXME Timezone

# Set this here in the event that other objects fire warnings upon instantiation
errors = ERRORS()
errors.good_LED(True)

if boot_cause == 'PwrBtn':
    wifi.wifi = sta_ap()
    
    # Copy the module variable/object into a local variable/object
    wifi = wifi.wifi
    
    # Start our web admin interface
    import webadmin
else:
    wifi.wifi = sta()
    wifi = wifi.wifi

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

# Checking to see if we are first connected reduces running time while we wait for connections to time out
if wifi.isconnected() and cloud.ping():
    cloud.get_system_updates()
    cloud.send('battery_charge', battery.charge)
    cloud.send('attached_devices', system.attached_devices)
    cloud.send('ntp_status', rtc.ntp_status)
    cloud.get_data_updates()
else:
    # FIXME Finish and test this
    # If not connected to NTP and RTC time is not set, throw a hard error.
    # FIXME But ensure we can bootup to web admin with the button pressed.
    # FIXME The hour/minute/second will surely not match. Need to just look at year and day.
    if rtc.now() == (1970, 1, 1, 0, 0, 0):
        errors.hard_error()

schedule.run()

if wifi.isconnected() and cloud.ping():
    if cloud.send('schedule_status', schedule.status):
        schedule.clear_status()
    
    if cloud.send('warnings', errors.warnings):
        errors.clear_warnings()
else:
    # FIXME Remove most try/except, wait to see if we get any errors. Then for production disable the serial port.
    # Save our current status for next time we can connect
    schedule.save_status()
    errors.save_warnings()

# FIXME Finish webadmin
# TODO Inside webadmin, a read-only serial console

wdt.stop()

# FIXME Here, and everywhere deepsleep is used: machine.pin_deepsleep_wakeup(...
sleep_microseconds = (schedule.next_event() - rtc.now())*1000
deepsleep(sleep_microseconds)