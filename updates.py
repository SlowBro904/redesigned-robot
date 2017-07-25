import temp_file
from err import Err
from leds import leds
from cloud import Cloud
from reboot import reboot
from json import load, dump
from os import remove, rename
from maintenance import maint

err = Err()
cloud = Cloud()

updated_files_listing = '/flash/updated_files.json'

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
            get_all = load(f.read())
        
        remove(get_all_flag)
    except OSError:
        # Does not exist, ignore
        pass

    try:
        if get_all:
            updates = cloud.send('get_all_data_files')
        else:
            updates = cloud.send('get_latest_data_updates')
    except RuntimeError as warning:
        err.warning(warning + " ('updates.py', 'get_data_updates')")
        return False
    
    if not updates:
        return True
    
    existing_data = dict()
    for update in updates:
        data_file = update[0]
        parameter = update[1]
        # This might be a list
        values = update[2]
        
        maint()
        
        data_file_full_path = '/flash/device_data/' + data_file
        try:
            # Read the original file
            with open(data_file_full_path) as f:
                existing_data[data_file] = load(f.read())
        except OSError:
            # File doesn't exist yet. We'll create it in memory first.
            existing_data[data_file] = dict()
        
        existing_data[data_file][parameter] = values
    
    maint()
    
    for data_file in existing_data:
        # TODO Do general Pythonic cleanup everywhere
        try:
            with temp_file.create(data_file) as f:
                if f.write(dump(existing_data[data_file]):
                    temp_file.install(f, data_file)
        except OSError:
            warning = ("Failed to get data updates.",
                        " ('updates.py', 'get_data_updates')")
            err.warning(warning)


def clean_failed_system_update(updates, successfully_updated_files, 
                                web_admin_started, new_file = None):
    '''Cleans up failed system updates. All or nothing.'''
    # TODO This feels kludgy and tightly coupled.
    import web_admin
    
    # Even though we are in the clean_failed_system_update() function, this
    # would only be called from the get_system_updates() function.
    warning = ("Update failure. Reverting.",
                "('updates.py', 'get_system_updates'")
    err.warning(warning)
    
    for update in updates:
        try:
            if new_file:
                remove(new_file)
        except OSError:
            # Ignore if not able to
            pass
        
        for new_file in successfully_updated_files:
            try:
                remove(new_file)
            except OSError:
                # Ignore if not able to
                pass
        
        if web_admin_started:
            try:
                web_admin.start()
            except:
                # Ignore errors
                pass
        
        leds.blink(run = False)


def get_system_updates():
    '''Update the scripts on our system'''
    try:
        # Create any new directories
        new_directories = send('get_new_directories')
    except RuntimeError as warning:
        err.warning(warning + " ('updates.py', 'get_system_updates')")
    
    maint()
    
    if new_directories:
        from os import mkdir
        
        for new_directory in new_directories:
            maint()
            try:
                # exist_ok = True is a counter-intuitively-named flag. If the 
                # parent directory does not exist we will create it first.
                mkdir('/flash/' + new_directory, exist_ok = True)
            except:
                warning = ("Unable to create new directory ",
                            new_directory,
                            " ('updates.py', 'get_system_updates')")
                err.warning(warning)
    
    maint()
    
    # Now check for system updates
    try:
        updates = send('get_system_updates')
    except RuntimeError as warning:
        err.warning(warning + " ('updates.py', 'get_system_updates')")
        return False
    
    if not updates:
        return None
    
    # Signal that we are doing stuff. Warn/err every 500 ms.
    leds.blink(run = True, pattern = (
                    (leds.warn, True, 500),
                    (leds.warn, False, 0),
                    (leds.err, True, 500),
                    (leds.err, False, 0)))
    
    # FIXME Ensure we always update /flash/version.json via the server
    
    # Stop the web admin daemon
    import web_admin
    try:
        web_admin_started = web_admin.status() 
        web_admin.stop()
    except:
        pass
    
    from hashlib import MD5
    
    successfully_updated_files = list()
    
    for update in updates:
        script_file = update[0]
        expected_md5sum = update[1]
        script_contents = update[2]
        new_file = script_file + '.new'
        
        maint()
        
        try:
            # Create the file as .new and upon reboot our system will see the
            # .new file and delete the existing version, install the new.
            with open('/flash/' + new_file, 'w') as f:
                for row in script_contents:
                    f.write(row)
        except:
            clean_failed_system_update(updates, successfully_updated_files,
                                        web_admin_started)
            
            # Empty the list
            successfully_updated_files = list()
            return False
        
        with open('/flash/' + new_file) as f:
            stored_md5sum = MD5(f)
        
        if stored_md5sum == expected_md5sum:
            successfully_updated_files.append('/flash/' + script_file)
        else:
            clean_failed_system_update(updates, successfully_updated_files,
                                        web_admin_started, new_file)
            
            # Empty the list
            successfully_updated_files = list()
            return False
    
    leds.blink(run = False)
    
    if successfully_updated_files:
        try:
            with open(updated_files_listing) as f:
                f.write(dump(successfully_updated_files))
        except:
            clean_failed_system_update(updates, successfully_updated_files,
                                        web_admin_started)
        
        # Reboot and the system will install any .new files
        # FIXME Test to ensure that boot.py is run on reboot()
        reboot()


def install_updates():
    '''Install any recent updates'''
    # FIXME Test upgrading this file (updates.py) as well
    maint()
    reboot = False
    
    try:
        open(updated_files_listing)
    except OSError:
        return
    
    # Install any new versions of scripts
    with open(updated_files_listing) as f:
        for file in load(f.read()):
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
    
    if do_reboot:
        try:
            maint()
            remove(updated_files_listing)
        except OSError: # FIXME Get the exact exception type
            # Ignore if it does not exist
            pass
        
        reboot()