print("Starting test_motor")
import debugging
from time import sleep
from machine import Pin
from config import config
from motor import MotorCls
from test_suite import good

debug = debugging.printmsg

motor = MotorCls()
up = Pin(config.conf['MOTOR_UP_PIN'], mode = Pin.OUT,
            pull = Pin.PULL_DOWN).value
dn = Pin(config.conf['MOTOR_DN_PIN'], mode = Pin.OUT, 
            pull = Pin.PULL_DOWN).value

check = 'motor.voltage'
assert motor.voltage is not 0, check
good(check)

check = 'motor.run()'
motor.run('dn')
sleep(1)
debug("up(): '" + str(up()) + "'")
debug("dn(): '" + str(dn()) + "'")
assert dn() and not up(), check
good(check)

check = 'motor.stop()'
motor.stop()
assert not up() and not dn(), check
good(check)