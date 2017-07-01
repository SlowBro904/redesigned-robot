""" Sets variables for the door reed switch status. Basically this tells if the reed switches are active, and whether the door is in the up or down position. """
from machine import Pin
from config import config

up = Pin('P' + config['DOOR_REED_UP_PIN'], mode = Pin.IN, pull = Pin.PULL_UP)
dn = Pin('P' + config['DOOR_REED_DN_PIN'], mode = Pin.IN, pull = Pin.PULL_UP)