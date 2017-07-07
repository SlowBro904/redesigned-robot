"""Determines the wake cause.

Returns 'PwrBtn', 'WDT', 'Alarm', 'UpReed', 'DnReed', or 'Aux'

Can be overridden by placing the boot cause in /flash/boot_cause.txt.
"""
from os import remove
from maintenance import maintenance
from machine import BROWN_OUT_RESET, WDT_RESET, DEEPSLEEP_RESET
from machine import reset_cause, PWRON_RESET, HARD_RESET, SOFT_RESET

boot_cause = None

if reset_cause() in [PWRON_RESET, HARD_RESET, SOFT_RESET, BROWN_OUT_RESET]:
    boot_cause = 'PwrBtn'

if reset_cause() in [WDT_RESET]:
    boot_cause = 'WDT'

if reset_cause() in [DEEPSLEEP_RESET]:
    # FIXME Return also Up/DnReed or Aux
    boot_cause = 'Alarm'

maintenance()

# If this file is present it overrides what was discovered above
try:
    boot_cause_file = '/flash/boot_cause.txt'
    with open(boot_cause_file) as boot_causeH:
        boot_cause = boot_causeH.readlines()
    
    remove(boot_cause_file)
except:
    # Does not exist, ignore
    pass