class CLOUD(object):
    from json import loads, dumps
    from maintenance import maintenance
    
    def __init__(self):
        """Sets up communications with the cloud servers"""
        from mqtt import MQTT
        
        self.maintenance()
        self.mqtt = MQTT()
    
    
    def connect(self):
        self.mqtt.connect()
    
    
    def ping(self):
        """Ping the cloud servers, but don't test login or encryption"""
        self.maintenance()
        return self.send('ping', login = False, encrypt = False) == 'ack'
    
    
    def can_login(self):
        """Ensure login is functioning"""
        self.maintenance()
        return self.send('ping', login = True, encrypt = False) == 'ack'
    
    
    def encryption_working(self):
        """Ensure encryption is functioning"""
        self.maintenance()
        return self.send('ping', login = True, encrypt = True) == 'ack'
    
    
    def isconnected(self):
        """Ensure we can ping the cloud, login, and use encryption"""
        self.maintenance()
        return self.ping() and self.can_login() and self.encryption_working()
    
    
    def send(self, action, message = None, encrypt = True):
        """Send an action and message and get the reply.
        
        For example, action = 'door_status', message = 'up'
        """
        self.maintenance()
        
        self.mqtt.publish(dumps(action, message, encrypt))
        return self.mqtt.get(loads(action))