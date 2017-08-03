# Automatic garbage collector
import gc
gc.enable()

# Did we download any new updates? Install them now before anything runs.
import updates
install_updates()

# The rest of our modules
import web_admin
from rtc import RTC
import factory_reset
from leds import leds
from cloud import Cloud
from config import config
from err import ErrCls
from system import System
from battery import Battery
from wifi import sta, sta_ap
from schedule import Schedule
from datastore import DataStore
from boot_cause import boot_cause
from updates import install_updates
from maintenance import maint
from machine import sleep, WAKEUP_ANY_HIGH, deepsleep, pin_deepsleep_wakeup

err = Err()

# TODO Not working
##Every two seconds, a green blink. Set this as the default.
# leds.blink(run = True, pattern = (
            # (leds.good, True, 300), 
            # (leds.good, False, 1700)),
            # default = True)
leds.LED('good', default = True)

rtc = RTC()
battery = Battery()
system = System()
schedule = Schedule(system.attached_devices)
cloud = Cloud()

# Keep our watchdog fed or he'll bite
wdt.start()

# If our charge is too low this will error
battery.check_charge()

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

wifi.connect()
rtc.start()
cloud.connect()
    
try:
    updates.get_system_updates()
    cloud.send('version', system.version)
    cloud.send('battery_charge', battery.charge)
    cloud.send('attached_devices', system.attached_devices)
    cloud.send('ntp_status', rtc.ntp_status)
    updates.get_data_updates()
except RuntimeError:
    # Ignore if not connected
    pass

schedule.run()
DataStore.save_all()

# FIXME For production disable the web repl, FTP, telnet, serial, etc.
# TODO Inside webadmin, a read-only serial console. Or log the console and
# upload it.

wdt.stop()

# Ensure these are on P2, P3, P4, P6, P8 to P10 or P13 to P23 per the
# documentation.
wake_pins = [config.conf['DOOR_REED_UP_PIN'],
                config.conf['DOOR_REED_DN_PIN'],
                config.conf['AUX_WAKE_PIN']]

pin_deepsleep_wakeup(pins = wake_pins, mode = WAKEUP_ANY_HIGH)
sleep_microseconds = (schedule.next_event_time - rtc.now())*1000
deepsleep(sleep_microseconds)