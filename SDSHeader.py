#!/usr/bin/env python

__author__ = "Francis Obiagwu"
__version__ = "1.0"

import binascii
import datetime


class SDSHeader:
    __message_type = ''
    __checksum = ''
    __timestamp = ''
    __timestamp_crc = None
    __data = ''

    def __init__(self):
        self.__message_type = None  # 8 bytes
        self.__checksum = None  #
        self.__timestamp = None
        self.__data = None

    def set_message_type_as_bytes(self, message_type):
        """
        Set the message type as bytes
        :param message_type:
        :return:
        """
        try:
            self.__message_type = message_type.encode()
        except AttributeError:
            pass

    def set_checksum(self):
        """
        converts the data into bytes object and then sets the checksum
        :return: None
        """
        try:
            self.__message_type = self.__message_type.encode()
        except AttributeError:
            pass

        try:
            self.__timestamp = self.__timestamp.encode()
        except AttributeError:
            pass

        try:
            self.__data = self.__data.encode()
        except AttributeError:
            pass

        self.__checksum = binascii.crc32(self.__message_type + self.__timestamp + self.__data)

    def get_checksum_error_crc(self, message_type, timestamp, data):
        """
        This function is used to verify the integrity of the checksum received
        :param message_type:
        :param timestamp:
        :param data:
        :return: checksum
        """

        try:
            message_type = message_type.encode()
        except AttributeError:
            pass

        try:
            timestamp = timestamp.encode()
        except AttributeError:
            pass

        try:
            data = data.encode()
        except AttributeError:
            pass

        self.__checksum = binascii.crc32(message_type + timestamp + data)
        return self.__checksum

    def set_timestamp_as_bytes(self):
        """
        Function used to set the timestamp as bytes
        :return: None
        """
        self.__timestamp = datetime.datetime.now()
        self.__timestamp = str(self.__timestamp).encode()

    def set_data_as_bytes(self, data):
        """
        Set the data as bytes before sending it
        :param data:
        :return: None
        """
        try:
            self.__data = data.encode()
        except AttributeError:
            self.__data = data

    def get_message_type(self):
        """
        Function to return message type
        :return:
        """
        return self.__message_type

    def get_checksum(self):
        """
        Used to return checksum
        :return: checksum
        """
        return self.__checksum

    def get_data(self):
        """
        Used to return data as string
        :return: data
        """
        return self.__data

    def get_timestamp(self):
        """
        Used to return timestamp as string
        :return:
        """
        return self.__timestamp

    def get_header(self, message_type, data):
        """
        Anytime the get header function is called, the class parameters re-initialized
        :param string message_type: This is the request on top of the header
        :param string data: This is the data to be sent
        :return: tuple ( byte message_type, int checksum, byte timestamp)
        """
        self.set_message_type_as_bytes(message_type)
        self.set_timestamp_as_bytes()
        self.set_data_as_bytes(data)
        self.set_checksum()

        # print(self.get_request(), self.get_checksum(), self.get_timestamp())
        return self.get_message_type(), self.get_checksum(), self.get_timestamp(), self.get_data()
