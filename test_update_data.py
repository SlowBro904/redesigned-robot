print("Starting test_updates")
from wifi import mywifi, sta
mywifi = sta()
mywifi.connect()

from ujson import loads
from cloud import CloudCls
from test_suite import good
from os import listdir, remove
from update_data import get_data_updates

cloud = CloudCls()
cloud.connect()

test_data = '/flash/device_data/testing1.json'
try:
    remove(test_data)
except:
    pass

get_data_updates(get_all = True)
files = listdir('/flash/device_data')

check = "get_data_updates() all"
assert 'testing1.json' in files, check
good(check)

with open(test_data) as f:
    contents = loads(f.read())

check = "get_data_updates() all contents"
assert contents['testing1'] == '123', check
good(check)

test_data = '/flash/device_data/testing2.json'
try:
    remove(test_data)
except:
    pass

get_data_updates(get_all = False)
files = listdir('/flash/device_data')

check = "get_data_updates() updates"
assert 'testing2.json' in files, check
good(check)

with open(test_data) as f:
    contents = loads(f.read())

check = "get_data_updates() updates contents"
assert contents['testing2'] == '456', check
good(check)