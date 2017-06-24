class SCHEDULE(object):
    from json import dump, load
    from wdt import wdt
    
    schedules = dict()
    status = dict()
    status_file = '/flash/schedule.status.json'
    
    def __init__(self, devices):
        """ Sets up scheduled events for our devices """        
        for device in devices:
            device_file = '/flash/' + device + '.json'
            
            self.wdt.feed()
            
            try:
                with open(device_file) as device_fileH:
                    self.schedules[device] = self.load(device_fileH)
            except:
                pass # FIXME Maybe not
    
    
    def next_event(self):
        """ Look across all schedules for all devices and return the time for the next scheduled event """
        self.wdt.feed()
        
        # FIXME Not working
        return reduce(lambda x: self.schedules)
    
    
    def save_schedule(self, device):
        """ Takes the current schedule in self.schedules[device] and writes it back to disk """
        device_file = '/flash/' + device + '.json'
        
        self.wdt.feed()
        
        with open(device_file, 'w') as device_fileH:
            return self.dump(self.schedule[device], device_fileH)
    
    
    def status(self):
        """ Returns the status, both present and past (if saved) """
        with open(self.status_file) as status_fileH:
            past_status = self.load(status_fileH)

        present_status = self.status
        
        return past_status + present_status
    
    
    def save_status(self):
        """ If we cannot connect to the cloud, let's save the status to flash for next time we can connect. """
        import temp_file
        
        self.wdt.feed()
        
        status_file_basename = self.status_file.split('/')[-1]
        temp_fileH      = temp_file.create(status_file_basename)
        temp_file_name  = temp_fileH.name
        
        self.dump(self.status(), temp_fileH)
        
        temp_fileH.close()
        
        return temp_file.install(temp_file_name, self.status_file)
    
    
    def removed_saved_status(self):
        """ Delete the saved status file. """
        from os import remove
        remove(self.status_file)
    
    
    def run(self):
        """ Run any events that are due now """
        # FIXME If we have a close and open event that we missed only do the latest one. Maybe only do the latest of anything that's overdue.
        from machine import RTC
        from config import config
        from device_routines import DEVICE_ROUTINE
        
        now = RTC.now()
        
        for device in self.schedules:
            # Pop off the next schedule and shorten the list
            next_schedule = self.schedules[device].pop(0)
            
            command = next_schedule['command']
            
            device_routine = DEVICE_ROUTINE(device)
            
            self.wdt.feed()
            if next_schedule['time'] <= now:
                try:
                    self.status[device] = device_routine.run(command)
                except:
                    pass # FIXME Definitely not this but what
                        
            # Write our modified schedule back to disk
            self.save_schedule(device)