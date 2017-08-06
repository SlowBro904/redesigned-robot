#import test_suite
#print("Starting test_battery")
#
#batt = BattCls()
#good = test_suite.good
#
# TODO Add a test if USB plugged in
# TODO This will be not zero if the ADC is even functional. Would be great if
# we test on fresh batteries with a known value and see that our charge is 
# above that value
#assert battery.charge() is not 0, "battery.charge()"
#good("battery.charge()")
#assert battery.check_charge() is None, "check_charge()"
#good("check_charge()")