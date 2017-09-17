print("Starting test_door_reed_switches")
import debugging
from test_suite import good
from door_reed_switches import status

debug = debugging.printmsg

# Put a magnet on the dn reed switch
check = 'door_reed_switches.status()'
#print("[DEBUG] status(): '" + str(status()) + "'")
assert status() == 'dn', check
good(check)