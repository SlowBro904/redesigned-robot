class CLOUD(object):
    from mqtt import MQTT
    from json import loads, load, dumps, dump
    from machine import reset
    from uhashlib import MD5
    from os import remove
    import temp_file

    def __init__(config):
        self.mqtt = self.MQTT(config)
    
    
    def ping(self):
        """ Ping the cloud servers, ensure we have complete connectivity """
        if not self.loads(self.send('ping')) == 'ack':
            return False
        
        return True

        
    def send(self, action, message = None):
        """ Send an action and message and get the reply. For example, action = 'door_status', message = 'up' """
        self.mqtt.publish(dumps(action, message))
        return self.mqtt.get(loads(action))
        

    def get_data_updates(self):
        """ Get all recent data updates such as new door schedules from our cloud servers. """
        updates = self.send('get_data_updates')
        
        if not updates:
            return True
        
        existing_data = dict()
        for update in updates:
            data_file           = update[0]
            parameter           = update[1]
            values              = update[2] # This might be a list
            
            try:
                with open('/flash/' + data_file) as json_data:
                    existing_data[data_file] = self.load(json_data)
                else: # FIXME Right?
                    pass
                    # FIXME Create the file here
            except:
                self.warning('Failed_data_updates_cannot_open_' + data_file)
            
            if parameter in existing_data[data_file]:
                existing_data[data_file][parameter] = values
        
        for data_file in existing_data:
            # Read the original file. If we find our parameter mark a flag True and overwrite the value in the temp file.
            # FIXME Change to 'with' and do general Pythonic cleanup
            temp_fileH = self.temp_file.create(data_file)
            self.dump(existing_data[data_file], temp_fileH)
            temp_file.install(temp_fileH, data_file)


    def get_system_updates(self):
        """ Update the scripts on our system """
        updates = self.send('get_system_updates')
        
        if not updates:
            return True
        
        for update in updates:
            script_file     = update[0]
            expected_md5sum = update[1]
            script_contents = update[2]
            new_file        = '/flash/' + script_file + '.new'
            
            try:
                # Create the file as .new and upon reboot our system will see the .new file and delete the existing version, install the new.
                with open(new_file, 'w') as script_fileH:
                    script_fileH.write(row) for row in script_contents
                
                with open(new_file) as script_fileH:
                    stored_md5sum = self.MD5(script_fileH)
                
                if stored_md5sum != expected_md5sum:
                    self.remove(new_file)
                    # FIXME And try again
            except:
                pass # FIXME Right?
        
        self.reset()