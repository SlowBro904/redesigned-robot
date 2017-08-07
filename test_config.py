from test_suite import good
from config_class import Config
config = Config('/flash/config.json', '/flash/defaults.json')

test_str = 'Config file updated'

try:
    config.conf['XYZ']
except (NameError, TypeError):
    raise AssertionError("Cannot read the config")

good("config.conf['XYZ'] at the start of the test: '" +
    str(config.conf['XYZ']) + "'")

config.update({'XYZ': test_str})
assert config.conf['XYZ'] == test_str, "Cannot update the config"
good("config.conf['XYZ'] after update: '" + str(config.conf['XYZ']) + "'")

config.update({'XYZ': None})
assert config.conf['XYZ'] is None, "Did not empty the XYZ config"
good("Emptied the XYZ config")

del(config.conf['XYZ'])
config.conf = config.load_config()
assert config.conf['XYZ'] is None, "Cannot load the config from flash"
good("Loaded the config from flash")

config.update({'Nonexistant': None})

assert('Nonexistant' not in config.config, 
    "Should not have updated nonexistant config option 'Nonexistant'")

rename('/flash/config.json', '/flash/config.good.json')
with open('/flash/config.good.json') as d:
    with open('/flash/config.json', 'w') as c:
        c.write(d.read())

try:
    config.update({"XYZ": test_str})
    assert config.conf["XYZ"] == test_str, "config.update()"
    good("config.update()")
    config.reset_to_defaults()
    assert config.conf["XYZ"] == None, "fac_rst failed"
    good("fac_rst")
finally:
    with open('/flash/config.good.json') as g:
        with open('/flash/config.json', 'w') as c:
            c.write(g.read())
    remove('/flash/config.good.json')

config.conf = config.load_config()
assert config.conf['XYZ'] is test_str, "Cannot load the config from flash"
good("Loaded the config from flash")

good("config.conf['XYZ'] at the end of the test: '" +
    str(config.conf['XYZ']) + "'")