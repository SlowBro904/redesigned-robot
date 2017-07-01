class CONFIG(object):
    import temp_file
    from re import search
    from errors import ERRORS
    from json import load, dump
    from os import remove, rename
    
    def __init__(self, config_file, defaults_file = None):
        """
        Provides a dictionary with keys and values coming from the config file's options and values.
        If the config file is unreadable or missing it will load values from the defaults file.
        """
        # TODO See if I can do something like def __dict__(self):, so that config = CONFIG() then when I use the object as a dictionary it shows a dictionary.
        self.config = dict()
        self.config_file = config_file
        self.defaults_file = defaults_file
        self.errors = self.ERRORS()
    
    
    @property
    def config(self):
        """ Fills in the values for the config dict() """
        # FIXME Any other @properties where the value may already be set? Do this there as well.
        # FIXME Test that this works as expected. Don't want to bog down the system fetching from the config file over and over if it's in memory.
        if len(self.config) > 0:
            return None
        
        try:
            config_fileH = open(self.config_file)
        except: # Missing or unreadable
            # TODO Get the exact exception
            self.reset_to_defaults() # TODO What if even this fails
            
            # Retry
            config_fileH = open(self.config_file)
        
        self.config = load(config_fileH)
        config_fileH.close()
    
    
    def reset_to_defaults(self):
        """ Resets the config file to defaults """
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
        
        # Empty this out so that when we fetch it next time it will fill in again. FIXME Test
        self.config = dict()
        defaults_fileH.close()
    
    
    def update(self, updates):
        """ Takes a list of updates (each item is a tuple of parameter and value) and updates the config file with new parameters and values, and also updates the values in memory """
        for parameter, value in updates:
            if parameter not in self.config:
                return False
        
            # Update the value also in memory FIXME Test. I might have to create a config.set(). Does this update the values in an instance or only in the class? Test.
            self.config[parameter] = value
        
        temp_config_fileH = self.create_temp_file(self.config_file)
        
        # Dump our config to the temp file
        self.dump(self.config, temp_config_fileH)
        temp_config_fileH.close()
        
        # Install the temp file
        if not self.install_temp_file(temp_config_fileH, self.config_file):
            warning('Cannot_update_config_file')