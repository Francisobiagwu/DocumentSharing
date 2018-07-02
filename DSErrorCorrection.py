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
        self.checksum = ''
        self.message_type = ''

    def add_recently_sent_data(self, data, checksum, message_type):
        """
        Used to add recently sent data such that if the client didn't receive data within 5 seconds window, data is
        automatically resent to the client
        :param data: data sent to the client
        :param checksum: the calculated checksum sent to the client
        :param message_type: the type of message sent to the client. Eg DSMessage.CAUTH
        :return: None
        """
        self.sent_data = {}
        self.sent_data.update({data: (message_type, checksum)})

    def is_data_received(self, given_checksum):
        """
        Used to verify if the client received sent data
        :param given_checksum:
        :return:
        """
        print(self.sent_data, given_checksum)
        checksum = [value[0] for value in self.sent_data.values()][0]
        self.checksum = checksum
        message_type = [value[1] for value in self.sent_data.values()][0]
        self.message_type = message_type
        print(checksum, message_type)
        if given_checksum == checksum:
            return True
        else:
            return False

    def get_checksum(self):
        """
        :return: Returns the checksum
        """
        return self.checksum

    def get_message_type(self):
        """
        :return: Returns the message type sent
        """
        return self.message_type


    def get_recently_sent_data(self):
        data = self.sent_data.values()


test = DSErrorCorrection('francis', 33333, 'ACK')
