import _thread
from time import sleep

class ThrTest(object):
    def __init__(self):
        pass
    
    def thread(self, run = True, id = None):
        if run:
            _thread.start_new_thread(self.thr_func, (True, id))
        else:
            self.thr_func(False, id)
    
    
    def thr_func(self, run, id = 0):
        print("id: " + str(id))
        
        global _run
        _run = False
        _run = run
        
        while _run:
            print("Running thread id " + str(id))
            sleep(1)
            if not _run:
                print("Stopping thread id " + str(id))
                _thread.exit()

thr_test = ThrTest()
for id in range(2):
    thr_test.thread(True, id)

sleep(5)
for id in range(2):
    thr_test.thread(False, id)
    sleep(5)