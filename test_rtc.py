from wifi import mywifi, sta
mywifi = sta()
mywifi.connect()

import rtc
from utime import sleep
from test_suite import good
print("Starting test_rtc")
rtc = rtc.RTC()
rtc.start()

check = "rtc.now_secs() is int"
assert isinstance(rtc.now_secs(), int), check
good(check)

sleep(10)

check = "ntp_status() is bool"
assert isinstance(rtc.ntp_status(), bool), check
good(check)

check = "rtc.now()[0] >= 2017, NTP working"
assert rtc.now()[0] >= 2017, check
good(check)