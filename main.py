# Set this up first because other modules depend upon this
from config import CONFIG
config = CONFIG('/flash/smartbird.cfg', '/flash/smartbird.defaults.cfg')

import errors
from i2c import I2C
from rtc import RTC
from wdt import WDT
from wifi import WIFI
from system import SYSTEM
from battery import BATTERY
from schedule import SCHEDULE
from machine import deep_sleep
from cloud_communication import ping_cloud, send, get_data_updates, update_system

# Set this here in the event that other objects fire warnings upon instantiation
errors.good_LED(True)

i2c = I2C()
wifi = WIFI()
rtc = RTC(i2c)
battery = BATTERY()
system = SYSTEM(i2c)
schedule = SCHEDULE()

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

schedule.run()
errors.process_warnings()
wdt.stop()
rtc.set_alarm(schedule.next_event_time())
deep_sleep()