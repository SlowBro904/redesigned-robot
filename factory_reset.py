"""Listens to our factory reset switch.

If it's held down more than five seconds do a reset back to factory settings.
"""
from time import sleep
from machine import Pin
from reboot import reboot
from config import config
from errors import ERRORS
from maintenance import maintenance

def fac_rst_handler():
    """ Triggered when the reset button is pressed """
    errors = ERRORS()
    
    maintenance()
    
    # Blink our yellow/red LEDs to let the user know the button is held
    errors.flash_LEDs(['warn', 'error'], 'start')
    sleep(5)
    errors.flash_LEDs(['warn', 'error'], 'stop')
    
    maintenance()
    
    # If we're still holding it after 5 seconds
    if fac_rst_pin:
        # Now red continuously until rebooted
        errors.good_LED(False)
        errors.warn_LED(False)
        errors.error_LED(True)
        
        maintenance()
        
        # FIXME What if it fails?
        config.reset_to_defaults()
        
        # Also delete local data files
        from os import listdir, remove
        data_path = '/flash/data/'
        for file in listdir(data_path):
            try:
                remove(data_path + file)
            except:
                # Ignore errors
                pass
        
        # Create a flag file to notify cloud.get_data_updates to fetch all data
        # files
        from json import dump
        with open('/flash/get_all_data_files.txt', 'w') as get_all_data_filesH:
            dump(True, get_all_data_filesH)
        
        reboot(delay = 3, boot_cause = 'PwrBtn')

maintenance()

# Setup our listener
fac_rst_pin = 'P' + config['FACTORY_RESET_PIN']
fac_rst_pin_lsnr = Pin(fac_rst_pin, mode = Pin.IN, pull = Pin.PULL_UP)
fac_rst_pin_lsnr.callback(Pin.IRQ_FALLING | Pin.IRQ_RISING, fac_rst_handler)