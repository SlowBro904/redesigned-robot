from wdt import wdt
from i2c import I2C
from rtc import RTC
from wifi import WIFI
from cloud import CLOUD
from config import config
from errors import ERRORS
from system import SYSTEM
from battery import BATTERY
from schedule import SCHEDULE
from machine import deep_sleep

# Set this here in the event that other objects fire warnings upon instantiation
errors = ERRORS()
errors.good_LED(True)

i2c = I2C()
wifi = WIFI()
rtc = RTC(i2c)
battery = BATTERY()
system = SYSTEM(i2c)
schedule = SCHEDULE(system.attached_devices)
cloud = CLOUD()

# FIXME Every command below feeds the wdt
wdt.start() # FIXME I shouldn't start any object automatically
battery.check_charge()
# TODO Add later, refer to the rtc.sh from C.H.I.P.
#rtc.check_temp()
rtc.rtc_to_system()

# FIXME What timeout?
if cloud.ping():
    cloud.get_system_updates()
    cloud.send('battery_charge', battery.charge)
    # TODO Add later
    #cloud.send('rtc_temp', rtc.temp)
    cloud.send('attached_devices', system.attached_devices)
    cloud.get_data_updates()

schedule.run()
errors.process_warnings()

if cloud.ping():
    cloud.send('schedule_status', schedule.status())
    schedule.remove_saved_status()
    cloud.send(errors.warnings)
else:
    # Save our current status for next time we can connect
    schedule.save_status()

wdt.stop()
rtc.set_alarm(schedule.next_event())
deep_sleep()