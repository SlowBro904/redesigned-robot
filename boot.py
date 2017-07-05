# Install any new versions of scripts
# FIXME Test upgrading this file, boot.py, as well
from os import listdir, remove, rename

reboot = False

for file in listdir('/flash/'):
    if file.endswith('.new'):
        # Will reboot after installing new files
        reboot = True
        remove('/flash/' + file)
        rename('/flash/' + file + '.new', '/flash/' + file)

if reboot:
    from reboot import reboot
    # Immediate reboot
    delay = 0
    reboot(delay)

import gc
gc.enable()