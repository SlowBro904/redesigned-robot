import web_admin
from wdt import wdt
from rtc import RTC
import factory_reset
from cloud import CLOUD
from config import config
from errors import ERRORS
from system import SYSTEM
from battery import BATTERY
from machine import deepsleep
from schedule import SCHEDULE
from boot_cause import boot_cause
from wifi import wifi, sta, sta_ap

# Set this here in the event that other objects fire warnings upon instantiation
errors = ERRORS()
errors.good_LED(True)

if boot_cause == 'PwrBtn':
    wifi = sta_ap()
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

# Checking to see if we are first connected reduces running time while we wait for connections to time out
if wifi.isconnected() and cloud.isconnected():
    cloud.get_system_updates()
    cloud.send('battery_charge', battery.charge)
    cloud.send('attached_devices', system.attached_devices)
    cloud.send('ntp_status', rtc.ntp_status)
    cloud.get_data_updates()
else:
    # If not connected to NTP and RTC time is not set, throw a hard error.
    # FIXME But ensure we can bootup to web admin with the button pressed.
    # FIXME The hour/minute/second will surely not match. Need to just look at year and day.
    if rtc.now() == (1970, 1, 1, 0, 0, 0):
        errors.hard_error()

schedule.run()

if wifi.isconnected() and cloud.isconnected():
    if cloud.send('schedule_status', schedule.status):
        schedule.clear_status()
    
    if cloud.send('warnings', errors.warnings):
        errors.clear_warnings()
else:
    # FIXME Remove most try/except, wait to see if we get any errors. Then for production disable the serial port.
    # FIXME Maybe not. Because if we get any exceptions the flow of logic will stop. Let's instead throw all errors into a log.
    # Save our current status for next time we can connect
    schedule.save_status()
    errors.save_warnings()

# FIXME Finish web admin. Show warnings/errors, what else?
# FIXME Shut down the web admin daemon when updating. Don't want browser commands doing stuff. Show a yellow/red alternating flashing light.
# TODO Inside webadmin, a read-only serial console. Or log the console and upload it.

wdt.stop()

# FIXME Here, and everywhere deepsleep is used: machine.pin_deepsleep_wakeup(...
sleep_microseconds = (schedule.next_event() - rtc.now())*1000
deepsleep(sleep_microseconds)