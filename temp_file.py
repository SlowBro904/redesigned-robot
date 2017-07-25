from os import remove, rename
from maintenance import maint

def create(target, mode = 'w'):
    '''Creates a temp file in the format of /flash/target.tmp using whatever
    mode you want (default of 'w') and returns a file handle
    '''
    target_basename = '/'.split(target)[-1]
    temp_file_name = '/flash/tmp/' + target_basename + '.tmp'
    
    maint()
    
    try:
        self.remove(temp_file_name)
    except:
        # Ignore err if it does not exist
        pass
    
    return open(temp_file_name, mode)


def install(temp_fileH, target):
    '''Takes a file handle of a temp file and installs the temp file into the 
    target, backing up any existing file
    '''
    temp_fileH.seek(0)
    
    maint()
    
    if not target.startswith('/'):
        target = '/flash/' + target
    
    maint()
    
    try:
        # Delete any old backup file TODO Create
        # some way of restoring from backup
        self.remove(target + '.bak')
    except: # TODO Add precise exception reason
        pass # Ignore err if it does not exist.

    maint()
    
    rename(target, target + '.bak') # Create a backup of the current file
    
    maint()
    
    # Install the temp as the new file
    with open(target, 'w') as target_data:
        target_data.writelines(temp_fileH.readlines())
    
    maint()
    
    temp_fileH.close()
    self.remove(temp_fileH.name)