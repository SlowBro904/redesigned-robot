class MQTT(object):
    def __init__(self):
        """ Setup our MQTT object """
        from config import config
        from binascii import hexlify
        # TODO Add exception AdafruitIOError but under what conditions
        from simple import MQTTClient
        from machine import unique_id
        
        self.topics = set()
        
        username = config['MQTT_USERNAME']
        password = config['MQTT_PASSWORD']
        server = config['MQTT_SERVER']
        port = config['MQTT_PORT']
        timeout = config['MQTT_TIMEOUT']
        
        # Use the unique ID for the root path
        self.root_path = hexlify(unique_id())
        
        self.client = MQTTClient(username, password, server, port)
        client.settimeout = timeout
        self.client.connect()
    
    
    def publish(self, path, message):
        """ Publish a data update to an MQTT path """
        from time import sleep
        
        try:
            self.client.publish(self.root_path + path, message)
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
        try:
            self.client.subscribe(path)
            self.topics.add(path)
            return True
        except:
            return False