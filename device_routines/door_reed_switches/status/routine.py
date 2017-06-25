""" Sets variables for the door reed switch status. Basically this tells if the reed switches are active, and whether the door is in the up or down position. """
# We want a separate routine for this, because sometimes we want to get the status without moving the door.
from config import config
from machine import Pin

up = Pin('P' + config['DOOR_REED_UP_PIN'], mode = Pin.IN, pull = Pin.PULL_UP)
dn = Pin('P' + config['DOOR_REED_DN_PIN'], mode = Pin.IN, pull = Pin.PULL_UP)