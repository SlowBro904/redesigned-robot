#!/usr/bin/python3.4
import process_mqtt
from json import load
from hashlib import sha512
from test_suite import good

process_mqtt.check_file_list('SB')

check = "len(check_file_list())"
with open('/clients/SB/file_list.json') as f:
    file_list = load(f)
assert len(file_list) == 3, check
good(check)

# This not only checks that we're getting SHAsums correctly, it also checks
# that the dictionary has been setup correctly.
check = "check_file_list() SHA-512"
with open('/clients/SB/version.json', 'rb') as f:
    expected_sha = sha512(f.read()).hexdigest()
files = 2
file_list_sha = file_list[files]['/clients/SB/version.json']
assert file_list_sha == expected_sha, check
good(check)