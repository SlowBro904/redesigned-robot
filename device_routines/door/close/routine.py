from config import config
from machine import Pin
from sys import path

path.append('/flash/device_routines/door_reed_switches/status/')

import door_reed_switch_status

door_dn             = door_reed_switch_status.dn
up_motor            = Pin('P' + config['UP_MOTOR_PIN'], mode = Pin.IN, pull = PULL_UP)
dn_motor            = Pin('P' + config['DN_MOTOR_PIN'], mode = Pin.IN, pull = PULL_UP)

dn_motor(True)

while True:
    if door_dn:
        dn_motor(False)
        break