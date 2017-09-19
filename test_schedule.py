print("Starting test_schedule")
from rtc import RTC
from ujson import dumps
from test_suite import good
from system import SystemCls
from schedule import Schedule
from time import mktime, gmtime

system = SystemCls()
rtc = RTC()
now = gmtime(rtc.now())
# 5 second buffer. If we don't do this next_event_time() likely will fail.
now_secs = rtc.now() + 5
# TODO Is it better to rename today to weekday?
now_hour, now_min, now_sec, today = now[3], now[4], now[5], now[6]
# Number of seconds since epoch as of 00:00 this morning.
today_secs = now_secs - (now_hour*60*60) - (now_min*60) - now_sec

# Turn our schedule into a comma-delimited string
temp_sched = ','.join([str(today), str(now_hour), str(now_min)])
# FIXME Create a command for test to run, and a different parameter than test
test_schedule = {temp_sched: ['test', 'test']}
with open('/flash/device_data/test.json', 'w') as f:
    f.write(dumps(test_schedule))

schedule = Schedule(['test'])

check = 'get_due()'
assert schedule.get_due('test') == [(today_secs, 'test', 'test')], check
good(check)

check = 'get_events()'
events = schedule.get_events('test')
assert events[0] == (today_secs, 'test', 'test'), check
good(check)

check = 'next_event_time()'
assert schedule.next_event_time() == now_secs, check
good(check)