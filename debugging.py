enabled = False
# TODO Instead of external checks on the level refer to it internally
level = 0
def printmsg(message):
    '''Prints a debug message if debugging is enabled'''
    if enabled:
        print("[DEBUG]", str(message))