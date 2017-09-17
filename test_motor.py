print("Starting test_motor")
import debugging
from machine import Pin
from config import config
from motor import MotorCls
from test_suite import good

debug = debugging.printmsg

motor = MotorCls()
up = Pin(config.conf['MOTOR_UP_PIN'], mode = Pin.OUT, pull = Pin.PULL_DOWN)
dn = Pin(config.conf['MOTOR_DN_PIN'], mode = Pin.OUT, pull = Pin.PULL_DOWN)

check = 'motor.voltage'
# FIXME Attach a voltage divider to config.conf['MOTOR_VOLT_PIN'] and try again
debug("motor.voltage: '" + str(motor.voltage) + "'")
assert motor.voltage is not 0, check
good(check)

check = 'motor.run()'
motor.run('up')
assert up.value() is True and dn.value() is False, check
good(check)

check = 'motor.stop()'
motor.stop()
assert up.value() is False and dn.value() is False, check
good(check)