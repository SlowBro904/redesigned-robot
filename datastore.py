class DataStore(object):
    # FIXME Everywhere I self.remove() and self.load() get the exact exception 
    # for not found
    # http://docs.micropython.org/en/latest/wipy/library/builtins.html?highlight=builtin%20types#OSError
    from os import remove
    from cloud import cloud
    from json import dump, load
    
    # Keep a list of all objects created
    registry = list()
    
    def __init__(self, dataset, testing = False):
        '''Takes the name of a dataset. When save(update) is issued, save the
        value either to the cloud or if we cannot connect, on the flash for
        uploading later.
        '''
        self.dataset_file = '/flash/datasets/' + dataset + '.json'
        self.dataset = dataset
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
            # FIXME Retry sends, and what if that fails
            self.cloud.send(self.dataset, self.value)
            if self.testing:
                self.save_all()
            else:
                del(self.value)
                self.clear_save_file()
        except (RuntimeError, OSError):
            pass
    
    
    def clear_save_file(self):
        return self.remove(self.dataset_file)
    
    
    def load_to_memory(self):
        '''Loads the saved file (if any) to memory'''
        with open(self.dataset_file, 'w') as dataset_fileH:
            try:
                self.value = self.load(dataset_fileH)
            except OSError:
                # Ignore if not exist
                pass
    
    
    @classmethod
    def save_all(cls):
        '''Save the datasets for all instances of this class to flash'''
        for obj in cls.registry:
            with open(obj.dataset_file, 'w') as dataset_fileH:
                try:
                    cls.dump(obj.value, dataset_fileH)
                    del(obj.value)
                except NameError:
                    # We must have been able to save the value to the cloud
                    pass