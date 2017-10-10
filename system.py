# FIXME Uncomment
#from err import ErrCls
from ujson import loads
from config import config
from maintenance import maint

class SystemCls(object):
    def __init__(self):
        '''Configures our system object which keeps track of certain items
        regarding the system such as the attached devices
        '''
        maint()
        # FIXME Uncomment
        #self.err = ErrCls()
    
    
    @property
    def version(self):
        '''Sets the version number variable based on the version number file'''
        # TODO Also get the sys.* version numbers
        # https://docs.pycom.io/pycom_esp32/library/sys.html
        maint()
        
        #try:
        # FIXME Does the ConfigCls have the ability to add new config items?
        # And if so how do I intend to add them? Some one-off startup script.
        with open(config.conf['VERSION_NUMBER_FILE']) as f:
            return loads(f.read())
        #except:
        #    error = "Cannot get our version number. ('system.py', 'version')"
        #    self.err.error(error)
    
    
    @property
    def serial(self):
        ''' Sets our serial number variable based on the system's unique ID '''
        from binascii import hexlify
        from machine import unique_id

        maint()
        return str(hexlify(unique_id()), 'utf-8')
    
    
    @property
    def attached_devices(self):
        '''Looks for i2c addresses for devices we certify and appends to a set
        of attached devices.
        
        Ignores any non-certified hardware.
        '''
        from i2c import i2c
        maint()
        
        try:
            return self._attached_devices
        except AttributeError:
            self._attached_devices = set()
            
            # We always have at least one door opener and reed switches, which 
            # do not use I2C (just GPIO) so add them here
            self._attached_devices.add('door')
            self._attached_devices.add('door_reed_switches')
            
            cert_addresses = config.conf['CERTIFIED_DEVICE_I2C_ADDRESSES']
            
            for name, addr in cert_addresses.items():
                maint()
                
                try:
                    if i2c.readfrom(addr, 1):
                        self._attached_devices.add(name)
                except OSError:
                    # FIXME And also look for string 'I2C bus error'
                    # Ignore failures, these devices are not attached
                    pass
            
            return self._attached_devices