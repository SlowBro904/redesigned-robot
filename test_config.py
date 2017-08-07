from test_suite import good
from config_class import Config
config = Config('/flash/config.json', '/flash/defaults.json')

try:
    config.conf['XYZ']
except (NameError, TypeError):
    raise AssertionError("Cannot read the config")

good("config.conf['XYZ'] at the start of the test: '" +
    str(config.conf['XYZ']) + "'")

config.update({'XYZ': 'ABC'})
assert config.conf['XYZ'] == 'ABC', "Cannot update the config"
good("config.conf['XYZ'] after update: '" + str(config.conf['XYZ']) + "'")

config.update({'XYZ': None})
assert config.conf['XYZ'] is None, "Did not empty the XYZ config"
good("Emptied the XYZ config")

del(config.conf['XYZ'])
config.conf = config.load_config()
assert config.conf['XYZ'] is None, "Cannot load the config"
good("Loaded the config from flash")

config.update({'Nonexistant': None})

assert('Nonexistant' not in config.config, 
    "Should not have updated nonexistant config option 'Nonexistant'")

good("config.conf['XYZ'] at the end of the test: '" +
    str(config.conf['XYZ']) + "'")