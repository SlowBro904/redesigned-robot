""" A config module which can be imported into other modules but which is specific to this device. For other devices, change the config file. """
from config_class import CONFIG
config = CONFIG('/flash/sb.cfg', '/flash/sb.defaults.cfg').config