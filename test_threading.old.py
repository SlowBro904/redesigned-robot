class Testing(object):
    from err import ErrCls
    
    err = Err()

    def __init__(self):
        try:
            raise ValueError
        except:
            self.err.log_exception(myfile = __file__,
                myclass = self.__class__.__name__,
                myfunc = '__init__',
                myaction = 'Testing exception logging inside a class')

        print("We shouldn't get here.")

def testing():
    from err import ErrCls
    
    err = Err()

    try:
        raise ValueError
    except:
        err.log_exception(myfile = __file__,
            myfunc = 'testing',
            myaction = 'Testing exception logging inside a function')

    print("We shouldn't get here.")