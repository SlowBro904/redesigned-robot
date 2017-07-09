class CLOUD(object):
    import temp_file
    from os import remove
    from errors import ERRORS
    from maintenance import maintenance
    from json import loads, load, dumps, dump
    
    def __init__(self):
        """Sets up communications with the cloud servers"""
        from mqtt import MQTT
        
        self.maintenance()
        self.mqtt = MQTT()
        
        self.errors = self.ERRORS()
    
    
    def connect(self):
        self.mqtt.connect()
    
    
    def isconnected(self):
        """Ping the cloud servers, ensure we have complete connectivity"""
        self.maintenance()
        return self.send('ping') == 'ack'
    
    
    def send(self, action, message = None):
        """Send an action and message and get the reply.
        
        For example, action = 'door_status', message = 'up'
        """
        self.maintenance()
        
        self.mqtt.publish(dumps(action, message))
        return self.mqtt.get(loads(action))
    
    
    def get_data_updates(self, get_all_data_files = False):
        """Get all recent data updates such as new door schedules from our 
        cloud servers.
        
        We can optionally specify which updates to get, whether only the latest
        or all data files if for example we just did a factory reset.
        
        This can also be specified by writing True into
        /flash/get_all_data_files.txt which will get deleted once read.
        """
        self.maintenance()
        
        get_all_data_files_flag = '/flash/get_all_data_files.txt'
        with open(get_all_data_files_flag) as get_all_data_filesH:
            if get_all_data_files.read().strip() == 'True':
                get_all_data_files = True
        
        try:
            remove(get_all_data_files_flag)
        except:
            # Does not exist, ignore
            pass

        if get_all_data_files:
            updates = self.send('get_all_data_files')
        else:
            updates = self.send('get_latest_data_updates')
        
        if not updates:
            return True
        
        existing_data = dict()
        for update in updates:
            data_file = update[0]
            parameter = update[1]
            # This might be a list
            values = update[2]
            
            self.maintenance()
            try:
                # Read the original file
                data_file_full_path = '/flash/data/' + data_file
                with open(data_file_full_path) as data_fileH:
                    existing_data[data_file] = self.load(data_fileH)
            except: # TODO Get the precise exception type
                # File doesn't exist yet. We'll create it in memory first.
                existing_data[data_file] = dict()

            existing_data[data_file][parameter] = values
        
        self.maintenance()
        
        for data_file in existing_data:
            # TODO Change to 'with' and do general Pythonic cleanup everywhere
            with self.temp_file.create(data_file) as temp_fileH:
                if self.dump(existing_data[data_file], temp_fileH):
                    self.temp_file.install(temp_fileH, data_file)
    
    
    def get_system_updates(self):
        """Update the scripts on our system"""
        # Create any new directories
        new_directories = self.send('get_new_directories')
        
        self.maintenance()
        
        if new_directories:
            from os import mkdir
            
            for new_directory in new_directories:
                self.maintenance()
                # exist_ok = True is a counter-intuitively-named flag. If the 
                # parent directory does not exist we will create it first.
                mkdir('/flash/' + new_directory, exist_ok = True)
        
        self.maintenance()
        
        # Now check for system updates
        updates = self.send('get_system_updates')
        
        if not updates:
            return None
        
        # Signal that we are doing stuff
        errors.flash_LEDs(['warn', 'error'], 'start')
        
        # FIXME Ensure we install /flash/version.txt via the server
        
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
            
            self.maintenance()
            
            # Create the file as .new and upon reboot our system will see the
            # .new file and delete the existing version, install the new.
            with open('/flash/' + new_file, 'w') as script_fileH:
                script_fileH.writelines(script_contents)
            
            with open('/flash/' + new_file) as script_fileH:
                stored_md5sum = self.MD5(script_fileH)
            
            if stored_md5sum == expected_md5sum:
                successfully_updated_files.append('/flash/' + script_file)
            else:
                # All or nothing.
                self.errors.warning('Update failure. Reverting.')
                
                self.remove(new_file)
                for new_file in successfully_updated_files:
                    self.remove(new_file)

                # Empty the list
                successfully_updated_files = list()

                web_admin.start()
                
                # Stop looping on updates
                break

        errors.flash_LEDs(['warn', 'error'], 'stop')
        
        if successfully_updated_files:
            with open('/flash/updated_files.txt') as updated_filesH:
                successfully_updated_files.writelines()
            
            # Reboot and the system will install any .new files
            # FIXME Test to ensure that boot.py is run on reboot()
            from reboot import reboot
            reboot()