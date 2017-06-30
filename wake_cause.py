""" Determine the wake cause. Return 'PwrBtn', 'WDT', 'Alarm', 'UpReed', 'DnReed', 'Aux' """
from machine import reset_cause, PWRON_RESET, HARD_RESET, SOFT_RESET, BROWN_OUT_RESET, WDT_RESET, DEEPSLEEP_RESET

wake_cause = None

if reset_cause() in [PWRON_RESET, HARD_RESET, SOFT_RESET, BROWN_OUT_RESET]:
    wake_cause = 'PwrBtn'

if reset_cause() in [WDT_RESET]:
    wake_cause = 'WDT'

if reset_cause() in [DEEPSLEEP_RESET]:
    wake_cause = 'Alarm'