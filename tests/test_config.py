from config_class import Config
config = Config('/flash/config.json', '/flash/defaults.json', 
                debug = True)
try:
    config.config['XYZ']
except NameError:
    raise AssertionError("Cannot read the config")
print("config.config['XYZ'] at the start of the test: '" + str(config.config['XYZ']) + "'")
config.update({'XYZ': 'ABC'})
assert config.config['XYZ'] == 'ABC', "Cannot update the config"
print("config.config['XYZ'] after update: '" + str(config.config['XYZ']) + "'")
config.update({'Nonexistant': None})
assert('Nonexistant' not in config.config, 
    "Should not have updated nonexistant config option 'Nonexistant'")
config.update({'XYZ': None})
print("config.config['XYZ'] at the end of the test: '" + str(config.config['XYZ']) + "'")