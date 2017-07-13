class MQTT(object):
    from config import config
    from crypto import AES, getrandbits
    from maintenance import maintenance
    
    def __init__(self):
        """Setup our MQTT object"""
        from system import SYSTEM
        # TODO Add exception AdafruitIOError but under what conditions
        from simple import MQTTClient
        
        self.maintenance()
        
        self.topics = set()
        
        serial = SYSTEM().serial
        version = SYSTEM().version
        
        self.key = bytes(self.config['ENCRYPTION_KEY'])
        
        port = self.config['MQTT_PORT']
        server = self.config['MQTT_SERVER']
        retries = self.config['MQTT_RETRIES']
        timeout = self.config['MQTT_TIMEOUT']
        device_name = self.config['DEVICE_NAME']
        username = self.config['SERVICE_ACCOUNT_EMAIL']
        password = self.config['SERVICE_ACCOUNT_PASSWORD']
        
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
        """Connect to the MQTT broker"""
        self.maintenance()
        self.client.connect()
        self.client_no_login.connect()
    
    
    def publish(self, path, message, retries = self.retries, login = True, 
                encrypt = True):
        """Publish a data update to an MQTT path.
        
        Optionally don't require a login to the MQTT server or encryption.
        These are ideal for things such as ping.
        """
        # FIXME This demands that every MQTT topic have a value, which I think
        # they always will at least have the most recently published value
        from time import sleep

        self.maintenance()
        
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
            result = myclient.publish(self.root_path + '/' + path, message)
            
            sleep(1) # TODO Is this necessary?
            if result:
                break
        
        return result
    
    
    def get(self, path, retries = self.retries):
        """Gets any current data in an MQTT path"""
        self.maintenance()
        
        message = None
        
        if path not in self.topics:
            self.subscribe(path)
            
        for i in range(retries):        
            message = self.client.receive(path)[1]
            if message:
                break
        
        cipher = self.AES(self.key, self.AES.MODE_CFB, message[:16])
        return cipher.decrypt(message[16:])
    
    
    def subscribe(self, path, retries = self.retries):
        """Subscribes to an MQTT path"""
        self.maintenance()
        
        result = None
        
        for i in range(retries):
            result = self.client.subscribe(path)
            if result:
                break
        
        self.topics.add(path)
        return result