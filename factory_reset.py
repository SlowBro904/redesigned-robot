"""Listens to our factory reset switch.

If it's held down more than five seconds do a reset back to factory settings.
"""
from time import sleep
from machine import Pin
from reboot import reboot
from config import config
from errors import ERRORS

def fac_rst_handler():
    """ Triggered when the reset button is pressed """
    errors = ERRORS()
    
    # Blink our yellow/red LEDs to let the user know the button is held
    errors.flash_yellow_red('start')
    sleep(5)
    errors.flash_yellow_red('stop')
    
    # If we're still holding it after 5 seconds
    if fac_rst_pin:
        # Now red continuously until rebooted
        errors.good_LED(False)
        errors.warn_LED(False)
        errors.error_LED(True)

        if config.reset_to_defaults():
            # FIXME What if it fails?
            # FIXME Also need to delete local data files
            # FIXME Create a mechanism to synchronize data files
            # TODO Create unmutable config options that survive a reset (Wait,
            # isn't this what the default config is for? We can always update
            # that.)            
            reboot(delay = 0, boot_cause = 'PwrBtn')

# Setup our listener
fac_rst_pin = 'P' + config['FACTORY_RESET_PIN']
fac_rst_pin_lsnr = Pin(fac_rst_pin, mode = Pin.IN, pull = Pin.PULL_UP)
fac_rst_pin_lsnr.callback(Pin.IRQ_FALLING | Pin.IRQ_RISING, fac_rst_handler)