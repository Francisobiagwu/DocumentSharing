"""
@author: Francis Obiagwu
@software: SecureDocumentSharing
@file: SDSServer.py
@description: This is the server side that services client request
@time: 6/6/18 6:44 PM
"""

# !/usr/bin/env python

__author__ = "Francis Obiagwu"
__copyright__ = "Copyright 2017, GSCE IDS Project"
__version__ = "1.0"
__email__ = "francis.c.obiagwu.civ@mail.mil"

import socket
import threading

from SDSDocument import SDSDocument
from SDSPdu import BSCAPdu


class Server:
    """
    This is the server that responds to the clients requests. Messages received from the clients
    shall be line with the Deterministic Finite Automata (DFA), otherwise, the server shall not
    respond to the client
    """
    __HOST_NAME = socket.gethostname()
    __IP_ADDRESS = socket.gethostbyname(__HOST_NAME)
    __PORT = 5000
    __SERVER_SOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    __BUFFER_SIZE = 100
    __HEADER_SIZE = 50
    __SIZE_OF_DATA = __BUFFER_SIZE - __HEADER_SIZE

    def __init__(self, host_name=__HOST_NAME, ip_address=__IP_ADDRESS, port=__PORT, buffer_size=__BUFFER_SIZE,
                 size_of_header=__HEADER_SIZE, size_of_data=__SIZE_OF_DATA):
        """
        If the caller didn't specify any  host name, ip address or port number, the default is used
        :param str host_name: host name of computer
        :param str ip_address: IP address assigned to the computer
        :param str port: Port where the server process will run
        :return type : object
        """
        self.__HOST_NAME = host_name
        self.__IP_ADDRESS = ip_address
        self.__PORT = port
        self.__BUFFER_SIZE = buffer_size
        self.__HEADER_SIZE = size_of_header
        self.__SIZE_OF_DATA = size_of_data

    def send_m(self, m, thread_name, pdu: object):
        try:
            req = 'CONNECT'
            pdu.send(req, m)
        except ConnectionResetError as err:
            print('\nclient at {} closed ended connection'.format(thread_name))

    def recv_m(self, client_socket, thread_name, pdu: object):
        while True:
            try:
                m = pdu.receive()
                request, checksum, timestamp, data = m
                print(request, checksum, timestamp, data)

            except ConnectionResetError as err:
                print('\n{} connected client closed'.format(thread_name))
                break

    def client_thread(self, client_socket, client_address):
        """
        This thread is used to run all client connection to the server.
        This will allow the server to service multiple processes
        :param object client_socket: client's socket object
        :param tuple client_address: client's IP address and Port number
        :return: None
        """

        doc_object = SDSDocument()
        m_doc = doc_object.get_document()

        client_thread_name = threading.current_thread().getName()
        pdu_s = BSCAPdu(client_socket, self.__BUFFER_SIZE, self.__HEADER_SIZE)
        pdu_r = BSCAPdu(client_socket, self.__BUFFER_SIZE, self.__HEADER_SIZE)

        send_PDU = threading.Thread(target=self.send_m, args=(m_doc, client_thread_name, pdu_s))
        recv_m = threading.Thread(target=self.recv_m, args=(client_socket, client_thread_name, pdu_r))
        send_PDU.start()
        recv_m.start()

    def start(self):
        """
        This method is called to start the server
        :return: None
        """
        print('Server started @ {} {}'.format(self.__IP_ADDRESS, self.__PORT))

        self.__SERVER_SOCKET.bind((self.__IP_ADDRESS, self.__PORT))  # Bind the socket to the IP address and port
        self.__SERVER_SOCKET.listen(5)  # Listen for connection

        while True:
            client_socket, client_address = self.__SERVER_SOCKET.accept()
            print("connected to: {}".format(client_address))
            c_thread = threading.Thread(target=self.client_thread, args=(client_socket, client_address))
            c_thread.start()


def main():
    server = Server()
    server.start()


main()
