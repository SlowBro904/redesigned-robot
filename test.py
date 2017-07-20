class Testing(object):
    from errors import Errors
    
    errors = Errors()

    def __init__(self):
        try:
            raise ValueError
        except:
            self.errors.log_exception({'file': __file__,
                'class': self.__class__.__name__,
                'func': '__init__',
                'action': 'Testing exception logging inside a class'})

        print("We shouldn't get here.")

def testing():
    from errors import Errors
    
    errors = Errors()

    try:
        raise ValueError
    except:
        errors.log_exception({'file': __file__,
            'func': 'testing',
            'action': 'Testing exception logging inside a function'})

    print("We shouldn't get here.")