from config import config
from system import System
from maintenance import maint
from crypto import AES, getrandbits
# TODO Add exception AdafruitIOError but under what conditions
from umqtt.robust import MQTTClient

class MQTT(object):
    def __init__(self):
        '''Setup our MQTT object'''       
        maint()
        
        self.topics = set()
        # Topics that I use without logging in
        self.topics_nl = set()
        
        serial = System().serial
        version = System().version
        
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
        self.root_path = device_name + '/' + version + '/' + serial
        
        # A no-username/pass for pings
        # FIXME Look out for security implications especially a DoS. I think we
        # can limit the rate of the client's connections. Best to use an MQTT
        # service.
        self.client_nl = MQTTClient(clientID, server, port)
        
        # A normal client
        self.client = MQTTClient(clientID, username, password, server, port)
        client.settimeout = timeout
    
    
    def connect(self):
        '''Connect to the MQTT broker'''
        maint()
        self.client.set_callback(sub_cb)
        # See the notes here on clean_session
        # https://github.com/micropython/micropython-lib/blob/master/umqtt.robust/example_sub_robust.py
        if not self.client.connect(clean_session = False):
            # We don't have any pre-existing sessions
            # FIXME Subscribe to all our topics. But what if I don't know of
            # any? See the note in the link above.
        self.client_nl.connect()
    
    
    def disconnect(self):
        '''Disconnect from the MQTT broker'''
        maint()
        self.client.disconnect()
        self.client_nl.disconnect()
    
    
    def publish(self, topic, msg, login = True, encrypt = True, 
                retries = retries):
        '''Publish a data update to an MQTT topic.
        
        Optionally don't require a login to the MQTT server or encryption.
        These are ideal for things such as ping.
        '''
        # FIXME This demands that every MQTT topic have a value, which I think
        # they always will at least have the most recently published value
        
        maint()
        
        if login:
            myclient = self.client
        else:
            myclient = self.client_nl
        
        if encrypt:
            # iv = Initialization Vector
            iv = self.getrandbits(128)
            cipher = AES(self.key, AES.MODE_CFB, iv)
            msg = iv + cipher.encrypt(bytes(msg))
        
        result = None
        
        for i in range(retries):
            root_path = bytes(self.root_path + '/' + topic)
            msg = bytes(msg)
            result = myclient.publish(root_path, msg)
            
            if result:
                break
        
        return result
    
    
    def get(self, topic, login = True, decrypt = True, retries = retries):
        '''Gets any current data in an MQTT topic'''
        maint()
        
        if login:
            myclient = self.client
        else:
            myclient = self.client_nl
        
        self.sub(topic)
        
        msg = None
        for i in range(retries):        
            msg = myclient.wait_msg(topic)[1]
            if msg:
                break
        
        if decrypt:
            cipher = self.AES(self.key, self.AES.MODE_CFB, msg[:16])
            msg = cipher.decrypt(msg[16:])
        
        return msg
    
    
    def sub_cb(self, topic, msg):
        '''Callback to collect messages as they come in'''
        # FIXME Finish. Add to sub, change topics to a data structure, and as
        # new data comes in overwrite what is in memory. Setup sub so it's non-
        # blocking and get so it just fetches what is in memory, if we even
        # need that. Maybe just login+decrypt right here, everything in get.
        self.data[topic] = msg
    
    
    def sub(self, topic, login = True, retries = retries):
        '''Subscribes to an MQTT topic'''
        maint()
        
        if login:
            if topic in self.topics:
                return
            myclient = self.client
        else:
            if topic in self.topics_nl:
                return
            myclient = self.client_nl
        
        topic = self.root_path + '/' + topic
        
        for i in range(retries):
            if myclient.sub(topic):
                if login:
                    self.topics.add(topic)
                else:
                    self.topics_nl.add(topic)
                
                break