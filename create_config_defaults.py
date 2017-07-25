#!/usr/bin/python3.6
'''Goes through every file in this suite looking for config['XYZ'] settings and
populates the config defaults file.

Usage: ./create_config_defaults.py > config_defaults.json
'''
import glob
import sys, re
from json import dumps

settings = dict()
for filename in glob.iglob('**/*.py', recursive=True):
    with open(filename) as f:
        for row in f.readlines():
            # TODO Won't get configs where two are on one line
            match = re.search(r"config\['([^\']*)']", row)
            if match:
                setting = match.groups(1)[0]
                settings[setting] = None

# Pretty print is pretty, but makes for harder coding
#print(dumps(settings, indent=4, sort_keys = True), end = '')
print(dumps(settings, sort_keys = True), end = '')