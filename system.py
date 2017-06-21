class SYSTEM(object):
    attached_devices = set()
    
    def __init__(self, i2c, config):
        self.config = config
        self.i2c = i2c
        self.attached_devices = set()
    
    @property
    def attached_devices(self):
        """ Looks for i2c addresses for devices we certify and appends to a set of attached devices. Ignores any non-certified hardware. """
        if len(self.attached_devices) > 0:
            return True
        
        for address in self.config['CERTIFIED_DEVICE_I2C_ADDRESSES']:
            if self.i2c.query(address):
                self.attached_devices.add(address)