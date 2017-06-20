from config import get_config
from i2c import I2C
from rtc import RTC
from wdt import WDT
from wifi import WIFI
from battery import BATTERY
from system import SYSTEM
from mqtt import MQTT
from scheduled_events import scheduled_events
from errors import process_warnings
from cloud_communication import ping_cloud, send, get_data_updates, update_system

config = CONFIG('/flash/smartbird.cfg', '/flash/smartbird.defaults.cfg')
i2c = I2C()
rtc = RTC(i2c)
system = SYSTEM(i2c)
wifi = WIFI()
battery = BATTERY()

battery.check_charge()
rtc.check_temp()
ping_cloud()
rtc.rtc_to_system()
# FIXME Set both the RTC and local clock with NTP
rtc.ntp_to_rtc()
update_system()
send('battery_charge', battery.charge)
send('rtc_temp', rtc.temp)
send('attached_devices', system.attached_devices)
get_data_updates()
# FIXME if not my_scheduled_events: hard_error()
for scheduled_event in scheduled_events():

process_warnings()
# FIXME Also wdt.feeder().stop()
wdt.stop()