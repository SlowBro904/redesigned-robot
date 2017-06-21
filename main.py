# TODO It feels kludgy always passing config as a value. How do we put the configuration in memory so it's accessible to all modules? Ask StackExchange.
from i2c import I2C
from rtc import RTC
from wdt import WDT
from wifi import WIFI
from cloud import CLOUD
from errors import ERRORS
from config import CONFIG
from system import SYSTEM
from battery import BATTERY
from schedule import SCHEDULE
from machine import deep_sleep

# Set this here in the event that other objects fire warnings upon instantiation
errors.good_LED(True)

config = CONFIG('/flash/smartbird.cfg', '/flash/smartbird.defaults.cfg')
errors = ERRORS(config)
i2c = I2C(config)
wifi = WIFI(config)
rtc = RTC(i2c, config)
battery = BATTERY(config)
system = SYSTEM(i2c, config)
schedule = SCHEDULE(config)
cloud = CLOUD(config)

battery.check_charge()
# TODO Add later, refer to the rtc.sh from C.H.I.P.
#rtc.check_temp()
rtc.rtc_to_system()

if cloud.ping():
    cloud.get_system_updates()
    cloud.send('battery_charge', battery.charge)
    # TODO Add later
    #cloud.send('rtc_temp', rtc.temp)
    cloud.send('attached_devices', system.attached_devices)
    cloud.get_data_updates()

schedule.run()
errors.process_warnings()
wdt.stop()
rtc.set_alarm(schedule.next_event_time())
deep_sleep()