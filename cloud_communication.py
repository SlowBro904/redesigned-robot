from main import wifi
from main import mqtt
from json import loads, load, dumps, dump
import temp_file 

# TODO Can I do if wifi?

def ping_cloud():
    if not wifi.isconnected():
        return False
        
    if not loads(send('ping')) == 'ack':
        return False
    
    return True

    
def send(action, message = None):
    if not wifi.isconnected():
        return False
    
    mqtt.publish(dumps(action, message))
    return mqtt.get(loads(action))
    

def get_data_updates():
    if not wifi.isconnected():
        return False
    
    updates = send('get_data_updates')
    
    if not updates:
        return True
    
    existing_data = dict()
    for update in updates:
        data_file           = update[0]
        parameter           = update[1]
        values              = update[2] # This might be a list
        
        try:
            with open('/flash/' + data_file) as json_data:
                existing_data[data_file] = load(json_data)
            else: # FIXME Right?
                pass
                # FIXME Create the file here
        except:
            warning('Failed_data_updates_cannot_open_' + data_file)
        
        if parameter in existing_data[data_file]:
            existing_data[data_file][parameter] = values
    
    for data_file in existing_data:
        # Read the original file. If we find our parameter mark a flag True and overwrite the value in the temp file.
        # FIXME Change to 'with' and do general Pythonic cleanup
        temp_fileH = temp_file.create(data_file)
        dump(existing_data[data_file], temp_fileH)
        temp_file.install(temp_fileH, data_file)


def update_system():
    if not wifi.isconnected():
        return False
    
    updates = send('get_system_updates')
    
    if not updates:
        return True
    
    for update in updates:
        script_file     = update[0]
        script_contents = update[1]
        
        try:
            # Create the file as .new and upon reboot our system will see the .new file and delete the existing version, install the new.
            with open('/flash/' + script_file + '.new', 'w') as script_fileH:
                for row in script_contents:
                    script_fileH.write(row)
        except:
            pass # FIXME Right?