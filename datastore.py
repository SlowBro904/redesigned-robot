class DataStore(object):
    # FIXME Everywhere I self.remove() and self.load() get the exact exception 
    # for not found
    # http://docs.micropython.org/en/latest/wipy/library/builtins.html?highlight=builtin%20types#OSError
    from os import remove
    from cloud import cloud
    from json import dump, load
    
    # Keep a list of all objects created
    registry = list()
    
    def __init__(self, dataset):
        '''Takes the name of a dataset. When save(update) is issued, save the
        value either to the cloud or if we cannot connect, on the flash for
        uploading later.
        '''
        # FIXME Add this directory to fac_rst
        self.dataset_file = '/flash/datasets/' + dataset
        self.dataset = dataset
        
        # Add myself to the registry
        self.registry.append(self)
        
        with open(self.dataset_file, 'w') as dataset_fileH:
            try:
                self.value = self.load(dataset_fileH)
            except OSError:
                # Ignore if not exist
                pass
        
        self.save()
    
    
    def update(self, update):
        '''Save the new value either in the cloud or in memory if we cannot 
        connect, so we can save it to flash later with save_all().
        '''
        try:
            self.value.append(update)
        except NameError:
            self.value = [update]
        
        self.save()
    
    
    def save(self):
        '''If it can be saved to the cloud delete the value in memory'''
        try:
            # FIXME Retry sends, and what if that fails
            self.cloud.send(self.dataset, self.value)
            del(self.value)
            self.remove(self.dataset_file)
        except (RuntimeError, OSError):
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