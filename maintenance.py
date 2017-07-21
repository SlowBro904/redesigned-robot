def maintenance():
    '''Run any regular maintenance tasks such as the garbage collector
    or watchdog feed
    '''
    try:
        import gc
        from wdt import wdt
        
        wdt.feed()
        gc.collect()
    except ImportError:
        # We must be on a desktop. Ignore.
        pass