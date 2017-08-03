from test_suite import good
from config_class import Config
config = Config('/flash/config.json', '/flash/defaults.json', 
                debug = True, debug_level = 0)

try:
    config.conf['XYZ']
except (NameError, TypeError):
    raise AssertionError("Cannot read the config")

good("config.conf['XYZ'] at the start of the test: '" + str(config.conf['XYZ']) + "'")

config.update({'XYZ': 'ABC'})

assert config.conf['XYZ'] == 'ABC', "Cannot update the config"

good("config.conf['XYZ'] after update: '" + str(config.conf['XYZ']) + "'")

config.update({'Nonexistant': None})

assert('Nonexistant' not in config.config, 
    "Should not have updated nonexistant config option 'Nonexistant'")

config.update({'XYZ': None})

good("config.conf['XYZ'] at the end of the test: '" + str(config.conf['XYZ']) + "'")