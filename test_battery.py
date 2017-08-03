import battery
print("Starting test_battery")
battery = Battery()

# TODO Add a test if USB plugged in
# TODO This will be not zero if the ADC is even functional. Would be great if
# we test on fresh batteries with a known value and see that our charge is 
# above that value
assert battery.charge() is not 0, "Cannot read the battery charge"
print("[SUCCESS] Able to read the battery charge")