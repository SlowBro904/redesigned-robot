'''A config module which can be imported into other modules but which is 
specific to this device.

Improves performance by avoiding reloading the config file every time it's
imported. For other devices, change the config file variable below.
'''
from config_class import Config
from errors import Errors

errors = Errors()

# FIXME Change to the real filename
try:
    config = Config('/flash/sb.json', '/flash/sb.defaults.json').config
except:
    error = "Could not load the config. ('config.py', 'main')"
    errors.hard_error(error)