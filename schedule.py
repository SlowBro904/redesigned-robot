class SCHEDULE(object):
    from os import remove
    from json import dump, load
    from maintenance import maintenance
    
    schedules = dict()
    status = dict()
    status_file = '/flash/data/status.json'
    
    def __init__(self, devices):
        """Sets up scheduled events for our devices"""        
        for device in devices:
            self.maintenance()
            
            with open('/flash/data/' + device + '.json') as device_fileH:
                    self.schedules[device] = self.load(device_fileH)
        
        status = self.load_saved_status()
    
    
    @property
    def next_event_time(self):
        """Look across all schedules for all devices and return the time for
        the next scheduled event
        """
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
        """Takes the current schedule in self.schedules[device] and writes it 
        back to disk
        """
        device_file = '/flash/data/' + device + '.json'
        
        self.maintenance()
        
        with open(device_file, 'w') as device_fileH:
            return self.dump(self.schedule[device], device_fileH)
    
    
    def save_status(self):
        """If we cannot connect to the cloud, let's save the status to flash
        for next time we can connect
        """
        self.maintenance()
        
        with open(self.status_file, 'w') as json_data:
            if not self.dump(self.status(), json_data):
                return False
    
    
    def load_saved_status(self):
        """Load the status from flash and delete the file"""
        self.maintenance()
        
        with open(self.status_file) as status_fileH:
            status = self.load(status_fileH)
    
        if status:
            self.clear_saved_status()
        
        return status
    
    
    def clear_saved_status(self):
        """Delete the saved status file"""
        self.maintenance()
        return self.remove(self.status_file)
    
    
    def clear_status(self):
        """Remove all current status"""
        self.maintenance()
        self.status = dict()
        self.clear_saved_status()
    
    
    def run(self):
        """Run any events that are due now"""
        # FIXME If we have a close and open event that we missed only do the
        # latest one. Maybe only do the latest of anything that's overdue.
        from rtc import RTC
        from config import config
        from device_routines import DEVICE_ROUTINE
        
        rtc = RTC()
        
        self.maintenance()
        
        # Keep re-checking the schedule until we're all clear. What might 
        # happen is we finish an event and the schedule starts for the next 
        # event. We want to keep checking until there are no more items
        # scheduled.
        
        # FIXME Add some kind of expected time buffer on the server so we're
        # not continuously running events and killing our battery. Want a long
        # buffer between events, how about SCHEDULE_BUFFER x 5?
        while True:
            item_scheduled = False
            for device in self.schedules:
                # Add a buffer to avoid a race condition if there is an event
                # that occurs between now and when the system goes to sleep.
                # This addresses a different situation than the while True
                # above.
                stop_time = rtc.now() + config['SCHEDULE_BUFFER']
                
                # Get all items scheduled
                all_scheduled_times = self.schedules[device].keys()
                currently_scheduled_times = filter(lambda x: x <= stop_time,
                                                    all_scheduled_times)
                
                # Logic to know when to stop executing the outer while loop. If
                # this never gets set in this for loop we know we have no items
                # scheduled under any device, and so we can exit the while loop
                # as well.
                if currently_scheduled_times:
                    item_scheduled = True
                
                # FIXME On the server, never schedule an event for a device at
                # the same time or this could fail
                for scheduled_time in currently_scheduled_times:
                    # Get our command
                    command = self.schedules[device][scheduled_time]['command']
                    device_routine = DEVICE_ROUTINE(device)
                
                    self.maintenance()
                    
                    # FIXME Am I re-running it if it fails?
                    self.status[device] = device_routine.run(command)
                    
                    # Remove the event just executed and write our modified
                    # schedule to disk
                    self.schedules[device].pop(0)
                    self.save_schedule(device)
            
            # We never encountered any items scheduled in the for loop above
            if not items_scheduled:
                break