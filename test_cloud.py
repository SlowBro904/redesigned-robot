print("Starting test_cloud")
from wifi import mywifi, sta_ap
mywifi = sta_ap()
from cloud import cloud
print("Here")
from test_suite import good

assert cloud.can_login() is True, "cloud.can_login()"
good("cloud.can_login()")

assert cloud.encryption_working() is True, "cloud.encryption_working()"
good("cloud.encryption_working()")

assert cloud.isconnected() is True, "cloud.isconnected()"
good("cloud.isconnected()")