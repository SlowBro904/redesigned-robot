class CLOUD(object):
    import temp_file
    from wdt import wdt
    from os import remove
    from errors import ERRORS
    from json import loads, load, dumps, dump
    
    def __init__(self):
        """ Sets up communications with the cloud servers """
        from mqtt import MQTT
        
        self.wdt.feed()
        self.mqtt = MQTT()
        
        self.errors = self.ERRORS()
    
    
    def connect(self):
        self.mqtt.connect()
    
    
    def isconnected(self):
        """ Ping the cloud servers, ensure we have complete connectivity """
        self.wdt.feed()
        return self.send('ping') == 'ack'
    
    
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
            data_file = update[0]
            parameter = update[1]
            # This might be a list
            values = update[2]
            
            self.wdt.feed()
            try:
                # Read the original file
                with open('/flash/schedules/' + data_file + '.json') as json_data:
                    existing_data[data_file] = self.load(json_data)
            except: # TODO Get the precise exception type
                # File doesn't exist yet. We'll create it in memory first.
                existing_data[data_file] = dict()

            existing_data[data_file][parameter] = values
        
        self.wdt.feed()
        
        for data_file in existing_data:
            # TODO Change to 'with' and do general Pythonic cleanup
            with self.temp_file.create(data_file) as temp_fileH:
                if self.dump(existing_data[data_file], temp_fileH):
                    self.temp_file.install(temp_fileH, data_file)
    
    
    def get_system_updates(self):
        """ Update the scripts on our system """
        # Create any new directories
        new_directories = self.send('get_new_directories')
        
        self.wdt.feed()
        
        if new_directories:
            from os import mkdir
            
            for new_directory in new_directories:
                self.wdt.feed()
                # exist_ok = True is a counter-intuitively-named flag. If the parent directory does not exist we will create it first.
                mkdir('/flash/' + new_directory, exist_ok = True)
        
        self.wdt.feed()
        
        # Now check for system updates
        updates = self.send('get_system_updates')
        
        if not updates:
            return None
        
        # FIXME Ensure we install /flash/version.txt
        
        from machine import reset
        from uhashlib import MD5
        
        successfully_updated_files = list()
        
        for update in updates:
            script_file = update[0]
            expected_md5sum = update[1]
            script_contents = update[2]
            new_file = script_file + '.new'
            
            self.wdt.feed()
            
            # Create the file as .new and upon reboot our system will see the .new file and delete the existing version, install the new.
            with open('/flash/' + new_file, 'w') as script_fileH:
                script_fileH.writelines(script_contents)
            
            with open('/flash/' + new_file) as script_fileH:
                stored_md5sum = self.MD5(script_fileH)
            
            if stored_md5sum == expected_md5sum:
                successfully_updated_files.append('/flash/' + new_file)
            else:
                # All or nothing.
                self.errors.warning('Update failure. Reverting.')
                
                self.remove(new_file)
                for updated_file in successfully_updated_files:
                    self.remove(updated_file)

        # Reboot and the system will install any .new files
        # FIXME Test to ensure that boot.py is run on reset()
        reset()