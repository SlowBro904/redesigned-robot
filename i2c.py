'''Sets up the i2c object for importing into other modules'''
#from err import ErrCls
#from config import config
from machine import I2C, Pin
from maintenance import maint

maint()
#errors = ErrCls()

# TODO I don't know if we really need to do this. Use the standard I2C pins.
#scl_pin = config.conf['I2C_SCL_PIN']
#sda_pin = config.conf['I2C_SDA_PIN']

# FIXME Uncomment
#try:
#i2c = I2C(0, I2C.MASTER, pins = (scl = Pin(scl_pin), sda = Pin(sda_pin)))
i2c = I2C(0, I2C.MASTER)
#except:
#    error = "Cannot setup the I2C bus. ('i2c.py', 'main')"
#    errors.err(error)