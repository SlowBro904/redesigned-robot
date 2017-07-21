class Schedule(object):
    from os import remove
    from json import dump, load
    from maintenance import maintenance
    
    
    def __init__(self, devices):
        '''Sets up scheduled events for our devices'''        
        self.status = dict()
        self.schedules = dict()
        self.status_file = '/flash/data/status.json'
        
        for device in devices:
            self.maintenance()
            
            try:
                with open('/flash/data/' + device + '.json') as device_fileH:
                        self.schedules[device] = self.load(device_fileH)
            except:
                # Ignore errors. If we have zero schedules nothing will run.
                pass
        
        try:
            self.status = self.load_saved_status()
        except:
            # Ignore errors
            pass
    
    
    @property
    def next_event_time(self):
        '''Look across all schedules for all devices and return the time for
        the next scheduled event for any device'''
        from time import mktime
        
        self.maintenance()
        
        next_event = None
        
        for device in self.schedules:
            # Pull off the next scheduled event for this device
            this_event = mktime(self.schedules[device][0]['time'])
            
            if not next_event:
                next_event = this_event
                
                # Next device
                continue
            
            # If the event we're looking at is sooner than our next event
            if this_event < next_event:
                next_event = this_event
        
        return next_event
    
    
    def save_schedule(self, device):
        '''Takes the current schedule in self.schedules[device] and writes it 
        back to disk
        '''
        device_file = '/flash/data/' + device + '.json'
        
        self.maintenance()
        
        try:
            with open(device_file, 'w') as device_fileH:
                return self.dump(self.schedule[device], device_fileH)
        except:
            warning = ("Cannot save to flash the schedule for " + device,
                        "('schedule.py','save_schedule')")
            self.errors.warning(warning)
            return False
    
    
    def save_status(self):
        '''If we cannot connect to the cloud, let's save the status to flash
        for next time we can connect'''
        self.maintenance()
        
        try:
            with open(self.status_file, 'w') as json_data:
                return self.dump(self.status, json_data)
        except:
            warning = "Cannot save the status. ('schedule.py', 'save_status')"
            self.errors.warning(warning)
            return False
    
    
    def load_saved_status(self):
        '''Load the status from flash and delete the file'''
        self.maintenance()
        
        try:
            with open(self.status_file) as status_fileH:
                status = self.load(status_fileH)
        except:
            warning = "Cannot save the status. ('schedule.py', 'save_status')"
            self.errors.warning(warning)
            return False
        
        self.clear_saved_status()
        return status
    
    
    def clear_saved_status(self):
        '''Delete the saved status file'''
        self.maintenance()
        try:
            return self.remove(self.status_file)
        except:
            # Ignore errors
            pass
    
    
    def clear_status(self):
        '''Remove all current status'''
        self.maintenance()
        self.status = dict()
        self.clear_saved_status()
    
    
    def run(self):
        '''Run any events that are due now'''
        from rtc import RTC
        from config import config
        from device_routines import DeviceRoutine
        
        rtc = RTC()
        
        self.maintenance()
        
        # TODO I might want a per-device retry but quite difficult to implement
        # so let's wait 'til we need it
        device_retries = config['DEVICE_RETRIES']
        
        # Keep re-checking the schedule until we're all clear. What might 
        # happen is we finish an event and the schedule starts for the next 
        # event. We want to keep checking until there are no more items
        # scheduled.
        
        # FIXME Add some kind of expected time buffer on the server so we're
        # not continuously running events and killing our battery. Want a long
        # buffer between events, how about Schedule_BUFFER x 5?
        items_scheduled = False
        while True:
            for device in self.schedules:
                # Add a buffer to avoid a race condition if there is an event
                # that occurs between now and when the system goes to sleep.
                # This addresses a different situation than the while True
                # above.
                stop_time = rtc.now() + config['Schedule_BUFFER']
                
                # Get all items scheduled
                all_scheduled_times = self.schedules[device].keys()
                
                # Get only the most recently scheduled item for this device
                due = filter(lambda x: x <= stop_time, all_scheduled_times)[-1]
                item_scheduled = None
                if due:
                    item_scheduled = due[-1]
                
                if item_scheduled:
                    # No schedules, move on to the next device
                    continue
                
                # At least one item was scheduled
                items_scheduled = True
                
                # Get our command and arguments
                this_event = self.schedules[device][item_scheduled]
                command = this_event['command']
                arguments = this_event['arguments']
                
                device_routine = DeviceRoutine(device)
                
                self.maintenance()
                
                status = None
                
                for i in range(device_retries):
                    status = device_routine.run(command, arguments)
                    
                    if status is not None:
                        break
                
                self.status[device] += status
                
                # Remove everything due (including but not limited to the one
                # we just executed) and write our modified schedule to disk
                for this_event in due:
                    this_event_index = self.schedules[device].index(this_event)
                    self.schedules[device].pop(this_event_index)
                
                self.save_schedule(device)
            
            
            # Logic to know when to stop executing the outer while loop. If
            # this never gets set in this for loop we know we have no items
            # scheduled under any device, and so we can exit the while loop
            # as well.
            if not items_scheduled:
                break