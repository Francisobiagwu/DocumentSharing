#!/usr/bin/env python

__author__ = "Francis Obiagwu"
__copyright__ = "Copyright 2017, GSCE IDS Project"
__version__ = "1.0"
__email__ = "francis.c.obiagwu.civ@mail.mil"

import socket
import sys

from BSCADocument import BSCADocument
from BSCAPdu import BSCAPdu


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
    __BSCAPduClient = None

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
        self.__BSCAPduClient = BSCAPdu(self.__CLIENT_SOCKET, self.__BUFFER_SIZE,
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

        doc_obj = BSCADocument()
        m_doc = doc_obj.get_document()

        self.__BSCAPduClient.send('CONNNECT', m_doc)
        print("----done sending----")
        print("----Now receiving----")

        while True:
            data_binary = self.__BSCAPduClient.receive()  # decode data when it is received
            # print(data_binary)
            request, checksum, timestamp, data = data_binary
            if self.__BSCAPduClient.error_check_crc(data_binary):
                print(request, checksum, timestamp, data)
                request = request.decode()
                timestamp = timestamp.decode()
                data = data.decode()
                print(request, timestamp, checksum, data)

            else:
                print('We had an error with the checksum')

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
