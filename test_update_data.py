print("Starting test_updates")
from wifi import mywifi, sta
mywifi = sta()
mywifi.connect()

from test_suite import good
from os import listdir, remove
from update_data import get_data_updates

test_data = '/flash/device_data/testing.json'
try:
    remove(test_data)
except:
    pass

get_data_updates(get_all = True)
# FIXME Coming up empty
files = listdir('/flash/device_data')

check = "get_data_updates() download"
assert 'testing.json' in files, check
good(check)

with open(test_data) as f:
    contents = loads(f.read())

check = "get_data_updates() contents"
assert contents['testing'] == '123', check
good(check)

# FIXME Now test only latest updates