# Install any new versions of scripts
from os import listdir, remove, rename
files = listdir('/flash/')
for file in files:
    if file.endswith('.new'):
        try:
            remove('/flash/' + file)
            rename('/flash/' + file + '.new', '/flash/' + file)
        except:
            pass # FIXME Do we want to really pass on this?

from WDT import WDT # This module will check whether the code is fixed and if not, create our own pseudoWDT

wdt = WDT(timeout = 10000)

# Feed our watchdog every chance you get or he'll bite
wdt.feeder()