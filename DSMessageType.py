#!/usr/bin/env python

"""
@author: Francis Obiagwu
@software: SecureDocumentSharing
@file: DSMessageType.py
@time: 6/6/18 7:16 PM
"""

class DSMessageType:

    CONNECT = b'CONNECT'
    CAUTH = b'CAUTH'
    S_EDIT = b'S_EDIT'
    S_COMMIT = b'S_COMMIT'
    S_RELEASE = b'S_RELEASE'
    CLOSE = b'CLOSE'
    ACK = b'ACK'
