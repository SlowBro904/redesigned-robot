import temp_file
# FIXME Uncomment
#from err import ErrCls
from cloud import CloudCls
from maintenance import maint
from ujson import dumps, loads
from uos import listdir, remove

#err = ErrCls()
cloud = CloudCls()
cloud.connect()

def get_data_updates(get_all = False):
    '''Get recent data updates such as new door schedules from our 
    cloud servers.
    
    We can optionally specify which updates to get, whether only the latest
    or all data files if for example we just did a factory reset.
    
    This can also be specified by writing True in JSON format into
    /flash/get_all_data_files.json which will get deleted once read.
    '''
    # TODO If our schedule is incomplete for some reason error/warn
    maint()
    
    get_all_flag = '/flash/get_all_data_files.json'
    
    try:
        with open(get_all_flag) as f:
            get_all = loads(f.read())
        
        remove(get_all_flag)
    except OSError:
        # Does not exist, ignore
        pass
    
    #try:
    if get_all:
        updates = cloud.send('get_data_updates', 'all')
    else:
        updates = cloud.send('get_data_updates', 'latest')
    #except RuntimeError as warning:
    #    err.warning(warning + " ('updates.py', 'get_data_updates')")
    #    return False
    
    if not updates:
        return True
    
    data = dict()
    for data_file, update in updates.items():
        print("[DEBUG] update_data.py get_data_updates() update: '" +
                str(update) + "'")
        
        parameter, value = update
        
        maint()
        
        myfile = '/flash/device_data/' + data_file
        try:
            # Read the original file
            with open(myfile) as f:
                data[data_file] = loads(f.read())
        except OSError:
            # File doesn't exist yet. We'll create it in memory first.
            data[data_file] = dict()
        
        data[data_file][parameter] = value
    
    maint()
    
    print("[DEBUG] update_data.py get_data_updates() data: '" + str(data) + "'")
    
    for data_file in data:
        # TODO Do general Pythonic cleanup and refactor everywhere
        #try:
        #print("[DEBUG] update_data.py temp_file.create(data_file): '" +
        #        str(temp_file.create(data_file)) + "'")
        my_temp = temp_file.create(data_file)
        #print("[DEBUG] update_data.py get_data_updates() my_temp: '" + 
        #        str(my_temp) + "'")
        success = False
        with open(my_temp, 'w') as f:
            if f.write(dumps(data[data_file])):
                #print("[DEBUG] update_data.py get_data_updates() " +
                #        "f.write(dumps(data[data_file])) successful")
                #print("[DEBUG] update_data.py get_data_updates() " +
                #        "listdir('/flash/tmp')" + str(listdir('/flash/tmp')) +
                #        "'")
                success = True
        
        if not success:
            # FIXME Some error somewhere
            remove(my_temp)
        else:
            # TODO Maybe make this an exception
            if temp_file.install(my_temp, 
                '/flash/device_data/' + data_file):
                cloud.send('got_data_update', data_file)
                #print("[DEBUG] update_data.py get_data_updates() " +
                #        "listdir('/flash/device_data')" +
                #        str(listdir('/flash/device_data')) + "'")
        #except OSError:
        #    warning = ("Failed to get data updates.",
        #                " ('updates.py', 'get_data_updates')")
        #    err.warning(warning)