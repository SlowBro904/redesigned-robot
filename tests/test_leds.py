from leds import leds

# Default
leds.blink(run = True,
                pattern = (
                (leds.good, True, None),
                (leds.warn, True, None), 
                (leds.err, True, None)),
                default = True)

assert leds.good == True
assert leds.warn == True
assert leds.err == True
leds.blink(run = False)

# Non-default
leds.blink(run = True,
                pattern = (
                (leds.good, True, None),
                (leds.warn, True, None), 
                (leds.err, True, None)),
                default = False)
leds.blink(run = False)

# Should still be on, based on the default
assert leds.good == True
assert leds.warn == True
assert leds.err == True