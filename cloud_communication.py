from main import wifi
from main import mqtt
from json import loads, dumps

# TODO Can I do if wifi?

def ping_cloud():
    if not wifi.isconnected():
        return False
        
    if not send('ping') == 'ack':
        return False
    
    return True

def send(action, message = None):
    if not wifi.isconnected():
        return False
    
    mqtt.publish(dumps(action, message))
    return mqtt.get(action)

def get(action):
    if not wifi.isconnected():
        return False
    
    return mqtt.get(action)

def get_data_updates():
    if not wifi.isconnected():
        return False

def update_system():
    if not wifi.isconnected():
        return False