print("Starting test_boot_cause_file")
from ujson import dumps
from test_suite import good

with open('/flash/boot_cause.json', 'w') as f:
    f.write(dumps('Aux'))

import boot_cause
check = 'boot_cause'
assert boot_cause.boot_cause == 'Aux', check
good(check)