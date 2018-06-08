#!/usr/bin/env python

"""
@author: Francis Obiagwu
@software: SecureDocumentSharing
@file: SDSClient.py
@description: Client class that request for service from the server
@time: 6/6/18 6:24 PM
"""

import binascii
import math
import struct

from SDSHeader import SDSHeader


class SDSPdu:
    """
    The SDSPdu class creates an instance needed to send messages across sockets

    """

    __data = ''  # data set as private
    __BUFFER_SIZE = ''  # buffer size for sending and receiving pdu
    __HEADER_SIZE = ''  # header size for the pdu
    __SIZE_OF_DATA = ''  # size of data in bytes
    __SOCKET = ''  # socket class
    __PDU_SIZE = ''  # pdu size
    __MESSAGE_FORMAT = ''  # message format used for the struct, this is used place pdu parts appropriately
    __HEADER = ''  # used to create header parts

    # __error_checker = SDSHeader()

    def __init__(self, socket, buffer_size, header_size):
        """
        When an instance of SDSPdu is created, we assign the header and the data None value
        """
        self.__data = None
        self.__BUFFER_SIZE = buffer_size
        self.__HEADER_SIZE = header_size

        # the size of the data is the difference between buffer size and header size
        self.__SIZE_OF_DATA = self.__BUFFER_SIZE - self.__HEADER_SIZE
        self.__SOCKET = socket
        self.__HEADER = SDSHeader()
        self.__MESSAGE_FORMAT = '12s q 26s' + str(self.__SIZE_OF_DATA) + 's'  # set size for PDU

    def generate_byte(self, message_type, data_chunk):
        """
        Used to convert different pdu parts to bytes and final tuning before returning it for sending
        :param string message_type: The request field
        :param string data_chunk: The data to be sent
        :return Struct: pdu packed
        """

        # verify that the parameters are strings
        try:
            message_type = message_type.decode()
        except AttributeError:
            pass

        try:
            data_chunk = data_chunk.decode()
        except AttributeError:
            pass

        print('{} size of data '.format(self.__SIZE_OF_DATA))
        s = struct.Struct(self.__MESSAGE_FORMAT)
        self.__PDU_SIZE = s.size
        print('size of struct {}'.format(s.size))
        print('----getting headers---')
        message_type, checksum, timestamp, data = self.__HEADER.get_header(message_type, data_chunk)
        data_chunk = data_chunk.encode()  # convert the data chuck to bytes
        print('---done-----')
        print('message_type {} checksum {} timestamp {} data {}'.format(message_type, checksum, timestamp, data_chunk))
        pdu = (message_type, checksum, timestamp, data_chunk)
        print(pdu)
        pdu_packed = s.pack(*pdu)
        print(pdu_packed)
        print(binascii.hexlify(pdu_packed))

        print(s.unpack(pdu_packed))

        return pdu_packed

    def send(self, request, data):
        print('data :{} request: {}'.format(data, request))
        try:
            data = data.decode()
        except AttributeError:
            pass
        try:
            request = request.decode()
        except AttributeError:
            pass

        self.__data = data
        data_arr = self.chunk_messages(data)  # return the data array

        if data_arr is not None:
            # for every data_chunk in the array, send with different header,
            # since the checksum and timestamp will be different
            for d in data_arr:
                pdu = self.generate_byte(request, d)  # returns the pdu in byte
                print('sending')
                print(pdu)

                print('sending')

                self.__SOCKET.send(pdu)

        else:
            print('The array returned from chuck message is None')




    def chunk_messages(self, data, no_chunks=None):
        """
        :return type:  string[]
        """
        no_chunks = self.__SIZE_OF_DATA
        arr = []
        start = 0
        no_iterations = math.ceil(len(data) / no_chunks)
        stop = no_chunks

        for i in range(no_iterations):
            arr.append(data[start: stop])  # 0:4
            start = stop
            stop += no_chunks  # 4:8

        return arr

    def receive(self):
        print('Receiving....')
        binary_data = self.__SOCKET.recv(self.__BUFFER_SIZE)

        s = struct.Struct(self.__MESSAGE_FORMAT)
        # print('Size : {}'.format(s.size))
        try:
            message_type, checksum, timestamp, data_chunk = s.unpack(binary_data)
            message_type = message_type.decode('unicode_escape').encode('utf-8')
            timestamp = timestamp.decode('unicode_escape').encode('utf-8')
            data_chunk = data_chunk.decode('unicode_escape').encode('utf-8')




        except struct.error as err:
            print('size of struct: {}\n'
                  'size of data: {}\n'
                  'size of heaer: {}\n'
                  '\n{}'.format(s.size, self.__SIZE_OF_DATA, self.__HEADER_SIZE, err.args))

        return message_type, checksum, timestamp, data_chunk

    def get_buffer_size(self):
        return self.__BUFFER_SIZE

    def get_data_size(self):
        return self.__SIZE_OF_DATA

    def get_pdu_size(self):
        return self.__PDU_SIZE

    def error_check_crc(self, binary_data):
        request, checksum, timestamp, data = binary_data
        # verify if the received checksum is the same as the sent checksum
        if checksum == self.__error_checker.get_checksum_error_crc(request, timestamp, data):
            return True
        else:
            print(checksum, self.__error_checker.get_checksum_error_crc(request, timestamp, data))
            print("Error was found on the checksum")
            return False

    def convert_to_human_readable(self, hex_data):
        s = struct.Struct(self.__MESSAGE_FORMAT)
        data = hex_data  # stil in binary
        data = binascii.a2b_hex(data)

        print(data)

# from SDSDocument import SDSDocument
#
# doc = SDSDocument()
# document.txt = doc.get_document()
#
# test = SDSPdu(None, 100, 50)
#
# arr = test.chunk_messages(document.txt, 50)
# print(len(arr))
#
# for item in arr:
#     test.generate_byte('CONNECT', item)
