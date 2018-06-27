"""
@author: Francis Obiagwu
@software: SecureDocumentSharing
@file: DSErrorCorrection.py
@time: 6/26/18 8:15 PM
"""

__author__ = "Francis Obiagwu"
__copyright__ = "Copyright 2018"
__version__ = "1.0"


class DSErrorCorrection:
    def __init__(self):
        self.sent_data = {}
        self.key = ''

    def add_recently_sent_data(self, data, checksum):
        self.sent_data = {}
        self.sent_data.update({data: checksum})

    def is_data_received(self, data):
        print(self.sent_data, data)
        checksum = [value for value in self.sent_data.values()]
        if data == checksum[0]:
            return True
        else:
            return False
