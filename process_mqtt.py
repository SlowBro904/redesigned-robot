#!/usr/bin/python3
# From http://www.steves-internet-guide.com/into-mqtt-python-client/
import os
from glob import glob
from time import sleep
from hashlib import sha512
from itertools import chain
from re import sub as re_sub
import paho.mqtt.client as mqtt
from json import dumps, load, dump
#from crypto import AES, getrandbits

debug_enabled = True
default_level = 0
client_code_base = '/clients'

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
    debug("in_msg.topic: '" + str(in_msg.topic) + "'", level = 1)
    debug("type(in_msg.topic): '" + str(type(in_msg.topic)) + "'", level = 1)
    
    dev_type, serial, ver, __, topic = in_msg.topic.split('/')
    msg = in_msg.value
    code_base = client_code_base + '/' + dev_type
    
    if topic == 'ping':
        # Don't encrypt ping/ack
        out_msg = 'ack'
    
    # FIXME Need a list of directories or maybe a protection file
    # (do_not_purge.json?) that don't get purged when we do an update. Data
    # directories, config files, and the like.
    elif topic == 'curr_client_ver':
        with open(code_base + '/version.json') as f:
            out_msg = load(f)
    
    elif topic == 'get_file_list':
        check_file_list()
        with open(code_base + '/file_list.json') as f:
            out_msg = f.readlines()

    elif topic == 'get_file':
        file = msg
        # TODO Paranoid. Can they get files from anywhere else?
        with open(code_base + '/' + file) as f:
            out_msg = f.readlines()
    
    out_topic = re_sub('/in/', '/out/', in_msg.topic)
    sha = sha512(out_msg).hexdigest()
    client.publish(out_topic, (dumps(out_msg), sha))


def get_sha_sums(dir):
    '''Recursively searches a directory for all folders and files and returns a
    tuple of two lists: The first list is a list of directories and the second 
    is a list of tuples which are file names with their SHA-512 hash.
    '''
    dirs = list()
    files = list()
    # TODO There's probably a way to combine these statements but I'm not that
    # advanced yet.
    for x in os.walk(dir):
        for file in (chain.from_iterable(glob(os.path.join(x[0], '*')))):
            if os.path.isdir(file):
                # It's actually a directory. Don't attempt SHA-512.
                dirs.append(file)
                continue
            
            sha = sha512()
            with open(file, 'rb') as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    sha.update(chunk)
                sha = sha.hexdigest()
                files.append((file, sha))
    return (dirs, files)


def check_file_list(dir):
    '''Checks dir + '/version.json' and compares it to dir + '/file_list.json'.
    If the version stored in version.json is newer than what is in
    file_list.json then update the latter with a tuple that is the version
    number, and the directories and file names with SHA-512 sums from
    get_sha_sums(). To do an update to push out to clients, we update
    version.json and all other files in the directory, and this will
    automatically update the file list.
    '''
    debug("check_file_list()", level = 1)
    dir = client_code_base + '/' + dir
    
    try:
        debug("Trying to open version.json", level = 1)
        open(dir + '/version.json')
        open(dir + '/file_list.json')
    except FileNotFoundError:
        # TODO Also [Errno 2]
        # Initialize
        debug("Could not open version.json", level = 1)
        code_ver = '0.0.0'
        debug("About to create version.json", level = 1)
        with open(dir + '/version.json', 'w') as f:
            dump(code_ver, f)
        
        debug("Created version.json, now to create file_list.json", level = 1)
        
        file_list_ver = code_ver
        dirs, files = get_sha_sums(dir)
        with open(dir + '/file_list.json', 'w') as f:
            dump((file_list_ver, dirs, files), f)
    
    with open(dir + '/version.json') as f:
        code_ver = load(f)
    
    with open(dir + '/file_list.json') as f:
        file_list_ver = load(f)[0]
    
    if file_list_ver != code_ver:
        dirs, files = get_sha_sums(dir)
        
        # FIXME Exclude file_list.json from SHA checking on the client since it
        # will differ from the line above to now
        with open(dir + '/file_list.json', 'w') as f:
            dump((code_ver, dirs, files), f)


def on_log(client, userdata, level, buf):
    debug("log: " + str(buf))


def _encrypt(msg):
    # iv = Initialization Vector
    iv = getrandbits(128)
    return iv + AES(key, AES.MODE_CFB, iv).encrypt(bytes(msg))

# FIXME Uncomment all, move to another script
#client = mqtt.Client(client_id = 'better_automations')
#client.connect('localhost')
#
## Client name and version they are at
#authorized_devices = {'SB': {'240ac400b1b6': '0.0.0'}}
#device_keys = {'SB': {'240ac400b1b6': 'abcd1234'}}
#topics = {'SB': ['ping', 'get_new_dirs']}
#
## Setup our callback
#client.on_message = on_message
#client.on_log = on_log
#client.loop_start()
#
## Subscribe to all of our authorized device topics
#for device_type in authorized_devices:
#    for serial, version in authorized_devices[device_type].items():
#        root_path = device_type + '/' + serial + '/' + version + '/in/'
#        for topic in topics[device_type]:
#            mytopic = root_path + topic
#            client.subscribe(mytopic, qos = 1)
#
#
#while True:
#    sleep(1)