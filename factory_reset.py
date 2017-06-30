""" Listens to our factory reset switch. If it's held down more than five seconds do a reset back to factory settings. """
from machine import Pin, reset
from config import config
from time import sleep

def fac_rst_handler():
    sleep(5)
    
    # If we're still held after 5 seconds
    if fac_rst_pin:
        if config.reset_to_defaults():
            reset()

fac_rst_pin = Pin('P' + config['FACTORY_RESET_PIN'], mode = Pin.IN, pull = Pin.PULL_UP)
fac_rst_pin.callback(Pin.IRQ_FALLING | Pin.IRQ_RISING, fac_rst_handler)