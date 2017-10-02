#import debugging
#import temp_file
#import web_admin
#from leds import leds
#from err import ErrCls
#from reboot import reboot

# FIXME:
############################ ALSO CREATE CLOUD_SIMPLE AND TEST ############################
# Hmm. Why? For saving RAM?

from config import config
from cloud import CloudCls
from uhashlib import sha512
#from system import SystemCls
from ubinascii import hexlify
from maintenance import maint
from ujson import loads, dumps
from os import remove, rename, mkdir

#err = ErrCls()
cloud = CloudCls()
#system = SystemCls()
#debug = debugging.printmsg
#testing = debugging.testing

# TODO If we are not connected umqtt/simple.py gives the following unhelpful
# error:
# File "umqtt/simple.py", line 176, in publish
# AttributeError: 'NoneType' object has no attribute 'write'
cloud.connect()

file_list = '/flash/file_list.json'
updated_files_list = '/flash/updated_files.json'

def _clean_failed_sys_updates(new_files):
    '''Cleans up failed system updates. All or nothing.'''
    # Even though we are in the _clean_failed_sys_updates() function, this
    # would only be called from the get_sys_updates() function.
    #warning = ("Update failure. Reverting.",
    #            "('updates.py', 'get_sys_updates'")
    #err.warning(warning)
    
    # FIXME Also remove new dirs. Don't want to assume it's safe to leave
    # them around.
    for new_file in new_files:
        try:
            remove(new_file)
        except OSError:
            # Ignore if not able to
            pass


def curr_client_ver():
    '''Get the current client version on the server and compare to our version.
    
    If we are current return True, else return False.
    '''
    # FIXME What about updating individual clients? What about one-off client
    # commands?
    # FIXME Wrap with except RuntimeError
    # FIXME Pulled from system.py for simplification
    with open(config.conf['VERSION_NUMBER_FILE']) as f:
        system_version = loads(f.read())
    print("[DEBUG] system_version: '" + str(system_version) + "'")
    print("[DEBUG] cloud.send('curr_client_ver'): '" + 
            str(cloud.send('curr_client_ver')) + "'")
    
    # FIXME Uncomment
    #return system.version == cloud.send('curr_client_ver')
    return system_version == cloud.send('curr_client_ver')


def new_dirs(server_dirs):
    '''Gets any directories we don't have which need to be created'''
    new_dirs = list()
    for dir in server_dirs:
        try:
            open('/flash/' + dir)
        except: # FIXME Except what
            new_dirs.append(dir)
    
    return new_dirs


def new_files(server_files):
    '''Checks the file list to see if anything needs to be updated/repaired'''
    new_files = list()
    for file, expected_sha in server_files.items():
        file = '/flash/' + file
        try:
            open(file)
        except: # FIXME Except what
            new_files.append(file)
            # Don't need to check anything else, go to the next file
            continue
        
        stored_sha = file_sha512(file)
        
        if stored_sha != expected_sha:
            new_files.append(file)
    
    return new_files


def file_sha512(file):
    stored_sha = sha512()
    with open(file, 'rb') as f:
        while True:
            chunk = f.read(4096)
            if not chunk:
                break
            stored_sha.update(chunk)
    
    return hexlify(stored_sha.digest()).decode('utf-8')


def get_sys_updates():
    '''Update the scripts on our system'''    
    maint()
    
    if curr_client_ver():
        return
    
    # FIXME Check shasums of all files on the system at boot. Use this code.
    #try:
    #    with open(file_list) as f:
    #        file_list_contents = loads(f.read())
    #except OSError:
    #    # FIXME Also [Errno 2] ENOENT
    
    file_list_contents = cloud.send('get_file_list')
    with open(file_list, 'w') as f:
        f.write(dumps(file_list_contents))
    
    print("[DEBUG] file_list_contents: '" + str(file_list_contents) + "'")
    print("[DEBUG] type(file_list_contents): '" +
            str(type(file_list_contents)) + "'")
    print("[DEBUG] len(file_list_contents): '" +
            str(len(file_list_contents)) + "'")
    
    for new_dir in new_dirs(file_list_contents[1]):
        print("[DEBUG] Creating new_dir '" + str(new_dir) + "'")
        maint()
        # MicroPython lacks the ability to create the entire path chain with
        # one command. Build the chain creating one directory at a time
        tempdir = '/flash'
        for subdir in new_dir.split('/'):
            maint()
            tempdir += '/' + subdir
            try:
                print("[DEBUG] Creating tempdir '" + str(tempdir) + "'")
                mkdir(tempdir)
            except OSError:
                # FIXME Actual error is OSError: file exists:
                pass
            
            # FIXME Do I want this?
            #try:
            #    mkdir('/flash/' + new_dir)
            #except:
            #    warning = ("Unable to create new directory ", new_dir,
            #                " ('updates.py', 'get_new_dirs')")
            #    err.warning(warning)
    
    if not new_files(file_list_contents[2]):
        return None
    
    # Stop the web admin daemon
    #try:
    #web_admin_started = web_admin.status() 
    #web_admin.stop()
    #except:
    #    pass
    
    successfully_updated_files = list()
    
    print("[DEBUG] new_files(file_list_contents[2]): '" + 
            str(new_files(file_list_contents[2])) + "'")
    
    for myfile in new_files(file_list_contents[2]):
        maint()
        
        # Remove the '/flash' at the head of the file to request
        get_file = '/'.join(myfile.split('/')[2:])
        
        print("[DEBUG] update_sys_simple.py get_sys_updates() file: '" + 
                str(get_file) + "'")
        print("[DEBUG] update_sys_simple.py get_sys_updates() " +
                " cloud.send('get_file', file): '" +
                str(cloud.send('get_file', get_file)) + "'")
        
        contents, expected_sha = cloud.send('get_file', get_file)
        new_file = myfile + '.new'
        
        try:
            # Create the file as .new and upon reboot our system will see the
            # .new file and delete the existing version, install the new.
            with open(new_file, 'w') as f:
                for row in contents:
                    f.write(row)
        except: # FIXME except what?
            print("[DEBUG] Couldn't write new_file '" + str(new_file) + "'")
            _clean_failed_sys_updates(new_files(file_list_contents[2]))
            
            # Empty the list
            successfully_updated_files = list()
            break
        
        stored_sha = file_sha512(new_file)
        
        if stored_sha == expected_sha:
            successfully_updated_files.append(myfile)
        else:
            print("[DEBUG] stored_sha '" + str(stored_sha) + "' "
                    " != expected_sha '" + str(expected_sha) + "'")
            _clean_failed_sys_updates(new_files(file_list_contents[2]))
            
            # Empty the list
            successfully_updated_files = list()
            break
    
    #if web_admin_started:
    #    web_admin.start()
    
    # TODO Not working
    #leds.blink(run = False)
    #leds.LED('default')
    
    if successfully_updated_files:
        try:
            with open(updated_files_list, 'w') as f:
                f.write(dumps(successfully_updated_files))
        except: # FIXME except what?
            _clean_failed_sys_updates(new_files)
        
        # Reboot and the system will install any .new files. At boot we'll run
        # install_updates().
        # FIXME Ensure I set the boot cause same as this boot. If I booted to
        # the web admin I want to ensure the web admin comes up again.
        from reboot import reboot
        reboot()


def install_updates():
    '''Install any recent updates. Typically runs at boot.'''
    # FIXME Test upgrading this file (updates.py) as well
    # FIXME This probably isn't necessary. I'll bet we can update files without
    # first rebooting. Update on the fly then reboot then proceed. Yeah I think
    # I want to remove this because LED() goes back to black on reboot. Maybe
    # one day retain that setting at boot but now now. Simpler.
    maint()
    do_reboot = False
    
    try:
        open(updated_files_list)
    except OSError:
        return
    
    # Install any new versions of scripts
    with open(updated_files_list) as f:
        for file in loads(f.read()):
            # Set the flag to reboot after installing new files
            # TODO I think there is an anti-pattern for this...
            do_reboot = True
            
            maint()
            
            try:
                # FIXME I get nervous deleting current in use system files. At
                # least ensure the .new file really does exist. I don't know a
                # good clean way to back up the old files and revert. Hmm.
                # Anyway before I delete any files check that 100% of new files
                # exist.
                remove(file)
            except OSError: # FIXME Get the exact exception type
                # Ignore if it does not exist
                pass
            
            rename(file + '.new', file)
    
    maint()
    
    try:
        remove(updated_files_list)
    except OSError: # FIXME Get the exact exception type
        # Ignore if it does not exist
        pass
    
    # FIXME Uncomment
    #if do_reboot:
    #    if not testing:
    #        from reboot import reboot
    #        reboot()