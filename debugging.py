# FIXME Set both to False for production
# TODO Maybe this flag is set in a file and if that file is deleted they are
# both False and level = 0?
testing = True
enabled = True
default_level = 0
def printmsg(msg, level = 0):
    '''Prints a debug message'''
    if default_level < level:
        return
    
    if not enabled:
        return

    print("[DEBUG]", str(msg))