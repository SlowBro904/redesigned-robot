'''A config module which can be imported into other modules but which is 
specific to this device.

Improves performance by avoiding reloading the config file every time it's
imported. For other devices, change the config file variable below.
'''
# FIXME Uncomment, and find everywhere it's commented out
#from err import ErrCls
import debugging
from config_class import Config

# FIXME Test config again
# Values we use for testing/debugging
testing = False
debug = debugging.printmsg
debugging.enabled = False
debug_level = 0

#err = Err()

# FIXME Move exception testing into err
#try:
config = Config('/flash/config.json', '/flash/defaults.json')
#except:
#    error = "Could not load the config. ('config.py', 'main')"
#    #err.error(error)