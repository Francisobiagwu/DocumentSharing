#!/usr/bin/env python

"""
@author: Francis Obiagwu
@software: SecureDocumentSharing
@file: DSServer.py
@time: 6/6/18 7:16 PM
"""

import binascii
import socket
import threading
from datetime import datetime

from DSAuthentication import DSAuthentication
from DSCodes import DSCode
from DSDocument import DSDocument
from DSErrorCorrection import DSErrorCorrection
from DSFlags import DSFlags
from DSMessageType import DSMessageType
from DSPdu import DSPdu
from DSPrintStyle import Color, Style
from DSServerLogManagement import DSServerLogManagement
from DSState import DSState


class DSServer:
    """
    Used to create our server object
    """
    __BUFFER_SIZE = None
    __PORT = 5001
    __TCP_IP = '127.0.0.1'
    __SERVER_SOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    __username = 'Admin'
    __password = 'root'
    __document_name = 'example1'

    def __init__(self, buffer_size=__BUFFER_SIZE):
        self.__BUFFER_SIZE = buffer_size
        self.__SERVER_SOCKET.bind((self.__TCP_IP, self.__PORT))
        self.ds_document = DSDocument(DSPdu().get_data_size())  # we are going to change this into some variable later
        self.document_as_string = None
        self.document_as_dic = None
        self.null_byte = b'\x00'
        self.message_type_index, self.timestamp_index, self.error_code_index, self.flag_index, self.reserved_1_index, self.reserved_2_index, self.section_id_index, self.data_index, self.checksum_index = DSPdu().get_pdu_parts_index()
        self.server_log_manager = DSServerLogManagement()
        self.string_builder = ''
        self.control_ack = {}
        self.color = Color()
        self.style = Style()
        self.authentication = DSAuthentication()

    def start(self):
        self.__SERVER_SOCKET.listen(1)
        str_to_print = 'SERVER started @ {} {}\n'.format(self.__TCP_IP, self.__PORT)
        print(str_to_print)
        self.server_log_manager.log_server_start(str_to_print)

        while True:
            client_socket, client_address = self.__SERVER_SOCKET.accept()
            self.server_log_manager.add_client_connection(client_socket, client_address)
            print('connected to {}'.format(client_address))

            c_thread = threading.Thread(target=self.client_thread, args=(client_socket, client_address)).start()

    def client_thread(self, client_socket, client_address):
        # create pdu object for the client, this happens only once for each client

        authorized = False  # now the client have no authorization
        client_state = DSState()  # create client state object
        client_pdu = DSPdu()  # create pdu object
        self.__BUFFER_SIZE = client_pdu.get_size()  # set the buffer size

        client_error_correction = DSErrorCorrection()

        ###############################
        # send the first hello message#
        ###############################

        # assign the pdu parameters

        issued_token = False
        token_id = ''

        # send connect message to the client and then start the timer immediately

        connect_thread = threading.Thread(target=self.connect, args=(
            client_state, client_pdu, client_socket, client_address, client_error_correction))
        connect_thread.start()

        # self.connect(client_state, client_pdu, client_socket, client_address, client_timer)

        ###################################
        # Now receive message and process #
        ###################################
        while True:
            try:
                pdu = client_socket.recv(self.__BUFFER_SIZE)
                # print('buffer size: {}'.format(self.__BUFFER_SIZE))
                unpacked_pdu = client_pdu.unpack(pdu)
                unpacked_pdu_no_pad = client_pdu.remove_padding(unpacked_pdu)

            except ConnectionResetError as err:
                print(err.args)
                str_to_print = 'The client @ {} closed connection'.format(client_address)
                print(str_to_print)
                self.server_log_manager.remove_client_connection(client_socket, client_address)
                break

                # CHECK STATE, IF THE CLIENT IS NOT FOLLOWING STATE, REJECT#

            current_state = client_state.get_current_state()
            message_type = unpacked_pdu_no_pad[self.message_type_index].encode()
            data = unpacked_pdu_no_pad[self.data_index]
            section_id = unpacked_pdu_no_pad[self.section_id_index]
            flag = unpacked_pdu_no_pad[self.flag_index].encode()
            print(current_state, message_type)
            if message_type == DSMessageType.CONNECT:
                pass
            elif message_type == DSMessageType.CAUTH:
                client_error_code = None
                self.cauth(data, client_state, client_pdu, client_socket, client_address, client_error_correction)

            elif message_type == DSMessageType.S_EDIT:
                self.s_edit(section_id, client_state, client_pdu, client_socket, client_address,
                            client_error_correction)

            elif message_type == DSMessageType.S_COMMIT:
                print(data, flag)
                print('data before the concatonation: {}'.format(data))
                print(client_pdu, unpacked_pdu, unpacked_pdu_no_pad)
                if flag == DSFlags.more:
                    self.string_builder += data
                    print('string after concatenation')
                    print('string {}'.format(self.string_builder))

                else:  # flag == DSFlags.finish:
                    if self.string_builder != '':  # if string builder contains something
                        data = self.string_builder
                        print('data: {}'.format(data))
                        self.string_builder = ''  # reset string builder

                    else:
                        # if string builder is None, then data that was sent for commit is equal to the size of struct
                        pass

                    self.s_commit(section_id, data, client_state, client_pdu, client_socket, client_address,
                                  client_error_correction)

            elif message_type == DSMessageType.S_RELEASE:
                self.release(section_id, client_pdu, client_state, client_socket, client_address)

            elif message_type == DSMessageType.CLOSE:
                self.close(client_pdu, client_state, client_socket, client_address)

    def connect(self, client_state, client_pdu, client_socket, client_address, client_error_correction,
                client_error_code=None):
        # assign the resigning parameters
        message_type = DSMessageType.CONNECT
        timestamp = client_pdu.get_time()  # get timestamp
        reserved_1 = self.null_byte
        reserved_2 = self.null_byte
        data = b'HELLO CLIENT'
        section_id = self.null_byte
        checksum = client_pdu.get_checksum(timestamp, data)
        flag = DSFlags.finish
        if client_error_code is None:
            error_code = DSCode.CONNECTED
        else:
            error_code = client_error_code

        # add recently sent data to the error-correction-tracker

        pdu_array = [message_type, timestamp, error_code, flag, reserved_1, reserved_2, section_id,
                     data, checksum]
        client_error_correction.add_recently_sent_data(data, checksum, message_type, flag)

        ##################################
        # set state#
        ##################################
        print(pdu_array)

        pdu = client_pdu.pack(pdu_array)
        print(pdu)
        client_state.set_state(DSState.CONNECTED)
        client_socket.send(pdu)
        # # start timer for ack
        # timer_thread = threading.Thread(target=client_timer.start_timer()).start()

    def cauth(self, data, client_state, client_pdu, client_socket, client_address, client_error_correction,
              client_error_code=None):
        # verify if the client presented a valid credentials
        # send an ACK to inform the client that they have been authenticated
        print(self.color.green('hey'))

        if client_error_code is None:
            error_code = DSCode.LOGIN_SUCCESS
            _, username, password, document_name = data.split(',')

            if username == self.authentication.get_username() and password == self.authentication.get_password() and document_name == self.authentication.get_document_name():

                self.server_log_manager.add_authenticated_client_connection(client_socket, client_address)
                # Now send the document.txt to the client
                data_string = self.ds_document.get_document_as_string()  # get the entire document.txt as string
                data_break_down = self.ds_document.break_data(data_string)

                freq_to_send = len(data_break_down)
                count = 0

                for item in data_break_down:  # we don't care about the document.txt flags about sections taken/free
                    count += 1
                    timestamp = client_pdu.get_time()  # get timestamp
                    error_code = DSCode.LOGIN_SUCCESS  # assign error code
                    if count == freq_to_send:
                        flag = DSFlags.finish
                    else:
                        flag = DSFlags.more

                    reserved_1 = self.null_byte
                    reserved_2 = self.null_byte
                    section_id = str(count - 1).encode()
                    data = item  # verify if the data is already encoded
                    checksum = client_pdu.get_checksum(timestamp, data)
                    pdu_array = [DSMessageType.CAUTH, timestamp, error_code, flag, reserved_1, reserved_2, section_id,
                                 data,
                                 checksum]
                    pdu = client_pdu.pack(pdu_array)
                    #############################################
                    # SEND THE DOCUMENT
                    #############################################
                    client_socket.send(pdu)
                    ##################################
                    # set state#
                    ##################################
                    client_state.set_state(DSState.AUTHENTICATED)
                    print('item : {}'.format(item))
                    print('pdu before send: {}'.format(pdu))

            else:
                client_state.CONNECTED
                print(self.color.red('Client presented wrong credentials'))
                self.connect(client_state, client_pdu, client_socket, client_address, client_error_correction,
                             DSCode.LOGIN_NOT_SUCCESS)
        else:
            error_code = client_error_code
            timestamp = client_pdu.get_time()  # get timestamp
            reserved_1 = self.null_byte
            reserved_2 = self.null_byte
            section_id = self.null_byte
            data = data  # verify if the data is already encoded
            checksum = client_pdu.get_checksum(timestamp, data)
            pdu_array = [DSMessageType.CAUTH, timestamp, error_code, DSFlags.finish, reserved_1, reserved_2, section_id,
                         data,
                         checksum]
            pdu = client_pdu.pack(pdu_array)
            #############################################
            # SEND THE DOCUMENT
            #############################################
            client_socket.send(pdu)
            ##################################
            # set state#
            ##################################
            client_state.set_state(DSState.AUTHENTICATED)

    def s_edit(self, section_id, client_state, client_pdu, client_socket, client_address, client_error_correction,
               client_error_code=None):
        authenticated_clients = self.server_log_manager.get_authenticated_clients()
        print('in s_edit')
        print('authenticated clients: {}'.format(authenticated_clients))

        # verify if the user is authenticated
        if client_socket in authenticated_clients:
            section_id = int(section_id)
            error_code = ''
            if client_error_code is None:
                error_code = DSCode.SECTION_RETRIEVED

            else:
                error_code = error_code
            print(self.ds_document.get_document_sections())

            # if the section id given by the client corresponds to the section id they currently possess
            if section_id in self.ds_document.get_document_sections():
                print('Before')
                print(self.ds_document.get_document_sections())
                section_data_tuple = self.ds_document.get_document_sections().get(section_id)
                section_data = section_data_tuple[0]
                is_free = section_data_tuple[1]

                # find out if the section the user requested for is free.
                if is_free:
                    print(self.ds_document.get_document_sections())
                    self.server_log_manager.add_section_owners(client_address, section_id)
                    self.ds_document.get_document_sections().update(
                        {section_id: (section_data, False)})  # set flag on data
                    print('the section data : {}'.format(section_data))
                    print('After dictionary flags')
                    print(self.ds_document.get_document_sections())

                    request = b'S_EDIT'
                    timestamp = client_pdu.get_time()  # get timestamp\
                    flag = DSFlags.finish
                    reserved_1 = self.null_byte
                    reserved_2 = self.null_byte
                    section_id = str(section_id).encode()
                    data = section_data
                    checksum = client_pdu.get_checksum(timestamp, data)
                    pdu_array = [request, timestamp, error_code, flag, reserved_1, reserved_2, section_id, data,
                                 checksum]
                    pdu = client_pdu.pack(pdu_array)
                    ##################################
                    # set state#
                    ##################################
                    client_state.set_state(DSState.EDITING_DOCUMENT)
                    self.server_log_manager.log(client_address, DSState.EDITING_DOCUMENT)
                    #############################################
                    # SEND THE DOCUMENT
                    #############################################
                    client_socket.send(pdu)

                else:  # data is not free
                    # find out who is the current owner of the document.txt
                    #
                    current_section_owners = self.server_log_manager.get_section_owners()
                    data = b''
                    if client_address in current_section_owners.values():
                        data = b'You are the current section owner'

                    else:
                        for key, value in current_section_owners.items():
                            if key == section_id:
                                data = value.encode() + b' is the current owner'
                    request = b'S_EDIT'
                    timestamp = client_pdu.get_time()  # get timestamp
                    error_code = DSCode.SECTION_NOT_AVAILABLE  # assign error code
                    flag = DSFlags.finish
                    reserved_1 = self.null_byte
                    reserved_2 = self.null_byte
                    section_id = self.null_byte
                    checksum = client_pdu.get_checksum(timestamp, data)
                    pdu_array = [request, timestamp, error_code, flag, reserved_1, reserved_2, section_id, data,
                                 checksum]
                    pdu = client_pdu.pack(pdu_array)
                    print(data)
                    ##################################
                    # set state#
                    ##################################
                    client_state.set_state(DSState.BLOCKED)
                    #############################################
                    # SEND THE DOCUMENT
                    #############################################
                    client_socket.send(pdu)
                    print(pdu)
                    issued_token = False
                    token_id = None
                    return issued_token, token_id

            # if the section id presented by the client is invalid or they don't possess a token for it
            else:
                issued_token = False
                token_id = None
                return issued_token, token_id

        # if the user is not authenticated
        else:
            self.connect(client_state, client_pdu, client_socket, client_address, client_error_correction,
                         DSCode.USER_NOT_AUTHENTICATED)

    def s_commit(self, section_id, data, client_state, client_pdu, client_socket, client_address,
                 client_error_correction,
                 client_error_code=None):
        print('in the server commit section ')
        print('authenticated clients: {}'.format(self.server_log_manager.get_authenticated_clients()))
        print('section owners: {}'.format(self.server_log_manager.get_section_owners().values()))
        print(self.server_log_manager.get_section_owners())
        # we have to verify if the client have token for the section to which they are committing

        # if the client exists in the list of authenticated clients and the client possesses the token for the section
        if client_socket in self.server_log_manager.authenticated_clients and client_address in self.server_log_manager.get_section_owners().values():
            print(self.color.yellow('client possess a token for this commit'))
            print('client address: {} section id: {}'.format(client_address, section_id))
            print('key: ', end='')
            print(self.server_log_manager.get_section_owners().get(section_id))
            print(type(section_id))

            if client_address == self.server_log_manager.get_section_owners().get(int(section_id)):
                print('data {}'.format(data))
                self.ds_document.update_document(section_id, data)
                ##################################
                # set state#
                ##################################
                client_state.set_state(DSState.COMMITTING_CHANGES)
                self.server_log_manager.log(client_address, client_state.get_current_state())
                #############################################
                print('authenticated clients: {}'.format(self.server_log_manager.authenticated_clients))

                for clients in self.server_log_manager.authenticated_clients:
                    # send the update to them
                    timestamp = client_pdu.get_time()  # get timestamp
                    reserved_1 = self.null_byte
                    reserved_2 = self.null_byte
                    ACK_data = self.null_byte
                    checksum = client_pdu.get_checksum(timestamp, ACK_data)
                    pdu_array = [DSMessageType.CAUTH, timestamp, DSCode.COMMIT_UPDATE, DSFlags.finish, reserved_1,
                                 reserved_2,
                                 self.null_byte, ACK_data, checksum]

                    pdu = client_pdu.pack(pdu_array)
                    client_socket.send(pdu)
                    self.server_log_manager.add_authenticated_client_connection(client_socket, client_address)


                    # Now send the document.txt to the client
                    data_string = self.ds_document.get_document_as_string()  # get the entire document.txt as string
                    data_break_down = self.ds_document.break_data(data_string)

                    freq_to_send = len(data_break_down)
                    count = 0

                    for item in data_break_down:  # we don't care about the document.txt flags about sections taken/free
                        count += 1
                        timestamp = client_pdu.get_time()  # get timestamp
                        error_code = DSCode.COMMIT_UPDATE  # assign error code
                        if count == freq_to_send:
                            flag = DSFlags.finish
                        else:
                            flag = DSFlags.more

                        reserved_1 = self.null_byte
                        reserved_2 = self.null_byte
                        section_id = str(count - 1).encode()
                        data = item  # verify if the data is already encoded
                        checksum = client_pdu.get_checksum(timestamp, data)
                        pdu_array = [DSMessageType.CAUTH, timestamp, error_code, flag, reserved_1, reserved_2,
                                     section_id, data,
                                     checksum]
                        pdu = client_pdu.pack(pdu_array)

                        client_state.set_state(DSState.COMMITTING_CHANGES)

                        # SEND THE DOCUMENT
                        #############################################
                        client_socket.send(pdu)
                        # print('item : {}'.format(item))
                        # print('pdu before send: {}'.format(pdu))
            else:
                self.s_edit(section_id, client_state, client_pdu, client_socket, client_address,
                            DSCode.SECTION_ID_NOT_VALID)


        # if the client exist in the authenticated client list but the client doesn't possess the token for the section which they are requesting
        elif client_socket in self.server_log_manager.get_authenticated_clients() and client_address not in self.server_log_manager.get_section_owners().values():

            print(self.color.red('testing'))
            print('testing for the keys')
            x = [value for value in self.server_log_manager.get_section_owners().values()]
            print(x)
            print('testing for keys end')
            print('client_address: ' + str(client_address))
            print(self.server_log_manager.get_section_owners().keys())
            print(self.server_log_manager.get_section_owners())
            print(self.server_log_manager.get_authenticated_clients())
            data = self.null_byte
            self.cauth(data, client_state, client_pdu, client_socket, client_address, client_error_correction,
                       DSCode.SECTION_DENIED)

        # if the client is neither authenticated nor authorized
        else:
            self.connect(client_state, client_pdu, client_socket, client_address, client_error_correction,
                         DSCode.USER_NOT_AUTHENTICATED)

    def close(self):
        pass

    def release(self, section_id, client_pdu, client_state, client_socket, client_address):
        self.ds_document.release(section_id)
        # should we send an acknowledgement to the client informing them that the section was
        # successfully released?

    @staticmethod
    def get_time():
        return str(datetime.now()).encode('utf-8')

    @staticmethod
    def get_checksum(timestamp, data):
        try:
            return binascii.crc32(timestamp + data)
        except TypeError as err:
            print('This value {} is not a byte'.format(data))

    @staticmethod
    def remove_space(array):
        new_array = []
        for item in array:
            new_array.append(item.strip())

        return new_array

    def response(self, request, error_code, data):
        """
        This is used to break server response to be sent into chucks of pdu
        ie if data = 'Access denied'
        the output is similar to [[b'S_DATA', 3434343, b'timestamp, b'Access ], [b'S_DATA', 36674545, b'timestamp, b'Denied']]
        :param byte request:
        :param string data:
        :return: list
        """
        array = []
        if request == b'CAUTH' and data != self.__null_byte:
            # process differently
            data_array = self.ds_document.break_data(data)
            # print('after data is broken: {}'.format(data_array))
            for item in data_array:  # for all the items we have to generate a different timestamp and checkum
                timestamp = self.get_time()
                checksum = self.get_checksum(timestamp, item)
                array.append([request, checksum, timestamp, error_code, item])
            # print(array)
            # print(array)
            return array

        else:  # if we are sending a generic response, then
            timestamp = self.get_time()
            checksum = self.get_checksum(timestamp, data)

            array = [request, checksum, timestamp, error_code, data]
            return array

    def response_document(self, request, error_code, data_array):
        """
        Used for sending documents only
        :param data_array:
        :return:
        """

        if (request == b'CAUTH' or request == b'S_DATA') and type(data_array) is list:
            array = []
            for item in data_array:  # for all the items we have to generate a different timestamp and checkum
                timestamp = self.get_time()
                checksum = self.get_checksum(timestamp, item)
                array.append([request, checksum, timestamp, error_code, item])
            # print(array)
            # print(array)
            return array


if __name__ == '__main__':
    try:
        server = DSServer()
        server.start()

    except (KeyboardInterrupt, OSError) as err:
        print(err.args)
        import sys

        sys.exit(1)

    finally:
        sys.exit(1)
