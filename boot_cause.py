""" Determine the wake cause. Return 'PwrBtn', 'WDT', 'Alarm', 'UpReed', 'DnReed', 'Aux' """
from machine import reset_cause, PWRON_RESET, HARD_RESET, SOFT_RESET, BROWN_OUT_RESET, WDT_RESET, DEEPSLEEP_RESET

boot_cause = None

if reset_cause() in [PWRON_RESET, HARD_RESET, SOFT_RESET, BROWN_OUT_RESET]:
    boot_cause = 'PwrBtn'

if reset_cause() in [WDT_RESET]:
    boot_cause = 'WDT'

if reset_cause() in [DEEPSLEEP_RESET]:
    # FIXME Return also Up/DnReed or Aux
    boot_cause = 'Alarm'