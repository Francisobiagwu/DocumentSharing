#!/usr/bin/env python



class Header:
    pass


import binascii

name = 'francis'

crc = binascii.crc32(b'francis')
crc2222 = binascii.crc32(b'francis')

print(crc)
print(crc2222)
