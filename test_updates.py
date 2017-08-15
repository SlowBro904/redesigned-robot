print("Starting test_updates")
from wifi import mywifi, sta
mywifi = sta()
mywifi.connect()

from test_suite import good
from os import listdir, remove
from updates import get_new_dirs

# FIXME Wrong return in updates.py get_new_dirs() cloud.send()
get_new_dirs()
assert 'deleteme' in listdir(), "get_new_dirs()"
good("get_new_dirs()")
remove('deleteme')