print("Starting test_door_reed_switches")
from test_suite import good
from door_reed_switches import status

# Put a magnet on the dn reed switch
check = 'door_reed_switches.status()'
assert status() == 'dn', check
good(check)