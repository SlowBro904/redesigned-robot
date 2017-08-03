class DeviceRoutine(object):
    def __init__(self, device):
        '''This sets up an object for the routines of a particular device'''
        from err import ErrCls
        
        self.err = Err()
        self.device = device
    
    def run(self, command, arguments = None):
        '''This runs a command for a particular device.'''
        from maintenance import maint
        
        module = self.device + '.' + command
        routine = __import__(module)
        
        maint()
        
        try:
            return routine(arguments)
        except:
            warning = ("Could not run command " + command + " on device ",
                        device + " with these arguments: '" + str(arguments),
                        "' ('device_routines/__init__.py','run')")
            self.err.warning(warning)
            return False