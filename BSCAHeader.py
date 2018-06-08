#!/usr/bin/env python

__author__ = "Francis Obiagwu"
__version__ = "1.0"

import binascii
import datetime


class BSCAHeader:
    __request = ''
    __checksum = ''
    __timestamp = ''
    __timestamp_crc = None
    __data = ''

    def __init__(self):
        self.__request = None  # 8 bytes
        self.__checksum = None  #
        self.__timestamp = None
        self.__data = None

    def set_request_as_bytes(self, req):
        try:
            self.__request = req.encode()
        except AttributeError:
            pass

    def set_checksum(self):
        """
        converts the data into bytes object and then sets the checksum
        :return: None
        """
        try:
            self.__request = self.__request.encode()
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

        self.__checksum = binascii.crc32(self.__request + self.__timestamp + self.__data)

    def get_checksum_error_crc(self, request, timestamp, data):

        try:
            request = request.encode()
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

        self.__checksum = binascii.crc32(request + timestamp + data)
        return self.__checksum

    def set_timestamp_as_bytes(self):
        self.__timestamp = datetime.datetime.now()
        self.__timestamp = str(self.__timestamp).encode()

    def set_timestamp_for_crc(self, t):
        self.__timestamp_crc = t

    def get_timestamp_crc(self):
        return self.__timestamp_crc

    def set_data_as_bytes(self, data):
        try:
            self.__data = data.encode()
        except AttributeError:
            self.__data = data

    def get_request(self):
        return self.__request

    def get_checksum(self):
        return self.__checksum

    def get_data(self):
        return self.__data

    def get_timestamp(self):
        return self.__timestamp

    def get_header(self, req, data):
        """
        Anytime the get header function is called, the class parameters re-initialized
        :param string req: This is the request on top of the header
        :param string data: This is the data to be sent
        :return: tuple ( byte request, int checksum, byte timestamp)
        """
        self.set_request_as_bytes(req)
        self.set_timestamp_as_bytes()
        self.set_data_as_bytes(data)
        self.set_checksum()

        # print(self.get_request(), self.get_checksum(), self.get_timestamp())
        return self.get_request(), self.get_checksum(), self.get_timestamp()
