from err import Err
from json import loads, dumps
from maintenance import maint

class Cloud(object):
    def __init__(self):
        '''Sets up communications with the cloud servers'''
        from mqtt import MQTT
        
        self.maint()
        self.mqtt = MQTT()
        self.err = Err()
    
    
    def connect(self):
        '''Connect to our MQTT broker'''
        try:
            return self.mqtt.connect()
        except:
            warning = ("Cannot connect to our MQTT broker.",
                        "('cloud.py', 'connect')")
            self.err.warning(warning)
            return False
    
    
    def ping(self):
        '''Ping the cloud servers, but don't test login or encryption'''
        self.maint()
        try:
            return self.send('ping', login = False, encrypt = False) == 'ack'
        except:
            return False
    
    
    def can_login(self):
        '''Ensure login is functioning'''
        self.maint()
        try:
            return self.send('ping', login = True, encrypt = False) == 'ack'
        except:
            return False
    
    
    def encryption_working(self):
        '''Ensure encryption is functioning'''
        self.maint()
        try:
            return self.send('ping', login = True, encrypt = True) == 'ack'
        except:
            return False
    
    
    def isconnected(self):
        '''Ensure we can ping the cloud, login, and use encryption'''
        try:
            status = self._status
        except NameError:
            self.maint()
            status = (self.ping() and self.can_login() 
                            and self.encryption_working())
    
        self._status = status
        return self._status
    
    
    def send(self, topic, message = None, encrypt = True):
        '''Send a message to a topic and gets the reply.
        
        For example, topic = 'door_status', message = 'up'
        '''
        self.maint()
        
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