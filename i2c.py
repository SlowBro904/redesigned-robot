""" Sets up the i2c object for importing into other modules """
from config import config
from machine import I2C, Pin
from maintenance import maintenance

maintenance()

scl_pin = config['I2C_SCL_PIN']
sda_pin = config['I2C_SDA_PIN']

i2c = I2C(scl = Pin(scl_pin), sda = Pin(sda_pin))