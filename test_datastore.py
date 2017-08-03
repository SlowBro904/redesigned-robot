from data_store import DataStore

data_store = DataStore('testing', testing = True, debug = True)

test_value = 'test'

data_store.update(test_value)

# If data_store.update() successfully sends data to the cloud .value will get
# deleted. But in testing we don't send to the cloud.
try:
    data_store.value
except NameError:
    raise AssertionError("data_store.value is not set")

assert test_value in data_store.value, (
    "data_store did not update the value correctly")

print("[SUCCESS] Updating data_store.value")

# Test save/restore from flash
data_store.save_to_flash()
data_store.load_to_memory()

try:
    data_store.value
except NameError:
    raise AssertionError(
        "data_store did not save the value to flash correctly")

assert test_value in data_store.value, ("data_store could not retrieve the ",
                                        "value from flash")

print("[SUCCESS] Saving and retrieving data_store.value")
del(data_store.value)
data_store.clear_save_file()