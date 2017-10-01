print("Starting test_updates")
try:
    from wifi import mywifi, sta
    mywifi = sta()
    mywifi.connect()
except ImportError:
    pass

import debugging
from test_suite import good
from os import listdir, remove
from update_sys_simple import (get_sys_updates, install_updates,
                            _clean_failed_sys_updates)

debug = debugging.printmsg

# FIXME MemoryError. Rewrite the update code so it is extremely simple. One
# module if possible. Debug, then translate that code into this, then freeze
# the bytecode.
# https://learn.adafruit.com/micropython-basics-loading-modules/frozen-modules

# Clean before starting
updates = ['/flash/testing.dir', '/flash/testing.file', '/flash/file_list.json']
for file in updates:
    try:
        remove(file)
    except: # TODO except what?
        pass

debug("get_sys_updates()")
get_sys_updates()
debug("install_updates()")
install_updates()
files = listdir('/flash')

check = "Update directories"
assert 'testing.dir' in files, check
good(check)

check = "Update files"
assert 'testing.file' in files, check
good(check)

_clean_failed_sys_updates(updates)
files = listdir('/flash')

check = "_clean_failed_sys_updates()"
assert 'testing.dir' not in files, check
good(check)