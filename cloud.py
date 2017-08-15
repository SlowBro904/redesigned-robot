import debugging
from err import ErrCls
from mqtt import MQTTCls
from maintenance import maint

debug = debugging.printmsg
testing = debugging.testing

class CloudCls(object):
    def __init__(self):
        '''Sets up communications with the cloud servers'''
        maint()
        self.err = ErrCls()
        self.mqtt = MQTTCls()
        debug("__init__() complete", level = 1)
    
    
    def connect(self):
        '''Connect to our MQTT broker'''
        #try:
        return self.mqtt.connect()
        #except:
        #    warning = ("Cannot connect to our MQTT broker.",
        #                "('cloud.py', 'connect')")
        #    self.err.warning(warning)
        #    return False
    
    
    def ping(self):
        '''Pings the MQTT broker'''
        maint()
        return self.mqtt.ping()
    
    
    def can_login(self):
        '''Ensure login is functioning'''
        maint()
        result = self.send('ping', encrypt = False)
        debug("result: '" + str(result) + "'", level = 1)
        debug("type(result): '" + str(type(result)) + "'", level = 1)
        #try:
        return result is 'ack'
        #except:
        #    return False
    
    
    def encryption_working(self):
        '''Ensure encryption is functioning'''
        maint()
        #try:
        result = self.send('ping', encrypt = True)
        debug("result: '" + str(result) + "'")
        debug("type(result): '" + str(type(result)) + "'")
        #except:
        #    return False
        return result is 'ack'
    
    
    def isconnected(self):
        '''Ensure we can ping the cloud, login, and use encryption'''
        maint()
        try:
            status = self._status
        except AttributeError:
            # FIXME Not using encryption. See note in mqtt.py _decrypt().
            #status = (self.can_login() and self.encryption_working())
            status = self.can_login()
        
        self._status = status
        return self._status
    
    
    def send(self, topic, msg = None, encrypt = True):
        '''Send a message to a topic and gets the reply.
        
        For example, topic = 'door_status', message = 'up'
        '''
        maint()
        debug("topic: '" + str(topic) + "'", level = 0)
        debug("msg: '" + str(msg) + "'", level = 0)
        
        # FIXME What if we only had a temporary burp at startup?
        # FIXME Some way, some how, check if we are connected and if not, raise
        # this error. I get into infinite recursion when I call
        # self.isconnected().
        #if not self.isconnected():
        #    raise RuntimeError
        
        # FIXME Get the exact exception type on failure so we 
        # can raise a RuntimeError
        #try:
        self.mqtt.publish(topic, msg, encrypt)
        #except:
        #    # TODO If we get multiple send warnings only record one
        #    warning = ("Unable to send to the cloud. Topic: '",
        #                str(topic) + "', message: '" + str(message) + "'")
        #    raise RuntimeError(warning)
        
        decrypt = True
        if not encrypt:
            # Then we also have nothing to decrypt
            decrypt = False
        
        # FIXME be aware that mqtt.get() returns a byte object
        result = self.mqtt.get(topic, decrypt = decrypt)
        
        debug("result: '" + str(result) + "'", level = 0)
        
        # TODO This may be a bit cleaner if we try/except on the error
        #   TypeError: can't convert 'NoneType' object to str implicitly
        if result is not None:
            return result

# end of class CloudCls(object)

cloud = CloudCls()
cloud.connect()