from config_class import Config
config = Config('/flash/config.json', '/flash/defaults.json', 
                debug = True)

try:
    config.conf['XYZ']
except NameError:
    raise AssertionError("Cannot read the config")

print("[SUCCESS] config.conf['XYZ'] at the start of the test: '" + str(config.conf['XYZ']) + "'")

config.update({'XYZ': 'ABC'})

assert config.conf['XYZ'] == 'ABC', "Cannot update the config"

print("[SUCCESS] config.conf['XYZ'] after update: '" + str(config.conf['XYZ']) + "'")

config.update({'Nonexistant': None})

assert('Nonexistant' not in config.config, 
    "Should not have updated nonexistant config option 'Nonexistant'")

config.update({'XYZ': None})

print("[SUCCESS] config.conf['XYZ'] at the end of the test: '" + str(config.conf['XYZ']) + "'")