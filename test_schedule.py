print("Starting test_schedule")
import debugging
from rtc import RTC
from ujson import dumps
from test_suite import good
from system import SystemCls
from schedule import Schedule
from time import mktime, gmtime

debug = debugging.printmsg

system = SystemCls()
rtc = RTC()
now = gmtime(rtc.now())
# 5 second buffer. If we don't do this next_event_time() likely will fail.
now_secs = rtc.now() + 5
now_hour, now_min, now_sec, today = now[3], now[4], now[5], now[6]
# Number of seconds since epoch as of 00:00 this morning.
today_secs = now_secs - (now_hour*60*60) - (now_min*60) - now_sec

# Turn our schedule into a comma-delimited string
temp_sched = ','.join([str(today), str(23), str(59)])
# FIXME Create a command for test to run, and a different parameter than test
test_schedule = {temp_sched: ['test', 'test']}
with open('/flash/device_data/test.json', 'w') as f:
    f.write(dumps(test_schedule))

schedule = Schedule(['test'])

check = 'get_due()'
print("[DEBUG] schedule.get_due('test'): '" + 
        str(schedule.get_due('test')) + "'")
print("[DEBUG] [(today_secs, 'test', 'test')]: '" + 
        str([(today_secs, 'test', 'test')]) + "'")
due = schedule.get_due('test')
# FIXME This needs to test whether due is less than or equal to today_secs +
# the SCHEDULE_BUFFER. I noticed today_secs is coming up as 5 though it should
# be 0. Not sure why.
assert due[0] == [(today_secs, 'test', 'test')], check
good(check)

check = 'get_todays_events()'
events = schedule.get_todays_events('test')
assert events[0] == (today_secs, 'test', 'test'), check
good(check)

check = 'next_event_time()'
assert schedule.next_event_time() == now_secs, check
good(check)