from main import config
from machine import Pin, deepsleep
from time import sleep
from wdt import wdt

good_LED = Pin(config['GOOD_LED_PIN'], mode = Pin.OUT)
warning_LED = Pin(config['WARNING_LED_PIN'], mode = Pin.OUT)
error_LED = Pin(config['ERROR_LED_PIN'], mode = Pin.OUT)
warnings = set()

def hard_error():
  error_LED(True)
  sleep(1)
  # TODO Can I combine?
  wdt.feeder().stop()
  wdt.stop()
  deepsleep()

def warning(warning)
  warning_LED_on()
  warnings.add(warning)

def warning_LED_on():
  if warning_LED: return True
  good_LED(False)
  warning_LED(True)
  return True
  
good_LED(True)