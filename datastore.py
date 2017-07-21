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
        self.dataset = dataset
        self.dataset_file = '/flash/datasets/'
        
        # Add myself to the registry
        self.registry.append(self)
        
        # FIXME Add this directory to fac_rst
        with open('/flash/dataset/' + self.dataset, 'w') as dataset_fileH:
            try:
                self.value = self.load(dataset_fileH)
            except OSError:
                # Ignore if it does not exist
                pass
        
        self.save()
    
    
    def update(self, update):
        '''Save the new value either in the cloud or in memory if we cannot 
        connect, so we can save it to flash later with save_all().
        '''
        self.value = update
        self.save()
    
    
    def save(self):
        '''If it can be saved to the cloud delete the value in memory'''
        try:
            self.cloud.send(self.dataset, self.value)
            del(self.value)
            self.clear_saved_file()
        except RuntimeError:
            pass
    
    
    @classmethod
    def save_all(cls):
        '''Save the dataset for all instances of this object to flash'''
        for obj in cls.registry:
            with open(obj.dataset_file, 'w') as dataset_fileH:
                try:
                    cls.dump(obj.value, dataset_fileH)
                except NameError:
                    # We must have been able to save it to the cloud
                    pass
    
    
    def clear_saved_file(self):
        '''Clear out the save file, if it exists. If not, ignore.'''
        try:
            return self.remove(self.dataset_file)
        except OSError:
            pass