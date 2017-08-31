print("Starting test_boot_cause")
from test_suite import good

import boot_cause
check = 'boot_cause'
assert boot_cause.boot_cause is not None, check
good(check)

print("[DEBUG] boot_cause: " + str(boot_cause.boot_cause))