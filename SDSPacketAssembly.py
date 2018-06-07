"""
@author: Francis Obiagwu
@software: SecureDocumentSharing
@file: SDSPacketAssembly.py
@time: 6/7/18 4:59 AM
"""


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
