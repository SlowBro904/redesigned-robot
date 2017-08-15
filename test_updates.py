print("Starting test_updates")
from wifi import mywifi, sta
mywifi = sta()
mywifi.connect()

from test_suite import good
from os import listdir, remove
from updates import get_new_dirs, get_sys_updates

# FIXME Wrong return in updates.py get_new_dirs() cloud.send()
get_new_dirs()
assert 'deleteme' in listdir(), "get_new_dirs()"
good("get_new_dirs()")
remove('deleteme')

# FIXME I'm testing that this file gets created, but also test that this file
# gets updated. Also test that a failed sha sum (insert a bad sum) causes a
# rollback.
get_sys_updates()
assert 'deleteme.txt' in listdir(), "get_sys_updates()"
good("get_sys_updates()")


remove('deleteme.txt')