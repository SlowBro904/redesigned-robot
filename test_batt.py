print("Starting test_battery")
from batt import BattCls
from test_suite import good

batt = BattCls()

# TODO Add a test if USB plugged in
# TODO This will be not zero if the ADC is even functional. Would be great if
# we test on fresh batteries with a known value and see that our charge is 
# above that value
check = "battery.charge"
assert batt.charge is not 0, check
good(check)

# FIXME Why would this be None?
check = "check_charge()"
assert batt.check_charge() is None, check
good(check)