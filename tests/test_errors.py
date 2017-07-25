from err import Err
from datastore import DataStore
datastore = DataStore('testing', testing = True)
datastore.load_to_memory()
try:
    assert datastore.value is not # FIXME What? Create an event.
except NameError:
    raise AssertionError