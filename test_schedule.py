print("Starting test_schedule")
from rtc import RTC
from ujson import dumps
from test_suite import good
from schedule import Schedule

rtc = RTC()
now = rtc.now()
# 5 second buffer. If we don't do this next_event_time() likely will fail.
now_secs = mktime(now) + 5
now_hour, now_min, now_sec, today = now[3], now[4], now[5], now[6]
# Number of seconds since epoch as of 00:00 this morning.
today_secs = now_secs - (now_hour*60*60) - (now_min*60) - now_sec

test_schedule = {(today, now_hour, now_min): ('test', 'test')}
with open('/flash/device_data/test.json', 'w') as f:
    f.write(dumps(test_schedule))

schedule = Schedule()

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