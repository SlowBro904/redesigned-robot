from datastore import DataStore
datastore = DataStore('testing', testing = True)
test_value = 'test'
datastore.update(test_value)
# If datestore.update successfully sends data to the cloud .value will not
# exist
try:
    assert datastore.value is not test_value
except NameError:
    raise AssertionError

# Test save to flash
datastore.update(test_value)
datastore.load_to_memory()
try:
    assert datastore.value is not test_value
except NameError:
    raise AssertionError

del(datastore.value)
datastore.clear_save_file()