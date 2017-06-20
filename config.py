class CONFIG(object):
    from os import remove, rename
    from re import search
    from errors import hard_error, warning
    from json import load, dump
    import temp_file
    
    def __init__(self, config_file, defaults_file):
        """ Provides a dictionary with keys and values coming from the config file's options and values.
        If the config file is unreadable or missing it will load values from the defaults file.
        """
        self.config = dict()
        self.config_file = config_file
        self.defaults_file = defaults_file
        return self.config # FIXME This might not work like I want it to. Test.
    
    @property
    def config(self):
        """ Fills in the values for the config dict() """
        if len(self.config) > 0: return True
        
        try:
            config_fileH = open(self.config_file)
        except: # Missing or unreadable
            # TODO Get the exact exception
            self.reset_to_defaults() # TODO What if even this fails
            
            # Retry
            config_fileH = open(self.config_file)
        
        try:
            self.config = load(config_fileH)
            config_fileH.close()
            return True
        except:
            config_fileH.close()
            return False
        
    def reset_to_defaults(self):
        """ Resets the config file to defaults """
        # TODO I think I want to use 'with' here
        try:
            # FIXME Ensure the defaults file is in json format. At the moment it's in Python.
            defaults_fileH = open(self.defaults_file)
        except:
            self.hard_error()
        
        try:
            self.remove(self.config_file)
        except:
            self.hard_error() # TODO How would I know there is an issue? Log these somewhere, every hard error. Maybe a medium error.
        
        try:
            config_fileH = open(self.config_file, 'w')
        except:
            self.hard_error()
        
        # Write the new config file from the defaults
        dump(load(defaults_fileH), config_fileH)
        defaults_fileH.close()
        config_fileH.close()
        
        self.config = dict() # Empty this out so that when we fetch it next time it will fill in again. FIXME Test
    
    def update(self, parameter, value):
        """ Updates the config file with new parameter and value, and also updates the value in memory """
        if parameter not in self.config:
            return False
        
        # Update the value also in memory FIXME Test. I might have to create a config.set(). Does this update the values in an instance or only in the class? Test.
        self.config[parameter] = value
        
        temp_config_fileH = self.temp_file.create(self.config_file)
        
        # Dump our config to the temp file
        dump(self.config, temp_config_fileH)
        
        # Install the temp file
        if not self.temp_file.install(temp_config_file, self.config_file):
            warning('Cannot_update_config_file')
            
        temp_config_fileH.close()