class I2C(object):
    from main import config
    from machine import I2C, Pin
    
    def __init__(self):
      """ Returns an i2c object """
      scl_pin = self.config['I2C_SCL_PIN']
      sda_pin = self.config['I2C_SDA_PIN']
      self.i2c = self.I2C(scl=self.Pin(scl_pin), sda=self.Pin(sda_pin))
      return self.i2c