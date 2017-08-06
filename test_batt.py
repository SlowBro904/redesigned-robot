from test_suite import good
from batt import BattCls
print("Starting test_battery")

batt = BattCls()

# TODO Add a test if USB plugged in
# TODO This will be not zero if the ADC is even functional. Would be great if
# we test on fresh batteries with a known value and see that our charge is 
# above that value
assert batt.charge is not 0, "battery.charge"
good("battery.charge")
assert batt.check_charge() is None, "check_charge()"
good("check_charge()")