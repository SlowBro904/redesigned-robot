import rtc
from test_suite import good
print("Starting test_rtc")
rtc = rtc.RTC()

assert isinstance(rtc.now(), int), "rtc.now() is not int"
good("rtc.now() is int")
# FIXME Not yet
#assert rtc.now()[0] >= 2017, "

# FIXME Finish