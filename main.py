import updates
import web_admin
from rtc import RTC
import factory_reset
from leds import leds
from cloud import Cloud
from config import config
from errors import Errors
from system import System
from battery import Battery
from schedule import Schedule
from boot_cause import boot_cause
from wifi import wifi, sta, sta_ap
from maintenance import maintenance
from machine import sleep, deepsleep, WAKEUP_ANY_HIGH, pin_deepsleep_wakeup

errors = Errors()

# Every two seconds, a green blink. Set this as the default.
leds.blink(run = True, pattern = (
            (leds.good, True, 300), 
            (leds.good, False, 1700)),
            default = True)

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
battery = Battery()
system = System()
schedule = Schedule(system.attached_devices)
cloud = Cloud()

# Keep our watchdog fed or he'll bite
wdt.start()

# If our charge is too low this will hard error
battery.check_charge()

wifi.connect()
rtc.start_ntp_daemon()
cloud.connect()

# Checking to see if we are first connected reduces running time while we wait
# for connections to time out
# FIXME Do I need to go through each point like in web_admin/__init__.py? Or do
# I need to test wifi.isconnected() only as before? Or is this sufficient?
if cloud.isconnected():
    updates.get_system_updates()
    cloud.send('version', system.version)
    cloud.send('battery_charge', battery.charge)
    cloud.send('attached_devices', system.attached_devices)
    cloud.send('ntp_status', rtc.ntp_status)
    updates.get_data_updates()
else:
    rtc.check_system_clock()

# TODO Should this be schedule.status = schedule.run() ?
schedule.run()

if cloud.isconnected():
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

# Ensure these are on P2, P3, P4, P6, P8 to P10 or P13 to P23 per the
# documentation.
wake_pins = [config['DOOR_REED_UP_PIN'],
                config['DOOR_REED_DN_PIN'],
                config['AUX_WAKE_PIN']]

pin_deepsleep_wakeup(pins = wake_pins, mode = WAKEUP_ANY_HIGH)

# In other words setup our interrupts and wakeup reasons
sleep_microseconds = (schedule.next_event_time - rtc.now())*1000
deepsleep(sleep_microseconds)