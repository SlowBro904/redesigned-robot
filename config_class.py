class CONFIG(object):
    import temp_file
    from os import remove
    from json import load, dump
    
    def __init__(self, config_file, defaults_file):
        """Provides a dictionary with keys and values coming from the config
        file's options and values.
        
        If the config file is unreadable or missing it will load values from the
        defaults file.
        """
        self.config = load_config()
        self.config_file = config_file
        self.defaults_file = defaults_file
    
    
    def load_config(self):
        """Loads the config file from flash into memory.
        
        If it doesn't exist it will copy the defaults file into place as the new
        config file and load from that.
        """
        try:
            config_fileH = open(self.config_file)
        except: # Missing or unreadable
            # TODO Get the exact exception
            # TODO What if even this fails
            self.reset_to_defaults()
            
            # Retry
            config_fileH = open(self.config_file)
        
        config = self.load(config_fileH)
        config_fileH.close()
        return config
    
    
    def reset_to_defaults(self):
        """Resets the config file to defaults"""
        # FIXME After clearing out the local get the latest data updates from
        # the server
        with open(self.defaults_file) as defaults_fileH:
            defaults = self.load(defaults_fileH)
        
        try:
            self.remove(self.config_file)
        except: # TODO Get the precise exception
            # Ignore if it does not exist
            pass
        
        with open(self.config_file, 'w') as config_fileH:
            # Write the new config file from the defaults
            self.dump(defaults, config_fileH)
        
        self.config = dict()
        defaults_fileH.close()
    
    
    def update(self, updates):
        """Takes a list of updates (each item is a tuple of parameter and value)
        and updates the config file with new parameters and values, and also
        updates the values in memory
        """
        for parameter, value in updates:
            if parameter not in self.config:
                return False
            
            # Update the value also in memory
            self.config[parameter] = value
        
        temp_config_fileH = self.temp_file.create(self.config_file)
        
        # Dump our config to the temp file
        self.dump(self.config, temp_config_fileH)
        temp_config_fileH.close()
        
        # Install the temp file
        if not self.temp_file.install(temp_config_fileH, self.config_file):
            warning('Cannot_update_config_file')