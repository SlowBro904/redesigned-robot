def reboot(delay = 0, boot_cause = None):
    '''Reboots the device.
    
    Takes an optional delay value in seconds and an optional boot cause (the
    values in boot_cause.py) that can override the normal boot cause detection. 

    A good usage of the delay would be to allow for the web server to show HTML
    content to the browser.
    
    A good usage of the boot cause would be for after a factory reset, we want
    to load the web admin so we want to always act as though the button was
    pressed.
    
    The boot cause can be overridden by placing the value in JSON format in
    /flash/boot_cause.json.
    '''
    from json import dump
    from maintenance import maint
    from _thread import start_new_thread
    
    maint()
    
    # Override boot cause detection using this text file
    if boot_cause:
        try:
            with open('/flash/boot_cause.json', 'w') as boot_causeH:
                dump(boot_cause, boot_causeH)
        except OSError:
            # Ignore if it does not exist
            pass
    
    # TODO Do I need the id variable?
    start_new_thread(_reboot, (delay, id = 0))

def _reboot(delay, id):
    '''This is the actual reboot command.
    
    Not recommended you call this directly. Use reboot() instead.
    '''
    from time import sleep
    from machine import reset
    from maintenance import maint
    
    maint()
    sleep(delay)
    reset()