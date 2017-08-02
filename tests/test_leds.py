import leds
from time import sleep
print("Starting test_leds")
leds = leds.LEDs(debug = True, debug_level = 0)

leds.LED('good', default = True)
assert leds.good.value() is 1, "Cannot set the good LED"
assert leds.warn.value() is 0, "Cannot set the warn LED"
assert leds.err.value() is 0, "Cannot set the err LED"
print("[SUCCESS] Set the good LED")

leds.LED()
assert leds.good.value() is 1, "Cannot set the good LED"
assert leds.warn.value() is 0, "Cannot set the warn LED"
assert leds.err.value() is 0, "Cannot set the err LED"
print("[SUCCESS] Back to the default")

leds.LED('warn')
assert leds.good.value() is 0, "Cannot set the good LED"
assert leds.warn.value() is 1, "Cannot set the warn LED"
assert leds.err.value() is 0, "Cannot set the err LED"
print("[SUCCESS] Set the warn LED")

leds.LED()
leds.LED('err')
assert leds.good.value() is 0, "Cannot set the good LED"
assert leds.warn.value() is 0, "Cannot set the warn LED"
assert leds.err.value() is 1, "Cannot set the err LED"
print("[SUCCESS] Set the err LED")

leds.LED()
assert leds.good.value() is 1, "Cannot set the good LED"
assert leds.warn.value() is 0, "Cannot set the warn LED"
assert leds.err.value() is 0, "Cannot set the err LED"
print("[SUCCESS] Back to the default")

leds.LED(default = True)
assert leds.good.value() is 0, "Cannot set the good LED"
assert leds.warn.value() is 0, "Cannot set the warn LED"
assert leds.err.value() is 0, "Cannot set the err LED"
print("[SUCCESS] All off")


# Old code that does not currently work.
# # Default
# leds.blink(run = True,
                # pattern = (
                # (leds.good, True, None),
                # (leds.warn, True, None), 
                # (leds.err, True, None)),
                # default = True, id = 1)

# sleep(5)
# assert leds.good.value() is 1, "Cannot set the good LED"
# assert leds.warn.value() is 1, "Cannot set the warn LED"
# assert leds.err.value() is 1, "Cannot set the err LED"

# print("[SUCCESS] Able to turn on the LEDs as default")
# leds.blink(run = False, id = 2)

# # Non-default
# leds.blink(run = True,
                # pattern = (
                # (leds.good, True, None),
                # (leds.warn, False, None), 
                # (leds.err, False, None)),
                # default = False, id = 3)

# sleep(5)
# assert leds.good.value() is 1, "Cannot set the good LED"
# assert leds.warn.value() is 0, "Cannot set the warn LED"
# assert leds.err.value() is 0, "Cannot set the err LED"

# print("[SUCCESS] Able to turn on the LEDs as non-default")
# leds.blink(run = False, id = 4)

# # Should still be on, based on the default
# sleep(5)
# assert leds.good.value() is 1, "Cannot set the good LED"
# assert leds.warn.value() is 1, "Cannot set the warn LED"
# assert leds.err.value() is 1, "Cannot set the err LED"

# print("[SUCCESS] The LED default setting works")

# leds.blink(run = False,
            # pattern = (
            # (leds.good, False, None),
            # (leds.warn, False, None),
            # (leds.err, False, None)),
            # default = True, id = 5)

# sleep(5)
# assert leds.good.value() is 0, "Cannot set the good LED"
# assert leds.warn.value() is 0, "Cannot set the warn LED"
# assert leds.err.value() is 0, "Cannot set the err LED"
# print("[SUCCESS] Able to turn off the LEDs")