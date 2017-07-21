class Cloud(object):
    from errors import Errors
    from json import loads, dumps
    from maintenance import maintenance
    
    
    def __init__(self):
        """Sets up communications with the cloud servers"""
        from mqtt import MQTT
        
        self.maintenance()
        self.mqtt = MQTT()
        self.errors = Errors()
    
    
    def connect(self):
        """Connect to our MQTT broker"""
        try:
            return self.mqtt.connect()
        except:
            warning = ("Cannot connect to our MQTT broker.",
                        "('cloud.py', 'connect')")
            self.errors.warning(warning)
            return False
    
    
    def ping(self):
        """Ping the cloud servers, but don't test login or encryption"""
        self.maintenance()
        try:
            return self.send('ping', login = False, encrypt = False) == 'ack'
        except:
            return False
    
    
    def can_login(self):
        """Ensure login is functioning"""
        self.maintenance()
        try:
            return self.send('ping', login = True, encrypt = False) == 'ack'
        except:
            return False
    
    
    def encryption_working(self):
        """Ensure encryption is functioning"""
        self.maintenance()
        try:
            return self.send('ping', login = True, encrypt = True) == 'ack'
        except:
            return False
    
    
    def isconnected(self):
        """Ensure we can ping the cloud, login, and use encryption"""
        try:
            status = self._status
        except NameError:
            self.maintenance()
            status = self.ping() and self.can_login() 
                            and self.encryption_working()
    
        self._status = status
        return self._status
    
    
    def send(self, topic, message = None, encrypt = True):
        """Send a message to a topic and gets the reply.
        
        For example, topic = 'door_status', message = 'up'
        """
        self.maintenance()
        
        # TODO What if we only had a temporary burp at startup?
        if not self.isconnected():
            raise RuntimeError
        
        try:
            self.mqtt.publish(dumps(topic, message, encrypt))
        except:
            # TODO If we get multiple send warnings only record one
            warning = ("Unable to send to the cloud. Topic: '",
                        str(topic) + "', message: '" + str(message) + "'")
            raise RuntimeError(warning)
        
        return self.mqtt.get(loads(topic))

# end of class Cloud(object)

cloud = Cloud()