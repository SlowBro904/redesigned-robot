class MQTT(object):
    from simple import MQTTClient # FIXME Add exception AdafruitIOError but under what conditions
    from machine import unique_id
    from binascii import hexlify
    from main import config # TODO This tightly couples our modules but I can't think of a better alternative. I want to keep main.py clean.
    from time import sleep
    
    def __init__(self, username = None, password = None, server = None, port = None, root_path = None):
        self.topics = set()
        if not username:
            username = config['MQTT_USERNAME']
        
        if not password:
            password = config['MQTT_PASSWORD']
        
        if not server:
            server = config['MQTT_SERVER']
        
        if not port:
            port = config['MQTT_PORT']
        
        if root_path:
            self.root_path = root_path
        else:
            self.root_path = hexlify(unique_id())
        
        self.client = MQTTClient(username, password, server, port)
        client.settimeout = settimeout
        self.client.connect()
    
    def publish(self, path, message):
        try:
            self.client.publish(self.root_path + path, message)
            self.sleep(1) # TODO Is this necessary?
            return True
        except:
            return False
            
    def get(self, path):
        if path not in self.topics:
            self.subscribe(path)
        
        return self.client.receive(path)[1]
    
    def subscribe(self, path):
        try:
            self.client.subscribe(path)
            self.topics.add(path)
            return True
        except:
            return False