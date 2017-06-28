class CLOUD(object):
    from json import loads, load, dumps, dump
    from machine import reset
    from uhashlib import MD5
    from os import remove
    from wdt import wdt
    from temp_file import create as create_temp_file, install as install_temp_file
    
    def __init__(self):
        """ Sets up communications with the cloud servers """
        from mqtt import MQTT
        from config import config
        self.wdt.feed()
        self.mqtt = MQTT(config)
    
    
    def ping(self):
        """ Ping the cloud servers, ensure we have complete connectivity """
        self.wdt.feed()
        return self.loads(self.send('ping')) == 'ack'
    
    
    def send(self, action, message = None):
        """ Send an action and message and get the reply. For example, action = 'door_status', message = 'up' """
        self.wdt.feed()
        
        self.mqtt.publish(dumps(action, message))
        return self.mqtt.get(loads(action))
    
    
    def get_data_updates(self):
        """ Get all recent data updates such as new door schedules from our cloud servers. """
        self.wdt.feed()
        
        updates = self.send('get_data_updates')
        
        if not updates:
            return True
        
        existing_data = dict()
        for update in updates:
            data_file           = update[0]
            parameter           = update[1]
            values              = update[2] # This might be a list
            
            self.wdt.feed()
            try:
                with open('/flash/' + data_file) as json_data:
                    existing_data[data_file] = self.load(json_data)
                else: # FIXME Right?
                    pass
                    # FIXME Create the file here
            except:
                self.warning('Failed data updates. Cannot open ' + data_file)
            
            if parameter in existing_data[data_file]:
                existing_data[data_file][parameter] = values
        
        self.wdt.feed()
        
        for data_file in existing_data:
            # Read the original file. If we find our parameter mark a flag True and overwrite the value in the temp file.
            # FIXME Change to 'with' and do general Pythonic cleanup
            temp_fileH = self.create_temp_file(data_file)
            self.dump(existing_data[data_file], temp_fileH)
            self.install_temp_file(temp_fileH, data_file)
    
    
    def get_system_updates(self):
        """ Update the scripts on our system """
        # Create any new directories
        new_directories = self.send('get_new_directories')
        
        self.wdt.feed()
        
        if new_directories:
            from os import mkdir
            
            for new_directory in new_directories:
                self.wdt.feed()
                try: # FIXME Does this work for nested subdirectories or do we need to create parents first? Like Linux mkdir -p
                    mkdir('/flash/' + new_directory)
                except:
                    pass # FIXME No. But not sure yet what to do.
        
        self.wdt.feed()
        
        # Now check for system updates
        updates = self.send('get_system_updates')
        
        if updates:
            for update in updates:
                script_file     = update[0]
                expected_md5sum = update[1]
                script_contents = update[2]
                new_file        = '/flash/' + script_file + '.new'
                
                self.wdt.feed()
                
                try:
                    # Create the file as .new and upon reboot our system will see the .new file and delete the existing version, install the new.
                    with open(new_file, 'w') as script_fileH:
                        map(script_fileH.write, script_contents)
                    
                    with open(new_file) as script_fileH:
                        stored_md5sum = self.MD5(script_fileH)
                    
                    if stored_md5sum != expected_md5sum:
                        self.remove(new_file)
                        # FIXME And try again
                except:
                    pass # FIXME Right?
            
            self.reset()