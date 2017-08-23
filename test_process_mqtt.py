#!/usr/bin/python3.4
import process_mqtt
from json import load
from test_suite import good

process_mqtt.check_file_list('SB')
with open('/clients/SB/file_list.json') as f:
    file_list = load(f)
check = "check_file_list()"
assert len(file_list) == 3, check
good(check)