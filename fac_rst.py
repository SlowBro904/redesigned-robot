'''Listens to our factory reset switch.

If it's held down more than five seconds do a reset back to factory settings.
'''
import debugging
from leds import leds
from err import ErrCls
from json import dumps
from time import sleep
from machine import Pin
from reboot import reboot
from config import config
from maintenance import maint
from os import listdir, remove

errors = ErrCls()

debug = debugging.printmsg
testing = debugging.testing

def _fac_rst_handler(pin):
    ''' Triggered when the reset button is pressed '''
    maint()
    debug("_fac_rst_handler callback called")
    
    # TODO blink() not working, using LED() instead
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
    
    if pin() == True:
        # The logic is inverted. If True the button is not pressed.
        debug("Didn't hold fac_rst_pin for five seconds")
        return
    
    # TODO Not working
    ## We're still holding it after 5 seconds. Now steady red until rebooted.
    #leds.blink(run = True, pattern = (('err', True, None)))
    leds.LED('err')
    
    maint()
    
    #try:
    config.reset_to_defaults()
    #except:
    #    # FIXME except what?
    #    error = ("Could not reset to factory defaults.",
    #                "('factory_reset.py', 'fac_rst_handler')"
    #    errors.err(error)
    
    # Also delete local data files
    for data_path in ['/flash/device_data/', '/flash/datastores/']:
        for file in listdir(data_path):
            #try:
            remove(data_path + file)
            #except OSError:
            #    # Ignore if any issue at all
            #    pass
    
    # Create a flag file to notify cloud.get_data_updates to fetch all data
    # files
    get_all_data_files_flag = '/flash/get_all_data_files.json'
    try:
        with open(get_all_data_files_flag, 'w') as f:
            f.write(dumps(True))
    except:
        # Ignore errors
        pass

    if testing:
        debug("Pretending to reboot")
    else:
        reboot(delay = 3, boot_cause = 'PwrBtn')

maint()

# Setup our listener
fac_rst_pin = config.conf['FACTORY_RESET_PIN']
debug("fac_rst_pin: '" + str(fac_rst_pin) + "'")

#try:
fac_rst_pin_lsnr = Pin(fac_rst_pin, mode = Pin.IN, pull = Pin.PULL_UP)
# FIXME Called repeatedly no matter what I choose. Maybe debounce? Maybe rising
# and falling as before?
fac_rst_pin_lsnr.callback(Pin.IRQ_HIG_LEVEL, _fac_rst_handler)
#except:
#    errors.err("Cannot listen for factory reset button presses.",
#                    "('factory_reset.py', 'main')")