class DeviceRoutine(object):
    def __init__(self, device):
        '''This sets up an object for the routines of a particular device'''
        from errors import Errors
        
        self.errors = Errors()
        self.device = device
    
    def run(self, command, arguments = None):
        '''This runs a command for a particular device.'''
        from maintenance import maintenance
        
        module = self.device + '.' + command
        routine = __import__(module)
        
        maintenance()
        
        try:
            return routine(arguments)
        except:
            warning = ("Could not run command " + command + " on device ",
                        device + " with these arguments: '" + str(arguments),
                        "' ('device_routines/__init__.py','run')")
            self.errors.warning(warning)
            return False