def exc(**kwargs):
    """Log uncaught exceptions.
    
    Ugly but functional, since Pycom's WiPy 2.0 (as of version 1.7.6.b1) 
    doesn't seem to have a working sys.print_exception and sys.excepthook is
    completely missing from all MicroPythons.
    
    kwargs is a dict that can optionally include:
    file: The file name such as __file__
    myclass: The class name such as self.__class__.__name__
    func: The function we are in such as '__init__'
    action: A human-readable string describing the action we were taking such
        as "Testing exception logging"
    logfile: Change the log file from the default ('/flash/exceptions.log')
    """
    # TODO Also optionally allow the exception to flow through to stderr
    import sys
    
    logfile = '/flash/exceptions.log'
    if kwargs is not None:
        if 'logfile' in kwargs:
            logfile = kwargs['logfile']
    
    with open(logfile, 'a') as exceptions_log:
        exceptions_log.write('-'*79 + '\n')
        if kwargs is not None:
            if 'file' in kwargs:
                exceptions_log.write('File: ' + str(kwargs['file']) + '\n')
            
            if 'class' in kwargs:
                exceptions_log.write('Class: ' + str(kwargs['class']) + '\n')        
            
            if 'func' in kwargs:
                exceptions_log.write('Function: ' + str(kwargs['func']) + '\n')
            
            if 'action' in kwargs:
                exceptions_log.write('Action: ' + str(kwargs['action']) + '\n')
        
        exc_type = str(sys.exc_info()[0])
        error = str(sys.exc_info()[1]).strip()
        
        exceptions_log.write('Exception type: ' + exc_type + '\n')
        exceptions_log.write('Exception error text: ' + error + '\n')
        # FIXME And what about the exc_num like in OSError?
    sys.exit(1)