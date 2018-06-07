"""
@author: Francis Obiagwu
@software: SecureDocumentSharing
@file: SDSPdu.py
@time: 6/6/18 7:21 PM
"""

import datetime
import struct

print(datetime.datetime.now())

class SDSPdu:
    message_type_len = '12s'
    timestamp = '12s'
    checksum_len = 'q'
    # error_code = 'i'
    data = '100s'
    # more_data = '?'
    space = ' '

    format = message_type_len + space + timestamp + space + checksum_len + space + data + space
    s = struct.Struct(format)
    print(format)

    class SDSPacketAssembly:
        message_type = None
        timestamp = None
        checksum = None
        data = None

        def set_message_type(self, message_type):
            self.message_type = message_type

        def set_timestamp(self, timestamp):
            self.timestamp = timestamp

        def set_checksum(self, checksum):
            self.checksum = checksum

        def set_data(self, data):
            self.data = data

        def get_message_type(self):
            return self.message_type

        def get_timestamp(self):
            return self.timestamp

        def get_checksum(self):
            return self.checksum

    def set_format(self, format):
        self.format = format
        self.s = struct.Struct(format)

    def pack(self, tuple_pdu):
        return self.s.pack(*tuple_pdu)


sds = SDSPdu()
