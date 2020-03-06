#!/usr/bin/env python
"""
@author: Francis Obiagwu
@software: SecureDocumentSharing
@file: DSClient.py
@time: 6/6/18 7:16 PM
"""

import socket
import sys
import threading
import os

from DSCodes import DSCode
from DSInput import DSInput
from DSPdu import DSPdu
from DSClientServerResponseProcessor import DSClientServerResponseProcessor


class DSClient:
    """
    The DSClient class is used to create a client connection. To avoid error, the server object has
    to be started first before starting the client object
    """
    __BUFFER_SIZE = None
    __PORT = 5005
    __TCP_IP = '127.0.0.1'
    __CLIENT__SOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    placement = 0

    def __init__(self):
        self.client_pdu = DSPdu()  # create new pdu object
        self.allowed_data_size = self.client_pdu.get_data_size()
        self.__BUFFER_SIZE = self.client_pdu.get_buffer_size()  # set the size of the pdu
        self.done_processing = False
        self.client_ds_code = DSCode()
        self.message_type_index, self.timestamp_index, self.error_code_index, self.flag_index,  self.changed_section_index, self.section_id_index, self.reserved_1_index, self.reserved_2_index, self.reserved_3_index, self.data,self.data_size_index, self.checksum_index = DSPdu().get_pdu_parts_index()
        self.null_byte = b'\x00'  # used in place of data when is not need to send data during S_DENIED, CAUTH etc
        self.input_processor = DSInput()
        self.server_response_processor = DSClientServerResponseProcessor()

        self.first_message_recvd = False  # used to track if the client have received the first 'CONNECT' message
        self.placement = 0
        self.is_authenticated = False
        self.server_alive = False

    def start( self ):
        """
        Used to start the client
        :return: None
        """
        try:
            self.__CLIENT__SOCKET.connect((self.__TCP_IP, self.__PORT))
            self.server_alive = True
            # print('client successfully connected')
        except ConnectionRefusedError as err:
            print(err.args)
            os._exit(1)

        #################################################
        # receive and send the first message
        #################################################

        while not self.first_message_recvd:
            # wait here until the server sends you the first message
            pdu = self.__CLIENT__SOCKET.recv(self.__BUFFER_SIZE)
            # print(pdu)
            array = self.client_pdu.remove_padding(self.client_pdu.unpack(pdu))
            if self.server_response_processor.process_response(array, self.__CLIENT__SOCKET, self):
                break
            else:
                print('The server doesn\'t want to talk to you')
                os._exit(1)

        # run the thread to receive pdu from the server, this thread runs forever
        recv_thread = threading.Thread(target=self.receiving_thread).start()

        while self.server_alive:
            array, string_array = self.input_processor.get_user_input()  # return the user input as array and as string
            if array[0] == 'COMMIT':
                # process differently
                # print(array, string_array)
                commit_pdu_array = self.input_processor.process_user_input(array, string_array)
                for item in commit_pdu_array:
                    print(item)
                    pdu = self.client_pdu.pack(item)
                    self.__CLIENT__SOCKET.send(pdu)
                    print('packed pdu sent: {}'.format(pdu))

            else:
                pdu_array = self.input_processor.process_user_input(array, string_array)  # obtain the pdu as byte
                print(pdu_array)
                pdu = self.client_pdu.pack(pdu_array)
                self.__CLIENT__SOCKET.send(pdu)  # send

            if array[0] == "LOGOFF":
                self.server_alive = False
                os._exit(-1)

    def receiving_thread( self ):
        """
        Used to run the receiving thread forever
        :return: None
        """
        while self.server_alive: # if the server is still listening for this client
            try:
                pdu = self.__CLIENT__SOCKET.recv(self.__BUFFER_SIZE)
                # print(pdu)
                unpacked_pdu = self.client_pdu.unpack(pdu)
                unpacked_no_pad = self.client_pdu.remove_padding(unpacked_pdu)
                self.server_response_processor.process_response(unpacked_no_pad, self.__CLIENT__SOCKET, self)

            except ConnectionResetError as err:
                print(err.args)
                self.server_alive = False

                os._exit(1)



if __name__ == '__main__':
    try:
        a = DSClient()
        a.start()
    except (KeyboardInterrupt, EOFError, OSError, IOError) as err:
        print(err.args)
        os._exit(1)
