# Set this up first because other modules depend upon this
from config import CONFIG
config = CONFIG('/flash/smartbird.cfg', '/flash/smartbird.defaults.cfg')

from i2c import I2C
from rtc import RTC
from wdt import WDT
from wifi import WIFI
from battery import BATTERY
from system import SYSTEM
from mqtt import MQTT
from scheduled_events import run_scheduled_events
from cloud_communication import ping_cloud, send, get_data_updates, update_system
import errors

# Set this here in the event that other objects fire warnings upon instantiation
errors.good_LED(True)

i2c = I2C()
rtc = RTC(i2c)
system = SYSTEM(i2c)
wifi = WIFI()
battery = BATTERY()

battery.check_charge()
# TODO Add later, refer to the rtc.sh from C.H.I.P.
#rtc.check_temp()
rtc.rtc_to_system()

if ping_cloud():
    update_system()
    send('battery_charge', battery.charge)
    # TODO Add later
    #send('rtc_temp', rtc.temp)
    send('attached_devices', system.attached_devices)
    get_data_updates()

run_scheduled_events()
errors.process_warnings()
wdt.stop()