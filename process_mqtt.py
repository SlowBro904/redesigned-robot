#!/usr/bin/python3.4
# From http://www.steves-internet-guide.com/into-mqtt-python-client/
import os
from glob import glob
from time import sleep
from hashlib import sha512
from itertools import chain
from re import sub as re_sub
import paho.mqtt.client as mqtt
#from crypto import AES, getrandbits
from multiprocessing import Process
from json import loads, dumps, load, dump

# FIXME False for prod
debug_enabled = True
testing = True
default_level = 0
client_code_base = '/clients'
device_data = {'SB': 
                {'240ac400b1b6':
                    {'0.0.0': 
                        {'testing1.json': ['testing1', '123']}
                    }
                }
              }

device_data_status = {'SB':
                        {'240ac400b1b6':
                            {'0.0.0':
                                {'testing1.json': False}
                            }
                        }
                     }

mqtt_client = mqtt.Client(client_id = 'better_automations')

# Client name and version they are at
# FIXME Need to also auto subscribe to new versions
authorized_devices = {'SB': {'240ac400b1b6': '0.0.0'}}
device_keys = {'SB': {'240ac400b1b6': 'abcd1234'}}
device_log = dict()
device_log['SB'] = dict()

# FIXME Remove 'testing' for prod
topics = {'SB': ['ping', 'curr_client_ver', 'get_file_list', 'get_file',
                    'get_data_updates', 'got_data_update', 'status',
                    'error_log', 'testing']}

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
    msg = loads(in_msg.payload.decode('utf-8'))
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
        check_file_list(dev_type)
        with open(code_base + '/file_list.json') as f:
            out_msg = load(f)
    
    elif topic == 'get_file':
        # FIXME The version.json file is different on the client
        myfile = msg
        # TODO Paranoid. Can they get files from anywhere else?
        # How about /.. ?
        # Run this script non-privileged and do file perms audit 
        # regularly
        # FIXME Add a try/except to here and anywhere
        # FileNotFoundError: [Errno 2] No such file or directory
        # TODO Not sending in 'rb' binary mode, will this cause a
        # problem later?
        with open(code_base + '/' + myfile) as f:
            contents = f.readlines()

        debug("contents: '" + str(contents) + "'")

        sha = get_file_sha512(code_base + '/' + myfile)
        out_msg = [contents, sha]
        
    
    elif topic == 'get_data_updates':
        # This is a list of lists; each item in the list is a list
        # that contains 1. the file to update 2. the parameter 3.
        # the value.
        # FIXME Move test data to the DB.
        if msg == 'all':
            # Send all data files. We probably did a factory reset.
            # FIXME Finish
            out_msg = device_data[dev_type][serial][ver]
        else:
            # Send only any new data updates since our last check.
            # FIXME Finish
            out_msg = dict()
            if testing:
                device_data[dev_type][serial][ver]['testing2.json'] = ['testing2', '456']
                device_data_status[dev_type][serial][ver]['testing2.json'] = False
            for data_file in device_data[dev_type][serial][ver]:
                if not device_data_status[dev_type][serial][ver][data_file]:
                    out_msg[data_file] = device_data[dev_type][serial][ver][data_file]
    
    
    elif topic == 'got_data_update':
        data_file = msg
        # TODO This only records the data file updated, not actual
        # data updated. But maybe we want that, because it doubles
        # the data sent. We basically wouldn't get this unless we
        # validate the data being sent, so I think it's sufficient.
        # FIXME Catch AttributeError or whatever it would be
        device_data_status[dev_type][serial][ver][data_file] = True
        out_msg = 'ack'
    
    
    elif topic == 'error_log':
        try:
            device_log[dev_type][serial]
        except KeyError:
            device_log[dev_type][serial] = list()
        device_log[dev_type][serial].append(msg)
        # FIXME Here, do something with the errors received
        debug("error_log: '" + str(device_log[dev_type][serial])
                + "'")
        
        out_msg = 'ack'
    
    
    elif topic == 'status':
        # Here, device is the on-board device such as door sensor
        # TODO Think of a less ambiguous name
        device, status = msg
        try:
            device_status[dev_type][serial]
        except AttributeError:
            device_status[dev_type][serial] = list()

        try:
           device_status[dev_type][serial][device] 
        except AttributeError:
            device_status[dev_type][serial][device] = bool()

        device_log[dev_type][serial][device] = status
        # FIXME Here, do something with the staus received
        debug("status: '" +
                str(device_log[dev_type][serial][device]) + "'")
        
        out_msg = 'ack'


    elif topic == 'testing':
        out_msg = 'ack'
    
    
    # TODO This shouldn't be naive and just substitute anywhere but
    # substitute exactly one level from the end
    out_topic = re_sub('/in/', '/out/', in_msg.topic)
    
    debug("out_topic: '" + str(out_topic) + "'")
    debug("out_msg: '" + str(out_msg) + "'")
    
    # Turn our message into a JSON string encoded UTF-8
    out_msg = dumps(out_msg)
    sha = sha512(out_msg.encode('utf-8')).hexdigest()
    
    # JSON again to wrap both message and SHA together
    client.publish(out_topic, dumps([out_msg, sha]))


def get_file_sha512(myfile):
    sha = sha512()
    with open(myfile, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b""):
            sha.update(chunk)
    return sha.hexdigest()


def get_sha_sums(mydir):
    '''Recursively searches a directory for all folders and files and returns a
    tuple of a list and a dict: The list holds directory names and the dict's
    keys are file names and the values are their SHA-512 hash.
    '''
    dirs = list()
    files = dict()
    # TODO Reduce this to less than 80 chars. I have a feeling the for myfile
    # is redundant. Found it here:
    # https://stackoverflow.com/questions/18394147/recursive-sub-folder-search-and-return-files-in-a-list-python
    for myfile in [y for x in os.walk(mydir) for y in glob(os.path.join(x[0], '*'))]:
        if os.path.isdir(myfile):
            # It's actually a directory. Don't attempt SHA-512.
            # Remove the client_code_base and device dir
            myfile = re_sub(client_code_base, '', myfile)
            myfile = '/'.join(myfile.split('/')[2:])
            dirs.append(myfile)
            continue
        
        sha = get_file_sha512(myfile)

        # TODO Redundant
        # Remove the client_code_base and device dir
        myfile = re_sub(client_code_base, '', myfile)
        myfile = '/'.join(myfile.split('/')[2:])
        files[myfile] = sha
    return (dirs, files)


def check_file_list(mydir):
    '''Checks mydir + '/version.json' and compares it to mydir +
    '/file_list.json'.
    
    If the version stored in version.json is newer than what is in
    file_list.json then update the latter with a tuple that is the version
    number, and the mydirectories and file names with SHA-512 sums from
    get_sha_sums(). To do an update to push out to clients, we update
    version.json and all other files in the mydirectory, and this will
    automatically update the file list.
    '''
    debug("check_file_list()", level = 1)
    mydir = client_code_base + '/' + mydir
    
    try:
        debug("Trying to open version.json", level = 1)
        open(mydir + '/version.json')
        open(mydir + '/file_list.json')
    except FileNotFoundError:
        # TODO Also [Errno 2]
        # Initialize
        debug("Could not open version.json", level = 1)
        code_ver = '0.0.0'
        debug("About to create version.json", level = 1)
        with open(mydir + '/version.json', 'w') as f:
            dump(code_ver, f)
        
        debug("Created version.json, now to create file_list.json", level = 1)
        
        file_list_ver = code_ver
        mydirs, files = get_sha_sums(mydir)
        with open(mydir + '/file_list.json', 'w') as f:
            dump((file_list_ver, mydirs, files), f)
    
    with open(mydir + '/version.json') as f:
        code_ver = load(f)
    
    with open(mydir + '/file_list.json') as f:
        file_list_ver = load(f)[0]
    
    if file_list_ver != code_ver:
        mydirs, files = get_sha_sums(mydir)
        
        # FIXME Exclude file_list.json from SHA checking on the client since it
        # will differ from the line above to now
        with open(mydir + '/file_list.json', 'w') as f:
            dump((code_ver, mydirs, files), f)


def on_log(client, userdata, level, buf):
    debug("log: " + str(buf), level = 1)


def _encrypt(msg):
    # iv = Initialization Vector
    iv = getrandbits(128)
    return iv + AES(key, AES.MODE_CFB, iv).encrypt(bytes(msg))


if __name__ == '__main__':
    mqtt_client.connect('localhost')
    mqtt_client.loop_start()
    
    # Setup our callbacks
    mqtt_client.on_message = on_message
    mqtt_client.on_log = on_log
    
    debug("authorized_devices: '" + str(authorized_devices) + "'")
    # Subscribe to all of our authorized device topics
    for dev_type in authorized_devices:
        debug("dev_type: '" + str(dev_type) + "'")
        for serial, version in authorized_devices[dev_type].items():
            debug("serial: '" + str(serial) + "'")
            debug("version: '" + str(version) + "'")
            root_path = dev_type + '/' + serial + '/' + version + '/in/'
            debug("root_path: '" + str(root_path) + "'")
            for topic in topics[dev_type]:
                mytopic = root_path + topic
                debug("Subscribing to '" + str(mytopic) + "'")
                mqtt_client.subscribe(mytopic, qos = 1)

    while True:
        sleep(1)
