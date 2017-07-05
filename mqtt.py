class MQTT(object):
    def __init__(self):
        """ Setup our MQTT object """
        from config import config
        from serial import serial
        from version import version
        # TODO Add exception AdafruitIOError but under what conditions
        from simple import MQTTClient
        
        self.topics = set()
        
        port = config['MQTT_PORT']
        server = config['MQTT_SERVER']
        timeout = config['MQTT_TIMEOUT']
        username = config['MQTT_USERNAME']
        password = config['MQTT_PASSWORD']
        device_name = config['DEVICE_NAME']
        
        # Use the device name, the version, and the serial number for the root path
        # I'm including the device name and version so that we can have multiple devices and a newer version does not break the interface for clients not upgraded yet
        self.root_path = device_name + '/' + version + '/' + serial
        
        self.client = MQTTClient(username, password, server, port)
        client.settimeout = timeout
    
    
    def connect(self):
        self.client.connect()
    
    
    def publish(self, path, message):
        """ Publish a data update to an MQTT path """
        from time import sleep
        
        try:
            self.client.publish(self.root_path + '/' + path, message)
            sleep(1) # TODO Is this necessary?
            return True
        except:
            return False
    
    
    def get(self, path):
        """ Gets any current data in an MQTT path """
        if path not in self.topics:
            self.subscribe(path)
        
        return self.client.receive(path)[1]
    
    
    def subscribe(self, path):
        """ Subscribes to an MQTT path """
        self.client.subscribe(path)
        self.topics.add(path)