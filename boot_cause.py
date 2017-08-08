'''Determines the wake cause.

Sets the boot_cause variable to 'PwrBtn', 'WDT', 'Alarm', 'UpReed', 'DnReed', 
or 'Aux'

Can be overridden by placing the boot cause in /flash/boot_cause.json in JSON
format.
'''
from os import remove
from ujson import loads
from maintenance import maint
from machine import BROWN_OUT_RESET, WDT_RESET, DEEPSLEEP_RESET
from machine import reset_cause, PWRON_RESET, HARD_RESET, SOFT_RESET

maint()

boot_cause = None

if reset_cause() in [PWRON_RESET, HARD_RESET, SOFT_RESET, BROWN_OUT_RESET]:
    boot_cause = 'PwrBtn'
elif reset_cause() in [WDT_RESET]:
    boot_cause = 'WDT'
elif reset_cause() in [DEEPSLEEP_RESET]:
    wake_reason, gpio_list = machine.wake_reason()
    if wake_reason == machine.RTC_WAKE:
        boot_cause = 'Alarm'
    elif wake_reason == machine.PWRON_WAKE:
        boot_cause = 'PwrBtn'
    elif wake_reason == machine.PIN_WAKE:
        if config.conf['DOOR_REED_UP_PIN'] in gpio_list:
            boot_cause = 'UpReed'
        elif config.conf['DOOR_REED_DN_PIN'] in gpio_list:
            boot_cause = 'DnReed'
        elif config.conf['AUX_WAKE_PIN'] in gpio_list:
            boot_cause = 'Aux'

maint()

# If this file is present it overrides what was discovered above
try:
    boot_cause_file = '/flash/boot_cause.json'
    with open(boot_cause_file) as f:
        boot_cause = loads(f.read())
    
    remove(boot_cause_file)
except:
    # Does not exist, ignore
    pass