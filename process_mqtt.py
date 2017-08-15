#!/usr/bin/python3
# From http://www.steves-internet-guide.com/into-mqtt-python-client/
from os import listdir
from json import dumps
from time import sleep
from hashlib import sha512
from re import sub as re_sub
import paho.mqtt.client as mqtt
#from crypto import AES, getrandbits

debug_enabled = True
default_level = 0

# Locations for client code
# FIXME Reconcile (maybe?) client version to code version?
# FIXME Do I want to just do /SB/current?
client_code = {'SB': '/SB/0.0.0'}

def debug(msg, level = 0):
    '''Prints a debug message'''
    if not debug_enabled:
        return

    if level > default_level:
        return

    print("[DEBUG]", str(msg))


def on_message(client, userdata, in_msg):
    '''Callback for when we get messages'''
    debug("in_msg: '" + str(in_msg) + "'", level = 1)
    debug("in_msg.topic: '" + str(in_msg.topic) + "'", level = 0)
    debug("type(in_msg.topic): '" + str(type(in_msg.topic)) + "'", level = 0)
    
    # Just the end subtopic, the rest is meta
    device_type = in_msg.topic.split('/')[0]
    topic = in_msg.topic.split('/')[-1]

    if topic == 'ping':
        # Don't encrypt ping/ack
        out_msg = 'ack'
    elif topic == 'get_new_dirs':
        # FIXME Change this to a directory reconcile on clients. Add what's new
        # and remove what's old.
        # FIXME Encrypt -- maybe :-)
        out_msg = ['deleteme']
    elif topic == 'get_sys_updates':
        # FIXME And delete files off the local client as well
        root_path = client_code[device_type]
        sha_sum = sha512()

        # FIXME Glob subdirectories and find files everywhere
        for file in listdir(root_path):
            with open(file) as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    sha_sum.update(chunk)
                
                sha_sum = sha_sum.digest()
                f.seek(0)
            
                # TODO Can I get the SHA sum AND read the contents at the same
                # time?
                contents = f.readlines()
            
            out_msg.append([file, sha_sum, contents])
        
    out_topic = re_sub('/in/', '/out/', in_msg.topic)
    client.publish(out_topic, dumps(out_msg))


def on_log(client, userdata, level, buf):
    debug("log: " + str(buf))


def _encrypt(msg):
    # iv = Initialization Vector
    iv = getrandbits(128)
    return iv + AES(key, AES.MODE_CFB, iv).encrypt(bytes(msg))

client = mqtt.Client(client_id = 'better_automations')
client.connect('localhost')

# Client name and version they are at
# FIXME Pull from a database
authorized_devices = {'SB': {'240ac400b1b6': '0.0.0'}}
device_keys = {'SB': {'240ac400b1b6': 'abcd1234'}}
topics = {'SB': ['ping', 'get_new_dirs']}

# Setup our callback
client.on_message = on_message
client.on_log = on_log
client.loop_start()

# Subscribe to all of our authorized device topics
for device_type in authorized_devices:
    for serial, version in authorized_devices[device_type].items():
        root_path = device_type + '/' + serial + '/' + version + '/in/'
        for topic in topics[device_type]:
            mytopic = root_path + topic
            # FIXME When getting a message, should I/do I want to auto-sub?
            client.subscribe(mytopic, qos = 1)

while True:
    sleep(1)