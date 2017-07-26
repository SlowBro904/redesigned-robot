from leds import leds

# Default
leds.blink(run = True,
                pattern = (
                (leds.good, True, None),
                (leds.warn, True, None), 
                (leds.err, True, None)),
                default = True)

assert leds.good == True, "Cannot set the good LED"
assert leds.warn == True, "Cannot set the warn LED"
assert leds.err == True, "Cannot set the err LED"

print("[SUCCESS] Able to turn on the LEDs as default")
leds.blink(run = False)

# Non-default
leds.blink(run = True,
                pattern = (
                (leds.good, True, None),
                (leds.warn, False, None), 
                (leds.err, False, None)),
                default = False)

assert leds.good == True, "Cannot set the good LED"
assert leds.warn == False, "Cannot set the warn LED"
assert leds.err == False, "Cannot set the err LED"

print("[SUCCESS] Able to turn on the LEDs as non-default")
leds.blink(run = False)

# Should still be on, based on the default
assert leds.good == True, "Cannot set the good LED"
assert leds.warn == True, "Cannot set the good LED"
assert leds.err == True, "Cannot set the good LED"

print("[SUCCESS] The LED default setting works")

leds.blink(run = False,
            pattern = (
            (leds.good, False, None),
            (leds.warn, False, None),
            (leds.err, False, None)),
            default = True)

assert leds.good == False, "Cannot set the good LED"
assert leds.warn == False, "Cannot set the good LED"
assert leds.err == False, "Cannot set the good LED"
print("[SUCCESS] Able to turn off the LEDs")