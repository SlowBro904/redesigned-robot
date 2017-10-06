# FIXME Failing to import ErrCls for some reason. Comment that out everywhere.

print("Starting test_datastore")
from wifi import mywifi, sta
mywifi = sta()
mywifi.connect()

from test_suite import good
from data_store import DataStore

data_store = DataStore('testing')

test_value = 'test'

data_store.update(test_value)

# If data_store.update() successfully sends data to the cloud .value will get
# deleted. But in testing we don't send to the cloud.
# FIXME After cloud is fixed, send to the cloud as well
check = "data_store.value exists"
try:
    data_store.value
except NameError:
    raise AssertionError(check)
good(check)

check = "data_store.value is correct"
assert test_value in data_store.value, (check)
good(check)

# Test save/restore from flash
DataStore.save_all()
del(data_store)
data_store = DataStore('testing')

check = "data_store saved the value to flash"
try:
    data_store.value
except NameError:
    raise AssertionError(check)
good(check)

check = "Saving and retrieving data_store.value"
assert test_value in data_store.value, check
good(check)

# TODO See how to automate this
print("Now check the server to ensure our data arrived")

del(data_store.value)
data_store._clear_save_file()