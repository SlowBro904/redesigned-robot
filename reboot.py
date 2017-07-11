def reboot(delay = 0, boot_cause = None):
    """Reboots the device.
    
    Takes an optional delay value in seconds and an optional boot cause (the
    values in boot_cause.py) that can override the normal boot cause detection. 

    A good usage of the delay would be to allow for the web server to show HTML
    content to the browser.
    
    A good usage of the boot cause would be for after a factory reset, we want
    to load the web admin so we want to always act as though the button was
    pressed.
    """
    from json import dump
    from maintenance import maintenance
    from _thread import start_new_thread
    
    maintenance()
    
    # Override boot cause detection using this text file
    if boot_cause:
        with open('/flash/boot_cause.json', 'w') as boot_causeH:
            dump(boot_cause, boot_causeH)
    
    start_new_thread(_reboot, (delay, id = 0))

def _reboot(delay, id):
    """This is the actual reboot command.
    
    Not recommended you call this directly. Use reboot() instead.
    """
    from time import sleep
    from machine import reset
    from maintenance import maintenance
    
    maintenance()
    sleep(delay)
    reset()