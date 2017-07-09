class MQTT(object):
    from maintenance import maintenance
    
    def __init__(self):
        """Setup our MQTT object"""
        from config import config
        from serial import serial
        from version import version
        # TODO Add exception AdafruitIOError but under what conditions
        from simple import MQTTClient
        
        self.maintenance()
        
        self.topics = set()
        
        port = config['MQTT_PORT']
        server = config['MQTT_SERVER']
        retries = config['MQTT_RETRIES']
        timeout = config['MQTT_TIMEOUT']
        username = config['MQTT_USERNAME']
        password = config['MQTT_PASSWORD']
        device_name = config['DEVICE_NAME']
        
        # Use the device name, the version, and the serial number for the root 
        # path. I'm including the device name and version so that we can have 
        # multiple devices and a newer version does not break the interface for 
        # clients not upgraded yet
        self.root_path = '/'.join([device_name, version, serial])
        
        self.client = MQTTClient(username, password, server, port)
        client.settimeout = timeout
    
    
    def connect(self):
        """Connect to the MQTT broker"""
        self.maintenance()
        self.client.connect()
    
    
    def publish(self, path, message, retries = self.retries):
        """Publish a data update to an MQTT path"""
        # FIXME This demands that every MQTT topic have a value, which I think
        # they always will at least have the most recently published value
        from time import sleep
        self.maintenance()
        
        result = None
        
        # TODO Can I copy this for i in range to a function then pass in the
        # exact function I want to repeat?
        for i in range(retries):
            result = self.client.publish(self.root_path + '/' + path, message)
            sleep(1) # TODO Is this necessary?
            if result:
                break
        
        return result
    
    def get(self, path, retries = self.retries):
        """Gets any current data in an MQTT path"""
        self.maintenance()
        
        result = None
        
        if path not in self.topics:
            self.subscribe(path)
            
        for i in range(retries):        
            result = self.client.receive(path)[1]
            if result:
                break
        
        return result
    
    
    def subscribe(self, path, retries = self.retries):
        """Subscribes to an MQTT path"""
        self.maintenance()
        
        result = None
        
        for i in range(retries):
            result = self.client.subscribe(path)
            if result:
                break
        
        self.topics.add(path)
        return result