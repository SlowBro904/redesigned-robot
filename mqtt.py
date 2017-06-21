class MQTT(object):
    from simple import MQTTClient # FIXME Add exception AdafruitIOError but under what conditions
    from machine import unique_id
    from binascii import hexlify
    from time import sleep
    
    def __init__(self, config):
        """ Setup our MQTT object """
        self.topics = set()
        self.config = config
        
        username    = self.config['MQTT_USERNAME']
        password    = self.config['MQTT_PASSWORD']
        server      = self.config['MQTT_SERVER']
        port        = self.config['MQTT_PORT']
        
        # Use the unique ID for the root path
        self.root_path = hexlify(unique_id())
        
        self.client = self.MQTTClient(username, password, server, port)
        client.settimeout = settimeout # FIXME What?
        self.client.connect()
    
    
    def publish(self, path, message):
        """ Publish a data update to an MQTT path """
        try:
            self.client.publish(self.root_path + path, message)
            self.sleep(1) # TODO Is this necessary?
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