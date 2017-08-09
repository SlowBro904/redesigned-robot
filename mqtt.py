# TODO Failover
import debugging
from config import config
from system import SystemCls
from maintenance import maint
from crypto import AES, getrandbits
# TODO Add exception AdafruitIOError but under what conditions
from umqtt.robust import MQTTClient

debug = debugging.printmsg
testing = debugging.testing

class MQTTCls(object):
    def __init__(self):
        '''Setup our MQTT object'''       
        maint()
        
        self.data = dict()
        self.resub = False
        
        serial = SystemCls().serial
        version = SystemCls().version
        
        self.key = bytes(config.conf['ENCRYPTION_KEY'])
        
        port = config.conf['MQTT_PORT']
        server = config.conf['MQTT_SERVER']
        retries = config.conf['MQTT_RETRIES']
        timeout = config.conf['MQTT_TIMEOUT']
        device_name = config.conf['DEVICE_NAME']
        username = config.conf['SERVICE_ACCOUNT_EMAIL']
        password = config.conf['SERVICE_ACCOUNT_PASSWORD']
        
        clientID = device_name + ":" + serial
        
        # Use the device name, the version, and the serial number for the root 
        # path. I'm including the device name and version so that we can have 
        # multiple devices and a newer version does not break the interface for 
        # clients not upgraded yet
        self.root_path = clientID + '/' + version
        
        # A normal client
        self.client = MQTTClient(clientID, username, password, server, port)
        self.client.settimeout = timeout
    
    
    def connect(self):
        '''Connect to the MQTT broker'''
        maint()
        self.client.set_callback(_sub_cb)
        # See the notes here on clean_session
        # https://github.com/micropython/micropython-lib/blob/master/umqtt.robust/example_sub_robust.py
        if not self.client.connect(clean_session = False):
            self.resub = True
        #self.client_nl.connect(clean_session = False):
        #    self.resub = True
    
    
    def disconnect(self):
        '''Disconnect from the MQTT broker'''
        maint()
        self.client.disconnect()
        #self.client_nl.disconnect()
    
    
    def _encrypt(self, msg):
        # FIXME What's the diff between AES.SEGMENT_8 and AES.SEGMENT_128
        # FIXME What about message authentication codes, SHA-512
        # FIXME Keys always 16 bytes long
        # FIXME Maybe uhashlib.sha512(data) for MAC?
        # iv = Initialization Vector
        iv = getrandbits(128)
        return iv + AES(self.key, AES.MODE_CFB, iv).encrypt(bytes(msg))
    
    
    def _decrypt(self, msg):
        return AES(self.key, AES.MODE_CFB, msg[:16]).decrypt(msg[16:])
    
    
    def publish(self, topic, msg, encrypt = True, retries = None):
        '''Publish a data update to an MQTT topic.
        
        Optionally don't require a login to the MQTT server or encryption.
        These are ideal for things such as ping.
        '''
        maint()
        
        if not retries:
            retries = self.retries
        
        if encrypt:
            msg = self._encrypt(msg)
        
        result = None
        
        # FIXME Add in and out topic trees
        root_path = bytes(self.root_path + '/' + topic)
        
        for i in range(retries):
            result = self.client.publish(root_path, msg)
            
            if result:
                break
        
        return result
    
    
    def get(self, topic, decrypt = True, retries = None):
        '''Gets any current data in an MQTT topic'''
        maint()
        
        if not retries:
            retries = self.retries
        
        self.sub(topic)
        
        for i in range(retries):    
            # Upon success it will break
            # FIXME Test
            self.client.check_msg()
            sleep(1)
        
        msg = self.data[topic]
        
        if decrypt:
            msg = self._decrypt(msg)
        
        return msg
    
    
    def _sub_cb(self, topic, msg):
        '''Callback to collect messages as they come in'''
        self.data[topic] = msg
    
    
    def sub(self, topic, login = True, retries = None):
        '''Subscribes to an MQTT topic'''
        maint()
        if not self.resub and topic in self.data:
            return
        
        if not retries:
            retries = self.retries
        
        topic = bytes(self.root_path + '/' + topic)
        
        for i in range(retries):
            if self.client.subscribe(topic, qos = 1):
                # FIXME Don't set resub to false because we probably have other
                # topics. But if true resub everything in self.data and/or
                # maybe clear data and force a refetch. I think msg persistence
                # may be required except in cases like ping? But if we ping we
                # at least know our connection to the broker is good. We don't
                # care all that much to test from client through broker to
                # processing modules. We can test broker to processing modules
                # elsewhere.
                self.resub = False
                break