class DEVICE_ROUTINE(object):
    def __init__(self, device):
        """ This sets up an object for the routines of a particular device """
        self.device = device
    
    def run(self, command):
        """ This runs a command for a particular device """
        # By creating a directory structure and manipulating the sys path we can import different routines for different devices
        from sys import path
        from wdt import wdt
        
        root_path = '/flash/device_routines/'
        
        # Example directory name: /flash/device_routines/door/open
        # And inside that directory is routine.py
        path.append('/'.join([root_path, self.device, command]))
        
        from routine import routine
        
        wdt.feed()
        
        # FIXME We might need to create a separate feeder thread here, to prevent long-running routines such as motor control from tripping the wdt.
        return routine()