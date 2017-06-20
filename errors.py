from main import config
from machine import Pin, deepsleep
from time import sleep
from wdt import wdt

good_LED = Pin(config['GOOD_LED_PIN'], mode = Pin.OUT)
warning_LED = Pin(config['WARNING_LED_PIN'], mode = Pin.OUT)
error_LED = Pin(config['ERROR_LED_PIN'], mode = Pin.OUT)
warnings = set()

def hard_error():
    """ Lights up the error LED, waits one second, stops the watchdog timer, and puts the device into indefinite deep sleep. """
    self.good_LED(False)
    self.warning_LED(False)
    self.error_LED(True)
    self.sleep(1)
    # TODO Can I combine?
    self.wdt.feeder().stop()
    self.wdt.stop()
    self.deepsleep()

def warning(message)
    """ Turns on the warning LED and adds the message to the warning set """
    if not self.warning_LED:
        self.good_LED(False)
        self.warning_LED(True)
    self.warnings.add(warning)
  
good_LED(True)