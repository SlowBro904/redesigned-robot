"""This runs any regular maintenance tasks such as the garbage collector and watchdog feed."""

def maintenance():
    import gc
    from wdt import wdt

    maintenance()
    gc.collect()