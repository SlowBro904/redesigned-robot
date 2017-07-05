""" Sets our serial number variable based on the system's unique ID """
from binascii import hexlify
from machine import unique_id
        
serial = str(hexlify(unique_id()), 'utf-8')