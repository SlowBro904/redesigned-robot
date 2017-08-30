#!/usr/bin/python3.4
import process_mqtt
from os import remove
from json import load
from hashlib import sha512
from test_suite import good

file_list = '/clients/SB/file_list.json'
remove(file_list)
process_mqtt.check_file_list('SB')

check = "len(check_file_list())"
with open(file_list) as f:
    file_list = load(f)
assert len(file_list) == 3, check
good(check)

# This not only checks that we're getting SHAsums correctly, it also checks
# that the dictionary has been setup correctly.
check = "check_file_list() SHA-512"
with open('/clients/SB/version.json', 'rb') as f:
    expected_sha = sha512(f.read()).hexdigest()
file_list_sha = file_list[2]['/clients/SB/version.json']
assert file_list_sha == expected_sha, check
good(check)

check = "check_file_list() version"
with open('/clients/SB/version.json') as f:
    client_ver = load(f)
file_list_ver = file_list[0]
assert client_ver == file_list_ver, check
good(check)

check = "check_file_list() dirs"
dirs = file_list[1]
assert '/clients/SB/testing.dir' in dirs, check
good(check)