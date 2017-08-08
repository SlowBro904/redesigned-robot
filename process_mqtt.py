#!/usr/bin/python3
# FIXME
# pip install paho-mqtt
#Mint-VM ~ # ./process_mqtt.py
#Traceback (most recent call last):
#  File "./process_mqtt.py", line 2, in <module>
#    import paho.mqtt.client as mqtt
#ImportError: No module named 'paho'
#Mint-VM ~ #

import paho.mqtt.client as mqtt
from crypto import AES, getrandbits

def on_message(client, userdata, message):
        '''Callback for when we get messages'''
        # Don't encrypt ping/ack
        if message.topic is 'ping':
                msg = 'ack'
        
        client.publish(message.topic, msg)

def _encrypt(msg):
        # iv = Initialization Vector
        iv = getrandbits(128)
        return iv + AES(key, AES.MODE_CFB, iv).encrypt(bytes(msg))

client = mqtt.Client(client_id = 'better_automations')
client.connect()

# Client name and version they are at
authorized_devices = {'SB': {'240ac400b1b6': '0.0.0'}}
device_kys = {'SB': {'240ac400b1b6': 'abcd1234'}}
topics = {'SB': ['ping']}

# Subscribe to all of our authorized device topics
for device_type in authorized_devices:
        for device in authorized_devices[device_type]:
                root_path = device + '/' + version
                for topic in topics[device_type]:
                        mytopic = root_path + '/' + topic
                        client.subscribe(mytopic, qos = 1)

# Setup our callback
client.on_message = on_message
client.loop_start()