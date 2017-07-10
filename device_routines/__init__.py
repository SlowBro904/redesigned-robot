class DEVICE_ROUTINE(object):
    def __init__(self, device):
        """This sets up an object for the routines of a particular device"""
        self.device = device
    
    def run(self, command, arguments = None):
        """This runs a command for a particular device."""
        from maintenance import maintenance
        
        module = self.device + '.' + command
        routine = __import__(module)
        
        maintenance()
        
        return routine(arguments)