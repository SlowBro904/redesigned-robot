from leds import leds

# FIXME Test blink(default = True)
leds.blink(run = True,
                pattern = (
                (leds.good, True, None),
                (leds.warn, True, None), 
                (leds.err, True, None)),
                default = False)

assert leds.good == True
assert leds.warn == True
assert leds.err == True
leds.blink(run = False)