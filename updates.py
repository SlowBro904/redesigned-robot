import debugging
import temp_file
import web_admin
from os import mkdir
from leds import leds
from err import ErrCls
from cloud import cloud
from reboot import reboot
from uhashlib import sha512
from system import SystemCls
from os import remove, rename
from maintenance import maint
from ujson import loads, dumps

err = ErrCls()
system = SystemCls()
debug = debugging.printmsg
testing = debugging.testing

file_list = '/flash/file_list.json'
updated_files_list = '/flash/updated_files.json'

debug("updates.py cloud.isconnected(): '" + str(cloud.isconnected()) + "'")

def get_data_updates(get_all = False):
    '''Get recent data updates such as new door schedules from our 
    cloud servers.
    
    We can optionally specify which updates to get, whether only the latest
    or all data files if for example we just did a factory reset.
    
    This can also be specified by writing True in JSON format into
    /flash/get_all_data_files.json which will get deleted once read.
    '''
    # FIXME If our schedule is incomplete for some reason error/warn
    maint()
    
    get_all_flag = '/flash/get_all_data_files.json'
    
    try:
        with open(get_all_flag) as f:
            get_all = loads(f.read())
        
        remove(get_all_flag)
    except OSError:
        # Does not exist, ignore
        pass
    
    try:
        if get_all:
            updates = cloud.send('get_data_updates', 'all')
        else:
            updates = cloud.send('get_data_updates', 'latest')
    except RuntimeError as warning:
        err.warning(warning + " ('updates.py', 'get_data_updates')")
        return False
    
    if not updates:
        return True
    
    existing_data = dict()
    for update in updates:
        data_file, parameter, value = update
        
        maint()
        
        # FIXME Actually how about just data? Simpler. Do recursive search.
        full_path = '/flash/device_data/' + data_file
        try:
            # Read the original file
            with open(full_path) as f:
                existing_data[data_file] = loads(f.read())
        except OSError:
            # File doesn't exist yet. We'll create it in memory first.
            existing_data[data_file] = dict()
        
        existing_data[data_file][parameter] = values
    
    maint()
    
    for data_file in existing_data:
        # TODO Do general Pythonic cleanup everywhere
        try:
            with temp_file.create(data_file) as f:
                if f.write(dumps(existing_data[data_file])):
                    temp_file.install(f, data_file)
        except OSError:
            warning = ("Failed to get data updates.",
                        " ('updates.py', 'get_data_updates')")
            err.warning(warning)


def _clean_failed_sys_updates(new_files):
    '''Cleans up failed system updates. All or nothing.'''
    # Even though we are in the _clean_failed_sys_updates() function, this
    # would only be called from the get_sys_updates() function.
    warning = ("Update failure. Reverting.",
                "('updates.py', 'get_sys_updates'")
    err.warning(warning)
    
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
    # FIXME Wrap wiith except RuntimeError
    return system.version() == cloud.send('curr_client_ver')


def new_dirs(server_dirs)
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
    for file, expected_sha in server_files:
        file = '/flash/' + file
        try:
            open(file)
        except: # FIXME Except what
            new_files.append(file)
            # Don't need to check anything else, go to the next file
            continue
        
        stored_sha = sha512()
        with open('/flash/' + file) as f:
            for chunk in iter(lambda: f.read(4096), b""):
                stored_sha.update(chunk)
            stored_sha.digest()

        if stored_sha != expected_sha:
            new_files.append(file)

    return new_files


def get_sys_updates():
    '''Update the scripts on our system'''    
    maint()
    
    if curr_client_ver():
        with open(file_list) as f:
            file_list_contents = f.read()
    else:
        # We are out of date
        file_list_contents = cloud.send('get_file_list')
        
        with open(file_list, 'w') as f:
            f.write(file_list_contents)
    
    server_dirs = file_list_contents[1]
    
    new_dirs = new_dirs(server_dirs)
    for new_dir in new_dirs:
        maint()
        #try:
        # The exist_ok = True flag is counter-intuitively named. If the parent
        # directory does not exist we will create it first, similar to the -p
        # flag in Unix mkdir.
        mkdir('/flash/' + new_dir, exist_ok = True)
        #except:
        #    warning = ("Unable to create new directory ", new_dir,
        #                " ('updates.py', 'get_new_dirs')")
        #    err.warning(warning)
    
    new_files = check_files(file_list_contents[2])
    if not new_files:
        return None
    
    # Stop the web admin daemon
    #try:
    web_admin_started = web_admin.status() 
    web_admin.stop()
    #except:
    #    pass
    
    successfully_updated_files = list()
    
    for file in new_files:
        maint()
        
        contents, expected_sha = cloud.send('get_file', file)
        new_file = file + '.new'
        
        try:
            # Create the file as .new and upon reboot our system will see the
            # .new file and delete the existing version, install the new.
            with open('/flash/' + new_file, 'w') as f:
                for row in contents:
                    f.write(row)
        except: # FIXME except what?
            _clean_failed_sys_updates(new_files)
            
            # Empty the list
            successfully_updated_files = list()
            break
        
        stored_sha = sha512()
        with open('/flash/' + new_file) as f:
            for chunk in iter(lambda: f.read(4096), b""):
                stored_sha.update(chunk)
        
        stored_sha = stored_sha.hexdigest()
        
        if stored_sha == expected_sha:
            successfully_updated_files.append(file)
        else:
            _clean_failed_sys_updates(new_files)
            
            # Empty the list
            successfully_updated_files = list()
            break
    
    if web_admin_started:
        web_admin.start()
    
    # TODO Not working
    #leds.blink(run = False)
    leds.LED('default')
    
    if successfully_updated_files:
        try:
            with open(updated_files_list) as f:
                f.write(dumps(successfully_updated_files))
        except: # FIXME except what?
            _clean_failed_sys_updates(new_files)
        
        # Reboot and the system will install any .new files. At boot we'll run
        # install_updates().
        # FIXME Ensure I set the boot cause same as this boot. If I booted to
        # the web admin I want to ensure the web admin comes up again.
        reboot()


def install_updates():
    '''Install any recent updates. Typically runs at boot.'''
    # FIXME Test upgrading this file (updates.py) as well
    # FIXME This probably isn't necessary. I'll bet we can update files without
    # first rebooting. Update on the fly then reboot then proceed. Yeah I think
    # I want to remove this because LED() goes back to black on reboot. Maybe
    # one day retain that setting at boot but now now. Simpler.
    maint()
    reboot = False
    
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
                remove('/flash/' + file)
            except OSError: # FIXME Get the exact exception type
                # Ignore if it does not exist
                pass
            
            rename('/flash/' + file + '.new', '/flash/' + file)
    
    maint()
    
    try:
        remove(updated_files_list)
    except OSError: # FIXME Get the exact exception type
        # Ignore if it does not exist
        pass
    
    if testing:
        do_reboot = False
    
    if do_reboot:    
        reboot()