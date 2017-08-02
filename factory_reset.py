'''Listens to our factory reset switch.

If it's held down more than five seconds do a reset back to factory settings.
'''
from leds import leds
from json import dump
from time import sleep
from machine import Pin
from reboot import reboot
from config import config
from err import Err
from os import listdir, remove
from maintenance import maint

err = Err()

def fac_rst_handler():
    ''' Triggered when the reset button is pressed '''
    maint()
    
    # TODO Not working
    ## Blink our yellow/red LEDs to let the user know the button is held
    # leds.blink(run = True, pattern = (
                # (leds.warn, True, 500),
                # (leds.warn, False, 0), 
                # (leds.err, True, 500),
                # (leds.err, False, 0)))
    # TODO Can I do multiple colors?
    leds.LED('warn')
    sleep(5)
    
    maint()
    
    if not fac_rst_pin:
        return
    
    # TODO Not working
    ## We're still holding it after 5 seconds. Now steady red until rebooted.
    #leds.blink(run = True, pattern = (('err', True, None)))
    leds.LED('err')
    
    maint()
    
    try:
        config.reset_to_defaults()
    except:
        error = ("Could not reset to factory defaults.",
                    "('factory_reset.py', 'fac_rst_handler')"
        err.hard_error(error)
    
    # Also delete local data files
    for data_path in ['/flash/device_data/', '/flash/datasets/']:
        for file in listdir(data_path):
            try:
                remove(data_path + file)
            except OSError:
                # Ignore if it does not exist
                pass
        
    # Create a flag file to notify cloud.get_data_updates to fetch all data
    # files
    get_all_data_files_flag = '/flash/get_all_data_files.json'
    try:
        with open(get_all_data_files_flag, 'w') as get_all_data_filesH:
            dump(True, get_all_data_filesH)
    except:
        # Ignore err
        pass
    
    reboot(delay = 3, boot_cause = 'PwrBtn')

maint()

# Setup our listener
fac_rst_pin = config.conf['FACTORY_RESET_PIN']

try:
    fac_rst_pin_lsnr = Pin(fac_rst_pin, mode = Pin.IN, pull = Pin.PULL_UP)
    fac_rst_pin_lsnr.callback(Pin.IRQ_FALLING | Pin.IRQ_RISING,
                                fac_rst_handler)
except:
    err.error("Cannot listen for factory reset button presses.",
                        "('factory_reset.py', 'main')")