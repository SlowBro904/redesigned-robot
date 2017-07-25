class System(object):
    from err import Err
    from config import config
    from maintenance import maint
    
    def __init__(self):
        '''Configures our system object which keeps track of certain items
        regarding the system such as the attached devices
        '''
        from i2c import i2c
        
        self.err = Err()
        
        self.maint()
        
        self.i2c = i2c
        self.attached_devices = set()
        
        # We always have at least one door opener and reed switches, which do
        # not use I2C (just GPIO) so add them here
        self.attached_devices.add('door')
        self.attached_devices.add('door_reed_switches')
    
    
    @property
    def version(self):
        '''Sets the version number variable based on the version number file'''
        # TODO Also get the sys.* version numbers
        # https://docs.pycom.io/pycom_esp32/library/sys.html
        from json import load
        
        self.maint()
        
        # FIXME Change the version number file to JSON format, it's currently
        # plain text
        try:
            with open(self.config.conf['VERSION_NUMBER_FILE']) as versionH:
                return load(versionH)
        except:
            error = "Cannot get our version number. ('system.py', 'version')"
            self.err.error(error)
    
    
    @property
    def serial(self):
        ''' Sets our serial number variable based on the system's unique ID '''
        from binascii import hexlify
        from machine import unique_id

        self.maint()
        return str(hexlify(unique_id()), 'utf-8')
    
    
    @property
    def attached_devices(self):
        '''Looks for i2c addresses for devices we certify and appends to a set
        of attached devices.
        
        Ignores any non-certified hardware.
        '''
        self.maint()
        
        # TODO Does this work?
        if self.attached_devices:
            return True
        
        attached_devices = set()
        certified_addresses = self.config.conf['CERTIFIED_DEVICE_I2C_ADDRESSES']
        
        # TODO See where else I should use iteritems()
        for name, address in certified_addresses.iteritems():
            self.maint()
            
            try:
                if self.i2c.readfrom(address, 1):
                    attached_devices.add(name)
            except: # TODO Get exact exception type
                # Ignore failures, these devices are not attached
                pass
        
        return attached_devices