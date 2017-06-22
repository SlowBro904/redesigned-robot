""" A device-specific SmartBird config module which can be imported into other modules """
from config_class import CONFIG
config = CONFIG('/flash/smartbird.cfg', '/flash/smartbird.defaults.cfg').config