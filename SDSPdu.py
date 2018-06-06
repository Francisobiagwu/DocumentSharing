"""
@author: Francis Obiagwu
@software: SecureDocumentSharing
@file: SDSPdu.py
@time: 6/6/18 7:21 PM
"""

import struct


class SDSPdu:
    message_type_len = '12s'
    checksum_len = 'q'
    error_code = 'i'
    more_data = '?'
    space = ' '

    format = message_type_len + space + checksum_len + space + error_code + space + more_data

    s = struct.Struct(format)
    print(format)
    array = (b'test', 888, 89, True)
    pdu_packed = s.pack(*array)
    print(pdu_packed)


sds = SDSPdu()
