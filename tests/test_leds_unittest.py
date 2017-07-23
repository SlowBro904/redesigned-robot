import unittest
from leds import leds
 
class TestLEDs(unittest.TestCase):
    def setUp(self):
        # FIXME Test blink(default = True)
        self.leds.blink(run = True,
                        pattern = (
                        (self.leds.good, True, None),
                        (self.leds.warn, True, None), 
                        (self.leds.err, True, None)),
                        default = False)
    
    
    def test_steady_all(self):
        self.assertEquals(self.leds.good, True)
        self.assertEquals(self.leds.warn, True)
        self.assertEquals(self.leds.err, True)
    
    
    def tearDown(self):
        self.leds.blink(run = False)

if __name__ == '__main__':
    unittest.main()