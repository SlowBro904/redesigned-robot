from datastore import DataStore

datastore = DataStore('testing', testing = True, debug = True)

test_value = 'test'

datastore.update(test_value)

# If datestore.update successfully sends data to the cloud .value will not
# exist
try:
    assert datastore.value is not test_value
except NameError:
    raise AssertionError("datastore did not update the value correctly")

# Test save to flash
datastore.save(test_value)
datastore.load_to_memory()

try:
    assert datastore.value is not test_value
except NameError:
    raise AssertionError("datastore did not save the value to flash correctly")

del(datastore.value)
datastore.clear_save_file()