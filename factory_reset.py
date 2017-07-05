""" Listens to our factory reset switch. If it's held down more than five seconds do a reset back to factory settings. """
from time import sleep
from machine import Pin
from reboot import reboot
from config import config

def fac_rst_handler():
    """ Triggered when the reset button is pressed """
    sleep(5)
    
    # If we're still held after 5 seconds
    if fac_rst_pin:
        if config.reset_to_defaults():
            # FIXME What if it fails?
            # FIXME Also need to delete local data files
            # FIXME Create a mechanism to synchronize data files
            # TODO Create unmutable config options that survive a reset (Wait, isn't this what the default config is for? We can always update that.)
            reboot(delay = 0)

Pin('P' + config['FACTORY_RESET_PIN'], mode = Pin.IN, pull = Pin.PULL_UP).callback(Pin.IRQ_FALLING | Pin.IRQ_RISING, fac_rst_handler)