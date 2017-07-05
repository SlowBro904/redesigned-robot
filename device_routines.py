class DEVICE_ROUTINE(object):
    def __init__(self, device):
        """ This sets up an object for the routines of a particular device """
        self.device = device
    
    def run(self, command):
        """ This runs a command for a particular device """
        # Commented out for now, going to try subpackage instead
        # By creating a directory structure and manipulating the sys path we can import different routines for different devices
        #from sys import path

        from wdt import wdt
        
        # Commented out for now, going to try subpackage instead
        #root_path = '/flash/device_routines/'
        
        # Commented out for now, going to try subpackage instead
        # FIXME Use importlib or something like that instead https://docs.python.org/3/reference/import.html
        # FIXME Try the __import__() below, it may work just fine.
        # Example directory name: /flash/device_routines/door/open
        # And inside that directory is routine.py
        #path.append('/'.join([root_path, self.device, command]))
        
        #from routine import routine
        
        routine = __import__('.'.join['device_routines', self.device, command])
        
        wdt.feed()
        
        # FIXME We might need to create a separate feeder thread here, to prevent long-running routines such as motor control from tripping the wdt.
        return routine()