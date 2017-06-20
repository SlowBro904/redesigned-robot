# Install any new versions of scripts
# FIXME But how can I install a new boot.py? Put all boot.py commands into a separate file, and this function in another. Rename most other files, then in a separate function rename the renamer function if it's updated. Or is that even needed? Test. Maybe reboot after renaming boot.py. Tested it, not needed. But keep this note to consider some more before go-live.
from os import listdir, remove, rename
files = listdir('/flash/')
for file in files:
    if file.endswith('.new'):
        try:
            remove('/flash/' + file)
            rename('/flash/' + file + '.new', '/flash/' + file)
        except:
            pass # FIXME Do we want to really pass on this?

from wdt import WDT # This module will check whether the code is fixed and if not, create our own pseudoWDT

# TODO Do I want to specify this somewhere?
wdt = WDT(timeout = 10000)

# Feed our watchdog every chance you get or he'll bite
wdt.feeder()