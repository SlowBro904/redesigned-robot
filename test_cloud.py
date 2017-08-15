print("Starting test_cloud")
from wifi import mywifi, sta
mywifi = sta()
mywifi.connect()

from cloud import cloud
from test_suite import good

# FIXME Incorporate ping() into main.py. But wait, does this actually do
# anything?
assert cloud.ping() is None, "cloud.ping()"
good("cloud.ping()")

assert cloud.can_login() is True, "cloud.can_login()"
good("cloud.can_login()")

assert cloud.isconnected() is True, "cloud.isconnected()"
good("cloud.isconnected()")