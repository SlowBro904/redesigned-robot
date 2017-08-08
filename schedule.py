import debugging
from os import remove
from err import ErrCls
from json import dumps, loads
from maintenance import maint
from datastore import DataStore

debug = debugging.printmsg
testing = debugging.testing

class Schedule(object):
    def __init__(self, devices):
        '''Sets up scheduled events for our devices'''
        self.status = dict()
        self.schedules = dict()
        self.datastore = DataStore('status')
        
        for device in devices:
            maint()
            
            try:
                device_file = '/flash/device_data/' + device + '.json'
                with open(device_file) as f:
                    self.schedules[device] = loads(f.read())
            except:
                # Ignore errors. If we have zero schedules nothing will run.
                pass
    
    
    @property
    def next_event_time(self):
        '''Look across all schedules for all devices and return the time for
        the next scheduled event for any device'''
        from time import mktime
        
        maint()
        
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
    
    
    def save(self, device):
        '''Takes the current schedule in self.schedules[device] and writes it 
        back to disk
        '''
        maint()
        errors = ErrCls()
        
        device_file = '/flash/device_data/' + device + '.json'
        
        #try:
        with open(device_file, 'w') as f:
            return f.write(dumps(self.schedule[device]))
        #except:
        #    warning = ("Cannot save to flash the schedule for " + device,
        #                "('schedule.py','save')")
        #    errors.warn(warning)
        #    return False
    
    
    def run(self):
        '''Run any events that are due now'''
        from rtc import RTC
        from config import config
        from device_routines import DeviceRoutine
        
        rtc = RTC()
        
        self.maint()
        
        # TODO I might want a per-device retry but quite difficult to implement
        # so let's wait 'til we need it
        device_retries = config.conf['DEVICE_RETRIES']
        
        # Keep re-checking the schedule until we're all clear. What might 
        # happen is we finish an event and the schedule starts for the next 
        # event. We want to keep checking until there are no more items
        # scheduled.
        
        # FIXME Add some kind of expected time buffer on the server so we're
        # not continuously running events and killing our battery. Want a long
        # buffer between events, how about SCHEDULE_BUFFER x 5?
        items_scheduled = False
        while True:
            for device in self.schedules:
                # Add a buffer to avoid a race condition if there is an event
                # that occurs between now and when the system goes to sleep.
                # This addresses a different situation than the while True
                # above.
                stop_time = rtc.now() + config.conf['SCHEDULE_BUFFER']
                
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
                
                self.maint()
                
                # FIXME Do retries in DataStore
                # TODO Does MQTT have built-in retries?
                status = device_routine.run(command, arguments)
                self.datastore.update((device, status))
            
                # Remove everything due (including but not limited to the one
                # we just executed) and write our modified schedule to disk
                for this_event in due:
                    this_event_index = self.schedules[device].index(this_event)
                    self.schedules[device].pop(this_event_index)
                
                self.save(device)
            
            
            # Logic to know when to stop executing the outer while loop. If
            # this never gets set in this for loop we know we have no items
            # scheduled under any device, and so we can exit the while loop
            # as well.
            if not items_scheduled:
                break