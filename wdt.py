class WDT(object):
    def __init__(self, timeout = 10000):
        from machine import WDT # TODO Move all imports down into the init where possible
        self.wdt = WDT(timeout)
    
    
    # TODO This won't catch code that's stuck in a loop.
    def feeder_func(delay, id):
        from time import sleep
        while True:
            sleep(delay)
            self.wdt.feed()
    
    
    # TODO How do you kill a thread?
    def start()
        import _thread
        _thread.start_new_thread(feeder_func, 0)
    
    
    def stop(self):
        self.wdt.stop()