# FIXME Test upgrading this file, boot.py, as well
from os import remove, rename

reboot = False

# Install any new versions of scripts
updated_files_listing = '/flash/updated_files.txt'
with open(updated_files_listing) as updated_filesH:
    for file in updated_filesH:
        # Set the flag to reboot after installing new files
        reboot = True
        
        try:
            remove('/flash/' + file)
        except: # TODO Get the exact exception type
            # Ignore if it does not exist
            pass
    
        rename('/flash/' + file + '.new', '/flash/' + file)

if reboot:
    try:
        remove(updated_files_listing)
    except: # TODO Get the exact exception type
        # Ignore if it does not exist
        pass
    
    from reboot import reboot
    reboot(delay = 0)

# Automatic garbage collector
# FIXME Run periodically as well. Maybe do a regular gc.mem_free and if below a certain amount automatically run. This may already do that.
# TODO Combine with wdt for a maintenance() function or something like that.
# FIXME Did I not use wdt anywhere?
import gc
gc.enable()