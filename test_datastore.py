from test_suite import good
from data_store import DataStore

data_store = DataStore('testing', testing = True, debug = True)

test_value = 'test'

data_store.update(test_value)

# If data_store.update() successfully sends data to the cloud .value will get
# deleted. But in testing we don't send to the cloud.
# FIXME After cloud is fixed, send to the cloud as well
try:
    data_store.value
except NameError:
    raise AssertionError("data_store.value is not set")

assert test_value in data_store.value, (
    "data_store did not update the value correctly")

good("Updating data_store.value")

# Test save/restore from flash
DataStore.save_all()
del(data_store)
data_store = DataStore('testing', testing = True, debug = True)

try:
    data_store.value
except NameError:
    raise AssertionError(
        "data_store did not save the value to flash correctly")

msg = "data_store could not retrieve the value from flash"
assert test_value in data_store.value, (msg)
good("Saving and retrieving data_store.value")

del(data_store.value)
data_store._clear_save_file()