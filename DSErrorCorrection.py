"""
@author: Francis Obiagwu
@software: SecureDocumentSharing
@file: DSErrorCorrection.py
@time: 6/26/18 8:15 PM
"""



class DSErrorCorrection:
    def __init__(self):
        self.sent_data_dic = {}
        self.sent_data = {}
        self.key = ''
        self.checksum = ''
        self.message_type = ''
        self.flag = ''
        self.error_code = ''

    def add_recently_sent_data(self, data, checksum, message_type, flag):
        """
        Used to add recently sent data such that if the client didn't receive data within 5 seconds window, data is
        automatically resent to the client
        :param data: data sent to the client
        :param checksum: the calculated checksum sent to the client
        :param message_type: the type of message sent to the client. Eg DSMessage.CAUTH
        :param flag: This data tells the client if the server is still sending message
        :return: None
        """
        self.sent_data = data
        self.message_type = message_type
        self.checksum = checksum
        self.flag = flag

        self.sent_data_dic.update({data: (message_type, checksum, flag)})

    def is_data_received(self, given_checksum):
        """
        Used to verify if the client received sent data
        :param given_checksum:
        :return:
        """
        print(self.sent_data, given_checksum)

        if given_checksum == self.checksum:
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


    def get_flag(self):
        return self.flag


    def get_recently_sent_data(self):
        data = self.sent_data.values()


