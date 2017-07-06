"""A config module which can be imported into other modules but which is 
specific to this device.

Improves performance by avoiding reloading the config file every time it's
imported. For other devices, change the config file variable below.
"""
from config_class import CONFIG
# FIXME Change to the real filename
config = CONFIG('/flash/sb.cfg', '/flash/sb.defaults.cfg').config