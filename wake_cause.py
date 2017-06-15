from machine import reset_cause, PWRON_RESET, SOFT_RESET

wake_cause = None
def wake_cause():
    """ Determine the wake cause. Return 'RTC', 'WDT', 'PwrBtn', 'UpReed', 'DnReed', 'Aux' """
    if wake_cause:
        return
    if reset_cause() == PWRON_RESET:
        if rtc.alarm(2):
            wake_cause = 'RTC'