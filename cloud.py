class CLOUD(object):
    from errors import ERRORS
    from json import loads, dumps
    from maintenance import maintenance
    
    errors = ERRORS()
    
    def __init__(self):
        """Sets up communications with the cloud servers"""
        from mqtt import MQTT
        
        self.maintenance()
        self.mqtt = MQTT()
    
    
    def connect(self):
        """Connect to our MQTT broker"""
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
    
    
    def send(self, topic, message = None, encrypt = True):
        """Send a message to a topic and gets the reply.
        
        For example, topic = 'door_status', message = 'up'
        """
        self.maintenance()
        
        # FIXME Do I need the try/except? If so do I need it elsewhere in this
        # module?
        try:
            self.mqtt.publish(dumps(topic, message, encrypt))
        except:
            # TODO If we get multiple send warnings only record one
            warning = ("Unable to send to the cloud. Topic: '",
                        str(topic) + "', message: '" + str(message) + "'")
            raise RuntimeError(warning)
        
        return self.mqtt.get(loads(topic))