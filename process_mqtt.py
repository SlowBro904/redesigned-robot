#!/usr/bin/python3
# From http://www.steves-internet-guide.com/into-mqtt-python-client/
from time import sleep
from re import sub as re_sub
import paho.mqtt.client as mqtt
#from crypto import AES, getrandbits

debug_enabled = True
default_level = 0
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

    # Don't encrypt ping/ack
    if in_msg.topic.endswith('/ping'):
        out_msg = 'ack'
        
    out_topic = re_sub('/in/', '/out/', in_msg.topic)
    client.publish(out_topic, out_msg)


def on_log(client, userdata, level, buf):
    debug("log: " + str(buf))


def _encrypt(msg):
    # iv = Initialization Vector
    iv = getrandbits(128)
    return iv + AES(key, AES.MODE_CFB, iv).encrypt(bytes(msg))

client = mqtt.Client(client_id = 'better_automations')
client.connect('localhost')

# Client name and version they are at
authorized_devices = {'SB': {'240ac400b1b6': '0.0.0'}}
device_kys = {'SB': {'240ac400b1b6': 'abcd1234'}}
topics = {'SB': ['ping']}

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
            client.subscribe(mytopic, qos = 1)

while True:
    sleep(1)
