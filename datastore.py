from os import remove
from cloud import cloud
from json import dump, load

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
        self.dataset_file = '/flash/datasets/' + dataset + '.json'
        self.dataset = dataset
        debugging.enabled = debug
        self.debug = debugging.printmsg
        self.testing = testing
        
        # Add myself to the registry
        self.registry.append(self)
        
        self.load_to_memory()
        self.save()
    
    
    def update(self, update):
        '''Save the new value either in the cloud or in memory if we cannot 
        connect, so we can save it to flash later with save_all().
        '''
        try:
            self.value.append(update)
        except NameError:
            self.value = [update]
        
        return self.save()
    
    
    def save(self):
        '''If it can be saved to the cloud delete the value in memory'''
        # We need to be able to test this and save to disk
        try:
            if not self.testing:
                # FIXME Retry sends, and what if that fails
                self.cloud.send(self.dataset, self.value)
                del(self.value)
                self.clear_save_file()
        except (RuntimeError, OSError):
            self.save_to_flash()
            del(self.value)
    
    
    def save_to_flash(self):
        with open(self.dataset_file, 'w') as f:
            try:
                f.write(dumps(self.value))
            except NameError:
                # We must have been able to save the value to the cloud
                pass
    
    
    def clear_save_file(self):
        return self.remove(self.dataset_file)
    
    
    def load_to_memory(self):
        '''Loads the saved file (if any) to memory'''
        with open(self.dataset_file, 'w') as f:
            try:
                self.value = loads(f.read())
            except OSError:
                # Ignore if not exist
                pass