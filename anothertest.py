#!/usr/bin/env python

__author__ = "Francis Obiagwu"
__copyright__ = "Copyright 2017, GSCE IDS Project"
__version__ = "1.0"
__email__ = "francis.c.obiagwu.civ@mail.mil"


class Header:
    pass


import binascii

name = 'francis'

crc = binascii.crc32(b'francis')
crc2222 = binascii.crc32(b'francis')

print(crc)
print(crc2222)
