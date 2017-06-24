""" This can be imported into every module to always be feeding our dog. Don't want timeouts. """
# TODO But we don't want a fat dog e.g. fed too often and a slow system. Profile how many times we run feed() and compare to the time taken not running feed.
from machine import WDT
from config import config
wdt = WDT(timeout = config['WDT_TIMEOUT'])