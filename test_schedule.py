print("Starting test_schedule")
import debugging
from rtc import RTC
from ujson import dumps
from config import config
from test_suite import good
from system import SystemCls
from schedule import Schedule
from time import mktime, gmtime

debug = debugging.printmsg

system = SystemCls()
rtc = RTC()
now = rtc.now()
now_secs = rtc.now_secs()
now_hour, now_min, now_sec, today = now[3], now[4], now[5], now[6]
# Number of seconds since epoch as of 00:00 this morning.
today_secs = now_secs - (now_hour*60*60) - (now_min*60) - now_sec

# Turn our schedule into a comma-delimited string
temp_sched1 = ','.join([str(today), str(23), str(56)])
temp_sched2 = ','.join([str(today), str(23), str(57)])
temp_sched3 = ','.join([str(today), str(23), str(58)])
temp_sched4 = ','.join([str(today), str(23), str(59)])
# FIXME Create a command to run, and a parameter for it
test_schedule1 = {  temp_sched1: ['test1_cmd', 'test1_arg'],
                    temp_sched2: ['test2_cmd', 'test2_arg']}
test_schedule2 = {  temp_sched3: ['test3_cmd', 'test3_arg'],
                    temp_sched4: ['test4_cmd', 'test4_arg']}
with open('/flash/device_data/test1.json', 'w') as f:
    f.write(dumps(test_schedule1))
with open('/flash/device_data/test2.json', 'w') as f:
    f.write(dumps(test_schedule2))

schedule = Schedule(['test1','test2'])

print("[DEBUG] schedule.get_due('test1'): '" +
        str(schedule.get_due('test1')) + "'")
print("[DEBUG] schedule.get_due('test1')[0][0]: '" +
        str(schedule.get_due('test1')[0][0]) + "'")
print("[DEBUG] schedule.get_due('test1')[0][1:]: '" +
        str(schedule.get_due('test1')[0][1:]) + "'")
print("[DEBUG] today_secs: '" + str(today_secs) + "'")
print("[DEBUG] config.conf['SCHEDULE_BUFFER']: '" +
        str(config.conf['SCHEDULE_BUFFER']) + "'")
due = schedule.get_due('test1')

check = 'get_due()[0][0]'
assert due[0][0] <= today_secs + int(config.conf['SCHEDULE_BUFFER']), check
good(check)

check = 'get_due()[0][1:]'
assert due[0][1:] == ('test1_cmd','test1_arg'), check
good(check)

check = 'get_todays_events()'
events = schedule.get_todays_events('test1')
print("[DEBUG] events: '" + str(events) + "'")
event_secs = today_secs + (23*60*60) + (56*60)
assert events[0] == (event_secs, 'test1_cmd', 'test1_arg'), check
good(check)

check = 'next_event_time()'
print("[DEBUG] schedule.next_event_time(): '" +
        str(schedule.next_event_time) + "'")
assert schedule.next_event_time == event_secs, check
good(check)