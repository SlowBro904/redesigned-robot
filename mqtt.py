class MQTT(object):
    from config import config
    from crypto import AES, getrandbits
    from maintenance import maint
    
    def __init__(self):
        '''Setup our MQTT object'''
        from system import System
        # TODO Add exception AdafruitIOError but under what conditions
        from umqtt.robust import MQTTClient
        
        self.maint()
        
        self.topics = set()
        
        serial = System().serial
        version = System().version
        
        self.key = bytes(self.config.conf['ENCRYPTION_KEY'])
        
        port = self.config.conf['MQTT_PORT']
        server = self.config.conf['MQTT_SERVER']
        retries = self.config.conf['MQTT_RETRIES']
        timeout = self.config.conf['MQTT_TIMEOUT']
        device_name = self.config.conf['DEVICE_NAME']
        username = self.config.conf['SERVICE_ACCOUNT_EMAIL']
        password = self.config.conf['SERVICE_ACCOUNT_PASSWORD']
        
        # Use the device name, the version, and the serial number for the root 
        # path. I'm including the device name and version so that we can have 
        # multiple devices and a newer version does not break the interface for 
        # clients not upgraded yet
        self.root_path = '/'.join([device_name, version, serial])
        
        # A no-username/pass for pings
        # FIXME Look out for security implications especially a DoS. I think we
        # can limit the rate of the client's connections. Best to use an MQTT
        # service.
        self.client_no_login = MQTTClient(server, port)
        
        # A normal client
        self.client = MQTTClient(username, password, server, port)
        client.settimeout = timeout
    
    
    def connect(self):
        '''Connect to the MQTT broker'''
        self.maint()
        self.client.connect()
        self.client_no_login.connect()
    
    
    def publish(self, topic, message, retries = self.retries, login = True, 
                encrypt = True):
        '''Publish a data update to an MQTT topic.
        
        Optionally don't require a login to the MQTT server or encryption.
        These are ideal for things such as ping.
        '''
        # FIXME This demands that every MQTT topic have a value, which I think
        # they always will at least have the most recently published value
        from time import sleep
        
        self.maint()
        
        if self.login:
            myclient = self.client
        else:
            myclient = self.client_no_login
        
        if encrypt:
            iv = self.getrandbits(128)
            cipher = self.AES(self.key, self.AES.MODE_CFB, iv)
            message = iv + cipher.encrypt(bytes(message))
        
        result = None
        
        for i in range(retries):
            result = myclient.publish(self.root_path + '/' + topic, message)
            
            sleep(1) # TODO Is this necessary?
            if result:
                break
        
        return result
    
    
    def get(self, topic, retries = self.retries, decrypt = True):
        '''Gets any current data in an MQTT topic'''
        self.maint()
        
        message = None
        
        if topic not in self.topics:
            self.subscribe(topic)
            
        for i in range(retries):        
            message = self.client.receive(topic)[1]
            if message:
                break
        
        if decrypt:
            cipher = self.AES(self.key, self.AES.MODE_CFB, message[:16])
            message = cipher.decrypt(message[16:])
        
        return message
    
    
    def subscribe(self, topic, retries = self.retries):
        '''Subscribes to an MQTT topic'''
        self.maint()
        
        topic = self.root_path + '/' + topic
        
        result = None
        
        for i in range(retries):
            result = self.client.subscribe(topic)
            if result:
                break
        
        self.topics.add(topic)
        return result