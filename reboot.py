def reboot(delay = 0):
    """ Reboots te device. Takes a delay value in seconds. A good usage of this would be for example to allow for the web server to show HTML content to the browser. """
    from _thread import start_new_thread
    
    start_new_thread(_reboot, (delay, id = 0))

def _reboot(delay, id):
    """ This is the actual reboot command. Not recommended you call this directly. Use reboot() instead. """
    from time import sleep
    from machine import reset
    
    sleep(delay)
    reset()