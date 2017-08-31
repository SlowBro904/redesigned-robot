'''This can be imported into every module to always be feeding our dog. Don't
want timeouts.
'''
# TODO But we don't want a fat dog e.g. fed too often and a slow system. 
# Profile how many times we run feed() and compare to the time taken not 
# running feed.
from machine import WDT
from debugging import testing

timeout = 10
if testing:
    timeout = 360000000

# Hard coded because config sources this file and setting it there causes a
# loop
wdt = WDT(timeout = timeout)