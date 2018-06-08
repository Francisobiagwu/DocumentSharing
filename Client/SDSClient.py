# !/usr/bin/env python
"""
@author: Francis Obiagwu
@software: SecureDocumentSharing
@file: SDSClient.py
@description: Client class that request for service from the server
@time: 6/6/18 6:24 PM
"""

import socket
import sys

from SDSPdu import SDSPdu


class Client():
    """
    The Client class is used to create a client connection. To avoid error, the server object has
    to be started first before starting the client object
    """

    __HOST_NAME = socket.gethostname()
    __IP_ADDRESS = socket.gethostbyname(__HOST_NAME)
    __PORT = 5000
    __CLIENT_SOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    __BUFFER_SIZE = 100
    __SIZE_OF_HEADER = 50
    __SIZE_OF_DATA = __BUFFER_SIZE - __SIZE_OF_HEADER
    __sds_pdu_client = None

    def __init__(self, host_name=__HOST_NAME, ip_address=__IP_ADDRESS, port=__PORT):
        """
        if the user didn't specify,computer attributes, use the default
        :param str host_name: the computer name
        :param str ip_address: the ip address of the computer
        :param int port: client's port
        """
        self.__HOST_NAME = host_name
        self.__IP_ADDRESS = ip_address
        self.__PORT = port
        self.__sds_pdu_client = SDSPdu(self.__CLIENT_SOCKET, self.__BUFFER_SIZE,
                                       self.__SIZE_OF_HEADER)  # create a sending and receiving object for the client

    def start(self):
        """
        start the client
        :return:
        """
        try:
            self.__CLIENT_SOCKET.connect((self.__IP_ADDRESS, self.__PORT))  # connect the client to the server
            print('connected to {} {}'.format(self.__IP_ADDRESS, self.__PORT))

        except ConnectionRefusedError as err:
            print("We ran into errors!!!")
            print(err.args)
            sys.exit(1)

        print("----Now receiving----")

        while True:
            data_binary = self.__sds_pdu_client.receive()  # decode data when it is received
            # print(data_binary)
            # call the function that will remove excess padding and then print
            # print(data_binary)

            message_type, checksum, timestamp, data = self.__sds_pdu_client.remove_pdu_padding(data_binary)
            # print(message_type, checksum, timestamp, data)
            message_type = message_type.decode()
            timestamp = timestamp.decode()
            data = data.decode()
            # print(message_type, timestamp, checksum, data)
            print(data, end='')

    def get_server_name(self):
        return self.__HOST_NAME

    def get_server_ip_addr(self):
        return self.__IP_ADDRESS


def main():
    client = Client()
    print(client.get_server_name())
    print(client.get_server_ip_addr())
    client.start()


if __name__ == "__main__":
    main()
