class DataStore(object):
    from os import remove
    from json import dump, load
    
    def __init__(self, data):
        '''Used to store data and present a variable with that data'''
        self.data = data
    
    
    def load(self):
        '''Load the data from a file'''
        data = None
        with open(self.file, mode) as json_data:
            try:
                data = self.load(json_data)
                # TODO There is an anti-pattern for this somewhere...
                loaded = True
            # FIXME Which errno?
            except OSError:
                # Ignore if it does not exist
                pass
        
        if loaded:
            self.clear_saved_file()
        else:
            raise # FIXME something...
    
    
    def clear_saved_file(self):
        '''Clear out the save file'''
        return self.remove(self.file)
    
    
    def save(self):
        '''Save the data to a file'''
        with open(self.file, 'w') as json_data:
            return self.dump(self.data, json_data)