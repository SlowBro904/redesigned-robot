print("Starting test_updates")
from wifi import mywifi, sta
mywifi = sta()
mywifi.connect()

from test_suite import good
from os import listdir, remove
from updates import get_new_dirs

# FIXME This is not working in umqtt.simple.publish(), the server simply does 
# not see the published data. But sending 'ping' gets the 'ack'.
get_new_dirs()
assert 'deleteme' in listdir(), "get_new_dirs()"
good("get_new_dirs()")
remove('deleteme')