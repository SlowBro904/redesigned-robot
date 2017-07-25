'''A config module which can be imported into other modules but which is 
specific to this device.

Improves performance by avoiding reloading the config file every time it's
imported. For other devices, change the config file variable below.
'''
#from err import Err
from config_class import Config

#err = Err()

#try:
config = Config('/flash/config.json', '/flash/defaults.json')
#except:
#    error = "Could not load the config. ('config.py', 'main')"
#    #err.error(error)