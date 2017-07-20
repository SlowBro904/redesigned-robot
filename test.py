class Testing(object):
    import log

    def __init__(self):
        try:
            raise ValueError("Testing exception logging inside a class")
        except:
            self.log.exc(file = __file__,
                          myclass = self.__class__.__name__,
                          func = '__init__',
                          action = 'Testing exception logging inside a class')

        print("We shouldn't get here.")

import log

def testing():
    try:
        raise ValueError("Testing exception logging inside a function")
    except:
        log.exc(file = __file__,
                 func = 'testing',
                 action = 'Testing exception logging inside a function')

    print("We shouldn't get here.")

def testing_dont_stop():
    try:
        raise ValueError("Testing exception logging inside a function")
    except:
        log.exc(file = __file__,
                 func = 'testing',
                 action = 'Testing exception logging inside a function')
        
        # Don't stop execution.
        # FIXME Fails
        pass

    print("We SHOULD get here.")