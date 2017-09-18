print("Starting test_reboot")
from os import remove
from time import sleep
from ujson import loads
from reboot import reboot
from test_suite import good

check = 'reboot()'
print("Should get '[DEBUG] Simulating reboot' on the next line.")
reboot()

sleep(3)
check = 'boot_cause'
reboot(boot_cause = 'Testing')
boot_cause_file = '/flash/boot_cause.json'
with open(boot_cause_file) as f:
    boot_cause = loads(f.read())
remove(boot_cause_file)
assert boot_cause == 'Testing', check
good(check)