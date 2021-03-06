# Automatic garbage collector
import gc
gc.enable()

# Don't install updates on boot. Going to install them after get_sys_updates().
## Did we download any new updates? Install them now before anything runs.
## Test written
from update_sys import get_sys_updates#, install_updates
#install_updates()

# The rest of our modules
# Tested
import fac_rst
# Tested
import web_admin
# Tested
from rtc import RTC
# Tested
from leds import leds
# Tested
from err import ErrCls
# Tested
from batt import BattCls
# Tested
from config import config
# Tested
from cloud import CloudCls
# Tested
from wifi import sta, sta_ap
# Tested
from system import SystemCls
# Tested
from schedule import Schedule
# Tested
from maintenance import maint
# Tested
from deepsleep import deepsleep
# Tested
from datastore import DataStore
# Tested
from boot_cause import boot_cause
# Tested
from update_data import get_data_updates

# Keep our watchdog fed or he'll bite
wdt.start()

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
schedule = ScheduleCls(system.attached_devices)
cloud = CloudCls()

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
    get_sys_updates()
    cloud.send('version', system.version)
    cloud.send('battery_charge', battery.charge)
    cloud.send('attached_devices', system.attached_devices)
    cloud.send('ntp_status', rtc.ntp_status)
    get_data_updates()
except RuntimeError:
    # Ignore if not connected
    pass

schedule.run()
DataStore.save_all()

# FIXME For production disable the web repl, FTP, telnet, serial, etc. Edit the
# source code, esp32/frozen/_boot.py.
# TODO Inside webadmin, a read-only serial console. Or log the console and
# upload it.

wdt.stop()

secs = schedule.next_event_time - rtc.now_secs()
deepsleep(secs)