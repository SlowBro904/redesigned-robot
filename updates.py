import temp_file
from os import remove
from leds import leds
from errors import ERRORS
from json import load, dump
from maintenance import maintenance

errors = ERRORS()

def get_data_updates(get_all_data_files = False):
    """Get all recent data updates such as new door schedules from our 
    cloud servers.
    
    We can optionally specify which updates to get, whether only the latest
    or all data files if for example we just did a factory reset.
    
    This can also be specified by writing True in JSON format into
    /flash/get_all_data_files.json which will get deleted once read.
    """
    maintenance()
    
    get_all_data_files_flag = '/flash/get_all_data_files.json'
    
    try:
        with open(get_all_data_files_flag) as get_all_data_filesH:
            get_all_data_files = load(get_all_data_filesH)
        
        remove(get_all_data_files_flag)
    except:
        # Does not exist, ignore
        pass

    if get_all_data_files:
        updates = send('get_all_data_files')
    else:
        updates = send('get_latest_data_updates')
    
    if not updates:
        return True
    
    existing_data = dict()
    for update in updates:
        data_file = update[0]
        parameter = update[1]
        # This might be a list
        values = update[2]
        
        maintenance()
        try:
            # Read the original file
            data_file_full_path = '/flash/data/' + data_file
            with open(data_file_full_path) as data_fileH:
                existing_data[data_file] = load(data_fileH)
        except: # TODO Get the precise exception type
            # File doesn't exist yet. We'll create it in memory first.
            existing_data[data_file] = dict()

        existing_data[data_file][parameter] = values
    
    maintenance()
    
    for data_file in existing_data:
        # TODO Change to 'with' and do general Pythonic cleanup everywhere
        with temp_file.create(data_file) as temp_fileH:
            if dump(existing_data[data_file], temp_fileH):
                temp_file.install(temp_fileH, data_file)


def get_system_updates(self):
    """Update the scripts on our system"""
    # Create any new directories
    new_directories = send('get_new_directories')
    
    maintenance()
    
    if new_directories:
        from os import mkdir
        
        for new_directory in new_directories:
            maintenance()
            # exist_ok = True is a counter-intuitively-named flag. If the 
            # parent directory does not exist we will create it first.
            mkdir('/flash/' + new_directory, exist_ok = True)
    
    maintenance()
    
    # Now check for system updates
    updates = send('get_system_updates')
    
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
    web_admin.stop()

    from hashlib import MD5
    
    successfully_updated_files = list()
    
    for update in updates:
        script_file = update[0]
        expected_md5sum = update[1]
        script_contents = update[2]
        new_file = script_file + '.new'
        
        maintenance()
        
        # Create the file as .new and upon reboot our system will see the
        # .new file and delete the existing version, install the new.
        with open('/flash/' + new_file, 'w') as script_fileH:
            script_fileH.writelines(script_contents)
        
        with open('/flash/' + new_file) as script_fileH:
            stored_md5sum = MD5(script_fileH)
        
        if stored_md5sum == expected_md5sum:
            successfully_updated_files.append('/flash/' + script_file)
        else:
            # All or nothing.
            errors.warning('Update failure. Reverting.')
            
            remove(new_file)
            for new_file in successfully_updated_files:
                remove(new_file)

            # Empty the list
            successfully_updated_files = list()

            web_admin.start()
            
            # Stop looping on updates
            break

    leds.blink(run = False)
    
    if successfully_updated_files:
        with open('/flash/updated_files.txt') as updated_filesH:
            successfully_updated_files.writelines()
        
        # Reboot and the system will install any .new files
        # FIXME Test to ensure that boot.py is run on reboot()
        from reboot import reboot
        reboot()