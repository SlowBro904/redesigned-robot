enabled = False
default_level = 0
def printmsg(msg, level = 0):
    '''Prints a debug message'''
    if default_level < level:
        return
    
    if not enabled:
        return

    print("[DEBUG]", str(msg))