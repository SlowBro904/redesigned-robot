from main import config
from machine import Pin, deepsleep
from time import sleep
from wdt import wdt

good_LED = Pin(config['GOOD_LED_PIN'], mode = Pin.OUT)
warn_LED = Pin(config['WARN_LED_PIN'], mode = Pin.OUT)
error_LED = Pin(config['ERROR_LED_PIN'], mode = Pin.OUT)
warnings = set()

def hard_error():
    """ Turns on the error LED, waits one second, stops the watchdog timer, and puts the device into indefinite deep sleep. """
    good_LED(False)
    warn_LED(False)
    error_LED(True)
    sleep(1)
    # TODO Can I combine?
    wdt.feeder().stop()
    wdt.stop()
    deepsleep()


def warning(message)
    """ Turns on the warning LED and adds the message to the warning set """
    if not warn_LED:
        good_LED(False)
        warn_LED(True)
    
    warnings.add(warning)