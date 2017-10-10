print("[DEBUG] mqtt.py begin")
# TODO Failover
import debugging
from time import sleep
print("[DEBUG] mqtt.py before import config")
from config import config
print("[DEBUG] mqtt.py after import config")
from uhashlib import sha512
print("[DEBUG] mqtt.py before import SystemCls")
from system import SystemCls
print("[DEBUG] mqtt.py after import SystemCls")
from ubinascii import hexlify
from maintenance import maint
from ujson import dumps, loads
from crypto import AES, getrandbits
# TODO Add exception AdafruitIOError but under what conditions
print("[DEBUG] mqtt.py before import MQTTClient")
from umqtt.robust import MQTTClient
print("[DEBUG] mqtt.py after import MQTTClient")

debug = debugging.printmsg
testing = debugging.testing

class MQTTCls(object):
    def __init__(self):
        '''Setup our MQTT object'''       
        maint()
        print("[DEBUG] mqtt.py __init__() start")
        
        self.data = dict()
        self.resub = False
        
        serial = SystemCls().serial
        version = SystemCls().version
        
        self.key = bytes(config.conf['ENCRYPTION_KEY'], 'utf-8')
        
        server = config.conf['MQTT_SERVER']
        port = int(config.conf['MQTT_PORT'])
        timeout = config.conf['MQTT_TIMEOUT']
        device_name = config.conf['DEVICE_NAME']
        self.retries = config.conf['MQTT_RETRIES']
        username = config.conf['SERVICE_ACCOUNT_EMAIL']
        password = config.conf['SERVICE_ACCOUNT_PASSWORD']
        
        # Use the device name, the serial, then the version, for the root 
        # path. I'm including the device name and version so that we can have 
        # multiple devices and a newer version does not break the interface for 
        # clients not upgraded yet
        self.root_path = device_name + '/' + serial + '/' + version
        
        # A normal client
        self.client = MQTTClient(serial, server, port, username, password)
        self.client.settimeout = timeout
        print("[DEBUG] mqtt.py __init__() end")
    
    
    def connect(self):
        '''Connect to the MQTT broker'''
        maint()
        self.client.set_callback(self._sub_cb)
        # See the notes here on clean_session
        # https://github.com/micropython/micropython-lib/blob/master/umqtt.robust/example_sub_robust.py
        # FIXME On connection failure we get OSError: -1
        if not self.client.connect(clean_session = False):
            # FIXME Test this. It did say self.resub but I think that's wrong
            self.client.resub = True
    
    
    def disconnect(self):
        '''Disconnect from the MQTT broker'''
        maint()
        self.client.disconnect()
    
    
    def ping(self):
        '''Pings the MQTT broker'''
        maint()
        return self.client.ping()
    
    
    def _encrypt(self, msg):
        maint()
        # FIXME What's the diff between AES.SEGMENT_8 and AES.SEGMENT_128
        # FIXME What about message authentication codes, SHA-512
        # FIXME Keys always 16 bytes long
        # FIXME Maybe uhashlib.sha512(data) for MAC?
        # iv = Initialization Vector
        iv = getrandbits(128)
        # FIXME Generates this error:
        # TypeError: unsupported types for __add__: 'bytes', 'AESCipher'
        #cipher = iv + AES(self.key, AES.MODE_CFB, iv)
        #return cipher.encrypt(bytes(msg, 'utf-8'))
    
    
    def _decrypt(self, msg):
        maint()
        # FIXME Not using encryption for now. Going to see what AWS requires.
        # Maybe they have a better scheme than I could craft. Libraries, etc.
        pass
        #return AES(self.key, AES.MODE_CFB, msg[:16]).decrypt(msg[16:])
    
    
    def publish(self, topic, msg, encrypt = True, retries = None):
        '''Publish a data update to an MQTT topic.
        
        Optionally don't require a login to the MQTT server or encryption.
        These are ideal for things such as ping.
        '''
        debug("encrypt: '" + str(encrypt) + "'", level = 1)
        
        maint()
        
        if not retries:
            retries = self.retries
        
        # FIXME Not using encryption for now. See note in _decrypt().
        #if encrypt:
        #    msg = self._encrypt(msg)
        
        result = None
        
        in_topic = bytes(self.root_path + '/in/' + topic, 'utf-8')
        
        if not msg:
            msg = 'null'

        # FIXME Comment
        print("[DEBUG] publish() in_topic: '" + str(in_topic) + "'")
        print("[DEBUG] publish() type(in_topic): '" + str(type(in_topic)) + "'")
        print("[DEBUG] publish() msg: '" + str(msg) + "'")
        print("[DEBUG] publish() dumps(msg): '" + str(dumps(msg)) + "'")
        
        debug("publish() in_topic: '" + str(in_topic) + "'", level = 0)
        debug("publish() type(in_topic): '" + str(type(in_topic)) + "'",
                level = 0)
        debug("publish() msg: '" + str(msg) + "'", level = 0)
        debug("publish() type(msg): '" + str(type(msg)) + "'", level = 0)
        
        for i in range(retries):
            result = self.client.publish(in_topic, dumps(msg))
            
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
            #while 1:
            # Upon success it will break
            # FIXME Test
            # FIXME I think I want check_msg() and sleep(1) but let me try this
            # FIXME Newp. Just hangs on wait_msg(). Try the example code next.
            # https://github.com/micropython/micropython-lib/blob/master/umqtt.simple/example_sub.py
            # FIXME Might just need a longer retry?
            # TODO Should I idle and/or maint()? Should maint() also idle()?
            # FIXME Does this wait until the server is finally ready to send?
            self.client.check_msg()
            sleep(1)
        
        # The full topic would be device and serial and all that. Remove all
        # but the end topic name.
        topic = topic.split('/')[-1]
        
        try:
            msg = self.data[topic]
        except KeyError:
            msg = None
        
        # FIXME Not using encryption for now. See note in _decrypt().
        #if decrypt:
        #    msg = self._decrypt(msg)
        
        return msg
    
    
    def _sub_cb(self, topic, msg):
        '''Callback to collect messages as they come in'''
        # The full topic would be device and serial and all that. Remove all
        # but the end topic name.
        # FIXME Not being called for get_file_list now, but it was before?
        # FIXME Comment all print [DEBUG]s
        print("[DEBUG] _sub_cb() topic: '" + str(topic) + "'")#, level = 0)
        print("[DEBUG] _sub_cb() msg: '" + str(msg) + "'")#, level = 0)
        
        topic = topic.decode('utf-8').split('/')[-1]
        
        # Remove outer JSON encoding
        msg, remt_sha = loads(msg)
        
        recv_msg_sha = hexlify(sha512(msg).digest())
        
        # Remove the inner JSON encoding
        msg = loads(msg)
        
        # TODO I think this should be more clearly stated like this:
        # remt_sha = remt_sha.encode('utf-8)
        remt_sha = bytes(remt_sha, 'utf-8')
        
        if remt_sha == recv_msg_sha:
            # FIXME Revert to debug()
            print("[DEBUG] remt_sha == recv_msg_sha")
            
            self.data[topic] = msg
            
            print("[DEBUG] self.data[topic]: '" + str(self.data[topic]) + "'")
        else:
            # FIXME ping, curr_client_ver, etc. are failing here yet not
            # failing in their execution as they should
            print("[DEBUG] remt_sha != recv_msg_sha")
            print("[DEBUG] msg: '" + str(msg) + "'")
            print("[DEBUG] remt_sha: '" + str(remt_sha) + "'")
            print("[DEBUG] recv_msg_sha: '" + str(recv_msg_sha) + "'")
            
            # FIXME Else what? Hopefully re-request.
            pass
    
    
    def sub(self, topic, login = True, retries = None):
        '''Subscribes to an MQTT topic'''
        maint()
        
        # FIXME Uncomment
        #if not self.resub and topic in self.data:
        #    return
        
        if not retries:
            retries = self.retries
        
        out_topic = bytes(self.root_path + '/out/' + topic, 'utf-8')
        
        for i in range(retries):
            if self.client.subscribe(out_topic, qos = 1):
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