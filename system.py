class SYSTEM(object):
    def __init__(self, i2c):
        """Configures our system object which keeps track of certain items
        regarding the system such as the attached devices
        """
        from i2c import i2c
        
        self.i2c = i2c
        self.attached_devices = set()
        
        # We always have at least one door opener, which does not use I2C (just
        # GPIO) so add it here
        self.attached_devices.add('door')
    
    @property
    def attached_devices(self):
        """Looks for i2c addresses for devices we certify and appends to a set
        of attached devices. Ignores any non-certified hardware.
        """
        from config import config
        
        # TODO Does this work?
        if self.attached_devices:
            return True
        
        attached_devices = set()
        certified_addresses = self.config['CERTIFIED_DEVICE_I2C_ADDRESSES']
        
        # TODO See where else I should use iteritems()
        for name, address in certified_addresses.iteritems():
            try:
                if self.i2c.readfrom(address, 1):
                    attached_devices.add(name)
            except: # TODO Get exact exception type
                pass # Ignore failures, these devices are not attached
        
        return attached_devices