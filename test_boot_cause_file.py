print("Starting test_boot_cause_file")
from test_suite import good
from ujson import dumps, loads

with open('/flash/boot_cause.json', 'w') as f:
    f.write(dumps('Aux'))

with open('/flash/boot_cause.json') as f:
    print("[DEBUG] test_boot_cause_file.py boot_cause.json contents: '" +
            loads(f.read()) + "'")

import boot_cause
check = 'boot_cause'
print("[DEBUG] test_boot_cause_file.py boot_cause.boot_cause: '" +
        str(boot_cause.boot_cause) + "'")
assert boot_cause.boot_cause == 'Aux', check
good(check)