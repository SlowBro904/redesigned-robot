

from WDT import WDT # This module will check whether the code is fixed and if not, create our own pseudoWDT

wdt = WDT(timeout = 10000)

# Feed our watchdog every chance you get or he'll bite
wdt.feeder()