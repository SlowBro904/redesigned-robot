def maint():
    '''Run any regular maint tasks such as the garbage collector or 
    watchdog feed
    '''
    import gc
    from wdt import wdt
    
    gc.collect()
    wdt.feed()