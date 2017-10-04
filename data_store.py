import debugging
from os import remove
from cloud import CloudCls
from ujson import dumps, loads

cloud = CloudCls()
debug = debugging.printmsg
testing = debugging.testing

class DataStore(object):
    # FIXME Everywhere I self.remove() and self.load() get the exact exception 
    # for not found
    # http://docs.micropython.org/en/latest/wipy/library/builtins.html?highlight=builtin%20types#OSError
    
    # Keep a list of all objects created
    registry = list()
    
    def __init__(self, dataset):
        '''Takes the name of a dataset. When save(update) is issued, save the
        value either to the cloud or if we cannot connect, on the flash for
        uploading later.
        '''
        self.dataset_file = '/flash/datastores/' + dataset + '.json'
        
        # Add myself to the registry
        DataStore.registry.append(self)
        
        self._to_memory()
        self.save()
    
    
    def update(self, update):
        '''Add the new value and either upload to the cloud or if we cannot
        connect, save to the flash
        '''
        debug("Going to update the value with: " + str(update))
        try:
            debug("Updating value")
            self.value.append(update)
        except AttributeError:
            debug("Initializing value")
            self.value = [update]
        
        return self.save()
    
    
    def save(self):
        '''If it can be saved to the cloud delete the value in memory'''
        # We need to be able to test this and save to disk
        try:
            if not testing:
                debug("Sending to the cloud")
                # FIXME Retry sends, and what if that fails
                cloud.send(self.dataset, self.value)
                del(self.value)
                self._clear_save_file()
        except RuntimeError:
            # Stay in memory for now to save to flash later
            debug("Didn't send the value to the cloud")
    
    
    def _to_flash(self):
        with open(self.dataset_file, 'w') as f:
            try:
                debug("Saving to flash")
                f.write(dumps(self.value))
                del(self.value)
            except AttributeError:
                # We must have been able to save the value to the cloud
                pass
    
    
    def _to_memory(self):
        '''Loads the saved file (if any) to memory'''
        try:
            debug("Loading data store to memory", level = 1)
            with open(self.dataset_file) as f:
                self.value = loads(f.read())
            debug("Loaded")
            self._clear_save_file()
        except (OSError, ValueError):
            # FIXME Look for exact OSError and 'syntax error in JSON'
            
            # Doesn't exist yet. Initialize.
            debug("Cannot load data store from flash, initializing", level = 1)
            self.value = list()
    
    
    def _clear_save_file(self):
        debug("Clearing the save file")
        try:
            return remove(self.dataset_file)
        except:
            # Ignore if missing
            pass
    
    
    @classmethod
    def save_all(cls):
        '''Saves all objects in the registry to flash'''
        for obj in cls.registry:
            obj._to_flash()