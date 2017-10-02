from maintenance import maint
from os import remove, rename, listdir, mkdir

def create(target):
    '''Creates a temp file in the format of /flash/tmp/target.tmp and returns a
    file name
    '''
    # FIXME Alter everywhere this is used for the new behavior
    maint()
    # TODO Also if dir
    if not 'tmp' in listdir('/flash'):
        mkdir('/flash/tmp')
    
    # Ignore any preceding path, we're going to create our file in /flash/tmp.
    target_basename = target.split('/')[-1]
    temp_file_name = '/flash/tmp/' + target_basename + '.tmp'
    with open(temp_file_name, 'w') as f:
        f.write('None')
    
    return temp_file_name


def install(temp_file, target):
    '''Takes a temp file and installs the temp file into the target, backing up
    any existing file
    '''
    maint()
    with open(temp_file) as temp_fileH:
        if not target.startswith('/flash/'):
            target = '/flash/' + target
        
        maint()
        
        try:
            # Delete any old backup file TODO Create
            # some way of restoring from backup
            self.remove(target + '.bak')
        except: # TODO Add precise exception reason
            pass # Ignore err if it does not exist.
        
        maint()
        
        try:
            # Create a backup of the current file
            rename(target, target + '.bak')
        except OSError:
            # FIXME Error is exactly 'error renaming file'
            pass
        
        maint()
        
        # Install the temp as the new file
        with open(target, 'w') as f:
            # FIXME Check where I use read() elsewhere if I should instead use
            # readlines().
            for row in temp_fileH.readlines():
                f.write(row)
        
        maint()
        
    remove(temp_file)
    return True