def maintenance():
    '''Run any regular maintenance tasks such as the garbage collector or 
    watchdog feed
    '''
    import gc
    from wdt import wdt
    
    wdt.feed()
    gc.collect()