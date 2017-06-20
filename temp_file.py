from os import remove, rename

def create(target, mode = 'w'):
    """ Creates a temp file in the format of /flash/target.tmp using whatever mode you want (default of 'w') and returns a file handle """
    target_basename = '/'.split(target)
    return open('/flash/' + target_basename + '.tmp', mode)

def install(temp_file, target):
    """ Installs the temp file into the target, backing up any existing file """
    try:
        self.remove(target + '.bak') # Delete any old backup file TODO Create some way of restoring from backup
    except:
        pass # Ignore errors. It might not exist.

    try:
        self.rename(target, target + '.bak') # Create a backup of the current file
    except:
        pass # Ignore errors FIXME Do I want to? Probably throw an error to the GUI.

    try:
        self.rename(temp_file, target) # Install the temp as the new config file
    except:
        return False