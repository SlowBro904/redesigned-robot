import debugging
#from err import ErrCls
from mqtt import MQTTCls
from maintenance import maint
from ujson import loads, dumps

debug = debugging.printmsg
testing = debugging.testing

class CloudCls(object):
    def __init__(self):
        '''Sets up communications with the cloud servers'''
        maint()
        #self.err = ErrCls()
        self.mqtt = MQTTCls()
    
    
    def connect(self):
        '''Connect to our MQTT broker'''
        #try:
        return self.mqtt.connect()
        #except:
        #    warning = ("Cannot connect to our MQTT broker.",
        #                "('cloud.py', 'connect')")
        #    self.err.warning(warning)
        #    return False
    
    
    def can_login(self):
        '''Ensure login is functioning'''
        maint()
        #try:
        return self.send('ping', encrypt = False) == 'ack'
        #except:
        #    return False
    
    
    def encryption_working(self):
        '''Ensure encryption is functioning'''
        maint()
        #try:
        return self.send('ping', encrypt = True) == 'ack'
        #except:
        #    return False
    
    
    def isconnected(self):
        '''Ensure we can ping the cloud, login, and use encryption'''
        maint()
        try:
            status = self._status
        except AttributeError:
            status = (self.can_login() and self.encryption_working())
        
        self._status = status
        return self._status
    
    
    def send(self, topic, message = None, encrypt = True):
        '''Send a message to a topic and gets the reply.
        
        For example, topic = 'door_status', message = 'up'
        '''
        maint()
        
        # FIXME What if we only had a temporary burp at startup?
        if not self.isconnected():
            raise RuntimeError
        
        # FIXME Get the exact exception type on failure so we 
        # can raise a RuntimeError
        #try:
        self.mqtt.publish(topic, dumps(message), encrypt)
        #except:
        #    # TODO If we get multiple send warnings only record one
        #    warning = ("Unable to send to the cloud. Topic: '",
        #                str(topic) + "', message: '" + str(message) + "'")
        #    raise RuntimeError(warning)
        
        # FIXME be aware that mqtt.get() returns a byte object
        return mqtt.get(loads(topic))

# end of class CloudCls(object)

cloud = CloudCls()