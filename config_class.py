import debugging
import temp_file
#from err import Err
from os import remove
from maintenance import maint
from ujson import loads, dumps

class Config(object):
    # TODO How do I handle debugging and testing variables without adding to
    # the constructor?
    def __init__(self, config_file, defaults_file, debug = False, 
                    debug_level = 0):
        '''Provides a dictionary with keys and values coming from the config
        file's options and values.
        
        If the config file is unreadable or missing it will load values from 
        the defaults file.
        '''
        maint()
        debugging.enabled = debug
        debugging.default_level = debug_level
        self.debug = debugging.printmsg
        self.config_file = config_file
        self.defaults_file = defaults_file
        self.conf = self.load_config()
    
    
    def load_config(self):
        '''Loads the config file from flash into memory.
        
        If it doesn't exist it will copy the defaults file into place as the 
        new config file and load from that.
        '''
        maint()
        try:
            open(self.config_file)
            self.debug("Successfully opened our config file")
        except OSError:
            self.debug("Resetting to defaults")
            # TODO What if even this fails
            self.reset_to_defaults()
        
        maint()
        with open(self.config_file) as f:
            self.debug("Reading our config file...")
            if debugging.default_level > 0:
                self.debug("type(f): '" + str(type(f)) + "'")
                self.debug("f: '" + str(f) + "'")
                self.debug("f.read(): '" + str(f.read()) + "'")
                f.seek(0)
                self.debug("Contents: " + str(loads(f.read())))
                f.seek(0)
            
            try:
                return loads(f.read())
            except ValueError:
                # FIXME What? Means we have a corrupt config. I think reset to
                # default and error.
                pass
    
    
    def reset_to_defaults(self):
        '''Resets the config file to defaults'''
        maint()
        with open(self.defaults_file) as f:
            defaults = loads(f.read())
        
        maint()
        try:
            remove(self.config_file)
        except OSError: # TODO Get the precise exception
            # Ignore if it does not exist
            pass
        
        maint()
        with open(self.config_file, 'w') as f:
            # Write the new config file from the defaults
            f.write(dumps(defaults))
        
        self.conf = self.load_config()
    
    
    # TODO I thought I could make this into a setter but was not successful
    def update(self, updates):
        '''Takes a dict of updates and updates the config file with the new
        parameters and values, and also updates the values in memory
        '''
        maint()
        self.debug("Attempting to update our config file")
        
        if not isinstance(updates, dict):
            self.debug("Did not pass a dict()")
            return False
        
        found = False
        for parameter in updates.keys():
            if parameter not in self.conf:
                # Next parameter
                self.debug("Attempted to update the config file with")
                self.debug("a nonexistant parameter '" + str(parameter) + "'")
                continue
        
            # TODO There's an anti-pattern for this...    
            found = True
        
        if not found:
            self.debug("No existing config parameters found in update")
            return False
        
        for parameter, value in updates.items():
            self.conf[parameter] = value
        
        maint()
        # Update the config file
        #try:
        with open(self.config_file, 'w') as f:
            self.debug("Updating our config file on flash")
            # FIXME Also backup the config file and/or get temp file working,
            # I don't want some error leaving us without a config
            f.write(dumps(self.conf))
            #except:
            #    warning = ("Cannot update config file",
            #                "('config_class.py','update')")
            #    self.err.warning(warning)
        
            # Install the temp file
            #temp_file.install(f, self.config_file)
            #    warning = ("Cannot update config file",
            #                "('config_class.py','update')")
            #    self.err.warning(warning)
            # TODO Delete the temp file
        
        # Update the values in memory from flash
        self.conf = self.load_config()
        self.debug("New config: " + str(self.conf), level = 1)