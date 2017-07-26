import debugging
from os import remove
#from cloud import cloud
from ujson import dumps, loads

class DataStore(object):
    # FIXME Everywhere I self.remove() and self.load() get the exact exception 
    # for not found
    # http://docs.micropython.org/en/latest/wipy/library/builtins.html?highlight=builtin%20types#OSError
    
    # Keep a list of all objects created
    registry = list()
    
    def __init__(self, dataset, debug = False, testing = False):
        '''Takes the name of a dataset. When save(update) is issued, save the
        value either to the cloud or if we cannot connect, on the flash for
        uploading later.
        '''
        self.dataset_file = '/flash/my_data_store/' + dataset + '.json'
        self.dataset = dataset
        debugging.enabled = debug
        self.debug = debugging.printmsg
        self.testing = testing
        
        # Add myself to the registry
        self.registry.append(self)
        
        self.load_to_memory()
        self.save()
    
    
    def update(self, update):
        '''Add the new value and either upload to the cloud or if we cannot
        connect, save to the flash
        '''
        self.debug("Going to update the value with: " + str(update))
        try:
            self.debug("Updating value")
            self.value.append(update)
        except NameError:
            self.debug("Initializing value")
            self.value = [update]
        
        return self.save()
    
    
    def save(self):
        '''If it can be saved to the cloud delete the value in memory'''
        # We need to be able to test this and save to disk
        try:
            if not self.testing:
                self.debug("Sending to the cloud")
                # FIXME Retry sends, and what if that fails
                self.cloud.send(self.dataset, self.value)
                del(self.value)
                self.clear_save_file()
        except RuntimeError:
            # Stay in memory for now to save to flash later
            self.debug("Didn't send the value to the cloud")
    
    
    def save_to_flash(self):
        with open(self.dataset_file, 'w') as f:
            try:
                self.debug("Saving to flash")
                f.write(dumps(self.value))
                del(self.value)
            except NameError:
                # We must have been able to save the value to the cloud
                pass
    
    
    def clear_save_file(self):
        self.debug("Clearing the save file")
        try:
            return remove(self.dataset_file)
        except:
            # Ignore if missing
            pass
    
    
    def load_to_memory(self):
        '''Loads the saved file (if any) to memory'''
        try:
            self.debug("Loading to memory")
            with open(self.dataset_file) as f:
                self.value = loads(f.read())
            self.debug("Loaded")
            self.clear_save_file()
        except (OSError, ValueError):
            # FIXME Look for exact OSError and 'syntax error in JSON'
            
            # Doesn't exist yet. Initialize.
            self.debug("Cannot load from flash, initializing")
            self.value = list()
    
    
    def save_all(cls):
        '''Saves all objects in the registry to flash'''
        for obj in cls.registry:
            obj.save_to_flash()