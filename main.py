from i2c import I2C
from rtc import RTC
from wdt import WDT
from wifi import WIFI
from cloud import CLOUD
from config import config
from errors import ERRORS
from system import SYSTEM
from battery import BATTERY
from schedule import SCHEDULE
from machine import deep_sleep

# Set this here in the event that other objects fire warnings upon instantiation
errors.good_LED(True)

wdt = WDT() # FIXME I shouldn't start any object automatically
errors = ERRORS()
i2c = I2C()
wifi = WIFI()
rtc = RTC(i2c)
battery = BATTERY()
system = SYSTEM(i2c)
schedule = SCHEDULE()
cloud = CLOUD()

wdt.start()
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