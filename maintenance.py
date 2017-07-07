"""This runs any regular maintenance tasks such as the garbage collector and watchdog feed."""

def maintenance():
    import gc
    from maintenance import maintenance

    maintenance()
    gc.collect()