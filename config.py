class CONFIG(object):
    from os import remove, rename
    from re import search
    from errors import hard_error, warning
    import temp_file
    
    def __init__(self, config_file, defaults_file):
        """ Provides a dictionary with keys and values coming from the config file's options and values.
        If the config file is unreadable or missing it will load values from the defaults file.
    
        Config file option names must not contain spaces and must be followed by an equal sign. Example:
        WIFI_SECURITY_TYPE = WPA2
        """
        self.config = dict()
        self.config_file = config_file
        self.defaults_file = defaults_file
        return self.config # FIXME This might not work like I want it to.
    
    @property
    def config(self):
        """ Fills in the values for the config dict() """
        if len(self.config) > 0: return True
        
        try: config_fileH = open(self.config_file)
        except: # Missing or unreadable
            # TODO Get the exact exception
            self.reset_to_defaults() # TODO What if even this fails
            
            # Retry
            config_fileH = open(self.config_file)
        
        for row in config_fileH:
            if row.startswith('#'): continue # Skip comments
            if not self.search(r' = ', row): continue # Skip entries lacking an equal sign
            
            param = row.split()[0:]
            self.config[param] = ' '.join(row.split()[2:]) # Everything after the equal sign
            
            # Try to convert to integer if it's convertable
            try self.config[param] = int(self.config[param])
            except: pass

        config_fileH.close()
        
    def reset_to_defaults(self):
        """ Resets the config file to defaults """
        try: self.remove(self.config_file)
        except: self.hard_error() # TODO How would I know there is an issue? Log these somewhere, every hard error. Maybe a medium error.
        
        try: defaults_fileH = open(self.defaults_file)
        except: self.hard_error()
        
        # Write the new config file from the defaults
        config_fileH = open(self.config_file, 'w')
        config_fileH.write(row) for row in defaults_fileH
        config_fileH.close()
        defaults_fileH.close()
        
        self.config = dict() # Empty this out so that when we fetch it next time it will fill in again. FIXME Test
    
    def update(self, parameter, value):
        temp_config_file = 
        temp_config_fileH = temp_file.create(self.config_file)
        
        # Read the original config file. If we find our parameter mark a flag True and overwrite the value in the temp file.
        # FIXME Rewrite with temp_file
        found_parameter = False
        for row in open(self.config_file):
            if self.search(r'^ ' + parameter + ' = ', row):
                found_parameter = True
                temp_config_fileH.write(parameter + ' = ' + value)
            else:
                temp_config_fileH.write(row)
        
        temp_config_fileH.close()
                
        if not found_parameter:
            pass # Ignore if the parameter was not found
        else:
            if not temp_file.install(temp_config_file, self.config_file):
                warning('Cannot_update_config_file')
            
            self.config[parameter] = value # Update the value also in memory FIXME Test. I might have to create a config.set()