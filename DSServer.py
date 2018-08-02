#!/usr/bin/env python

"""
@author: Francis Obiagwu
@software: SecureDocumentSharing
@file: DSServer.py
@time: 6/6/18 7:16 PM
"""

import binascii
import os
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
from DSStringBuilder import DSStringBuilder


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

    def __init__( self ):
        self.server_pdu = DSPdu()
        self.__BUFFER_SIZE = self.server_pdu.get_buffer_size()
        self.__SERVER_SOCKET.bind((self.__TCP_IP, self.__PORT))
        self.ds_document = DSDocument(DSPdu().get_data_size())  # we are going to change this into some variable later
        self.null_byte = b'\x00'
        self.message_type_index, self.timestamp_index, self.error_code_index, self.flag_index, self.changed_section_index, self.section_id_index, self.reserved_1_index, self.reserved_2_index, self.reserved_3_index, self.data_index, self.data_size_index, self.checksum_index = DSPdu().get_pdu_parts_index()
        self.server_log_manager = DSServerLogManagement()
        self.string_builder = ''
        self.control_ack = {}
        self.color = Color()
        self.style = Style()
        self.authentication = DSAuthentication()





    def start( self ):
        self.__SERVER_SOCKET.listen(1)
        str_to_print = 'SERVER started @ {} {}\n'.format(self.__TCP_IP, self.__PORT)
        print(self.color.biege(str_to_print))
        self.server_log_manager.log_server_start(str_to_print)

        while True:
            client_socket, client_address = self.__SERVER_SOCKET.accept()
            self.server_log_manager.add_client_connection(client_socket, client_address)
            print('connected to: {}'.format(self.color.green(str(client_address))))

            c_thread = threading.Thread(target=self.client_thread, args=(client_socket, client_address)).start()

    def client_thread( self, client_socket, client_address ):
        # create pdu object for the client, this happens only once for each client

        authorized = False  # now the client have no authorization
        client_state = DSState()  # create client state object
        client_pdu = DSPdu()  # create pdu object
        client_string_builder = DSStringBuilder()
        self.__BUFFER_SIZE = client_pdu.get_buffer_size()  # set the buffer size

        client_error_correction = DSErrorCorrection()

        ###############################
        # send the first hello message#
        ###############################

        # assign the pdu parameters

        client_state.token_issued = False
        token_id = ''

        # send connect message to the client and then start the timer immediately

        connect_thread = threading.Thread(target=self.connect, args=(
            client_state, client_pdu, client_socket, client_address, client_error_correction))
        connect_thread.start()

        # self.connect(client_state, client_pdu, client_socket, client_address, client_timer)

        ###################################
        # Now receive message and process #
        ###################################
        client_state.is_client_alive = True
        while client_state.is_client_alive:
            try:
                pdu = client_socket.recv(self.__BUFFER_SIZE)
                # print('buffer size: {}'.format(self.__BUFFER_SIZE))
                print(pdu)
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
            # print('unpacked pdu without padding: {}'.format(unpacked_pdu_no_pad))

            message_type = unpacked_pdu_no_pad[self.message_type_index].encode()
            timestamp = unpacked_pdu_no_pad[self.timestamp_index]
            error_code = unpacked_pdu_no_pad[self.error_code_index]
            flag = unpacked_pdu_no_pad[self.flag_index].encode()
            data_size = unpacked_pdu_no_pad[self.data_size_index]
            changed_section = unpacked_pdu_no_pad[self.changed_section_index]
            section_id = unpacked_pdu_no_pad[self.section_id_index]
            reserved_1 = unpacked_pdu_no_pad[self.reserved_1_index]
            reserved_2 = unpacked_pdu_no_pad[self.reserved_2_index]
            reserved_3 = unpacked_pdu_no_pad[self.reserved_3_index]
            data = unpacked_pdu_no_pad[self.data_index]

            # print(current_state, message_type)
            if message_type == DSMessageType.CONNECT:
                pass
            elif message_type == DSMessageType.CAUTH:
                client_error_code = None
                self.cauth(data, client_state, client_pdu, client_socket, client_address, client_error_correction)


            elif message_type == DSMessageType.CREATE:
                pass

            elif message_type == DSMessageType.S_EDIT:
                self.s_edit(section_id, client_state, client_pdu, client_socket, client_address,
                            client_error_correction)

            elif message_type == DSMessageType.S_COMMIT:
                # print(data, flag)
                # print('data before the concatenation: {}'.format(data))
                # print(client_pdu, unpacked_pdu, unpacked_pdu_no_pad)

                if flag == DSFlags.more or flag == DSFlags.begin:
                    client_string_builder.append(data)
                    print(self.color.yellow('string after concatenation'))
                    print('string {}'.format(client_string_builder.text))
                    print('----------------------------------------------')

                else:  # flag == DSFlags.finish:
                    if client_string_builder.text != '':  # if client string builder contains something
                        client_string_builder.append(data)
                        data = client_string_builder.text
                        print(self.color.biege('data received from the client to be committed: {}'.format(data)))
                        client_string_builder.reset()  # reset string builder

                    else:
                        # if string builder is None, then data that was sent for commit is equal to the size of struct
                        pass

                self.s_commit(section_id, data, client_state, client_pdu, client_socket, client_address,
                                  client_error_correction)

            elif message_type == DSMessageType.S_RELEASE:
                self.release(section_id, client_pdu, client_state, client_socket, client_address)

            elif message_type == DSMessageType.LOGOFF:
                self.close(client_pdu, client_state, client_socket, client_address)


            else:
                print('an error have occured!!!')

    def connect( self, client_state, client_pdu, client_socket, client_address, client_error_correction,
                 client_error_code=None ):
        # assign the resigning parameters
        message_type = DSMessageType.CONNECT
        timestamp = client_pdu.get_time()
        error_code = ''
        changed_section = 0
        section_id = 0
        reserved_1 = self.null_byte
        reserved_2 = self.null_byte
        reserved_3 = self.null_byte
        data = b'HELLO CLIENT'
        data_size = len(data)
        checksum = client_pdu.get_checksum(timestamp, data)
        flag = DSFlags.finish
        if client_error_code is None:
            error_code = DSCode.CONNECTED
        else:
            error_code = client_error_code

        # add recently sent data to the error-correction-tracker

        pdu_array = [message_type, timestamp, error_code, flag, changed_section, section_id, reserved_1, reserved_2,
                     reserved_3,
                     data, data_size, checksum]
        client_error_correction.add_recently_sent_data(data, checksum, message_type, flag)

        ##################################
        # set state#
        ##################################
        # print(pdu_array)

        pdu = client_pdu.pack(pdu_array)
        # print(pdu)
        client_state.set_state(DSState.CONNECTED)
        client_socket.send(pdu)
        # # start timer for ack
        # timer_thread = threading.Thread(target=client_timer.start_timer()).start()

    def cauth( self, data, client_state, client_pdu, client_socket, client_address, client_error_correction,
               client_error_code=None ):
        # verify if the client presented a valid credentials
        if client_error_code is None:
            error_code = DSCode.LOGIN_SUCCESS
            _, username, password, document_name = data.split(',')

            if username == self.authentication.get_username() and password == self.authentication.get_password() and document_name == self.authentication.get_document_name():

                self.server_log_manager.add_authenticated_client_connection(client_socket, client_address)
                # Now send the document.txt to the client
                # when we start the server, we want the server to read the document once, and then update with the latest
                # using the dictionary, otherwise, the server won't be able to keep track of which client have the section

                freq_to_send = len(self.ds_document.document_as_dic)
                print('data to be sent')
                print('---------------')
                for item in self.ds_document.document_as_dic.values():
                    print(self.color.yellow(item[0].decode()))


                count = 1
                self.server_log_manager.document_sent_to_client.update(
                    {client_address: dict(self.ds_document.document_as_dic)})

                client_state.set_as_previous_document(self.ds_document.document_as_dic)

                for section_details, section_id in zip(self.ds_document.document_as_dic.values(),
                                                       self.ds_document.document_as_dic.keys()):  # we don't care about the document.txt flags about sections taken/free
                    message_type = DSMessageType.CAUTH
                    timestamp = client_pdu.get_time()  # get timestamp
                    error_code = DSCode.LOGIN_SUCCESS  # assign error code
                    data = section_details[0]
                    changed_section = 0
                    section_id = str(section_id).encode()

                    print('count: {}, freq: {}'.format(count, freq_to_send))

                    if count == 1:
                        flag = DSFlags.begin

                    elif count < freq_to_send:
                        flag = DSFlags.more

                    elif count == freq_to_send:
                        flag = DSFlags.finish

                    else:
                        print("Error have occurred!!!")

                    count += 1

                    reserved_1 = self.null_byte
                    reserved_2 = self.null_byte
                    reserved_3 = self.null_byte
                    section_id = (count - 1)
                    data = data  # verify if the data is already encoded
                    data_size = len(data)
                    checksum = client_pdu.get_checksum(timestamp, data)
                    pdu_array = [message_type, timestamp, error_code, flag, changed_section, section_id, reserved_1,
                                 reserved_2, reserved_3,
                                 data, data_size, checksum]

                    # print(pdu_array)
                    pdu = client_pdu.pack(pdu_array)
                    #############################################
                    # SEND THE DOCUMENT
                    #############################################
                    client_socket.send(pdu)
                    ##################################
                    # set state#
                    ##################################
                    client_state.set_state(DSState.AUTHENTICATED)
                    # print('pdu before send: {}'.format(pdu))

            else:
                client_state.set_state(DSState.CONNECTED)
                print(self.color.red('Client presented wrong credentials'))
                self.connect(client_state, client_pdu, client_socket, client_address, client_error_correction,
                             DSCode.LOGIN_NOT_SUCCESS)
        else:
            message_type = DSMessageType.CAUTH
            timestamp = client_pdu.get_time()  # get timestamp
            error_code = client_error_code
            flag = DSFlags.finish
            changed_section = 0
            section_id = 0
            reserved_1 = self.null_byte
            reserved_2 = self.null_byte
            reserved_3 = self.null_byte
            data = data  # verify if the data is already encoded
            data_size = len(data)
            checksum = client_pdu.get_checksum(timestamp, data)

            pdu_array = [message_type, timestamp, error_code, flag, changed_section, section_id, reserved_1, reserved_2,
                         reserved_3,
                         data, data_size, checksum]

            pdu = client_pdu.pack(pdu_array)
            #############################################
            # SEND THE DOCUMENT
            #############################################
            client_socket.send(pdu)
            ##################################
            # set state#
            ##################################
            client_state.set_state(DSState.AUTHENTICATED)

    def s_edit( self, section_id, client_state, client_pdu, client_socket, client_address, client_error_correction,
                client_error_code=None ):
        authenticated_clients = self.server_log_manager.get_authenticated_clients()
        # print('in s_edit')
        # print('authenticated clients: {}'.format(authenticated_clients))

        # verify if the user is authenticated
        if client_socket in authenticated_clients:
            section_id = int(section_id)
            error_code = ''
            if client_error_code is None:
                error_code = DSCode.SECTION_RETRIEVED

            else:
                error_code = error_code
            # print(self.ds_document.get_document_sections())

            # if the client is currently in possession of a section, don't issue another section
            if client_state.token_issued:
                message_type = b'S_EDIT'
                timestamp = client_pdu.get_time()  # get timestamp

                current_section_owners = self.server_log_manager.get_section_owners()

                if client_address is current_section_owners.get(section_id):
                    data = b'You are the current section owner'
                    error_code = DSCode.CLIENT_IS_THE_CURRENT_SECTION_OWNER  # assign error code
                    section_id = section_id

                else:
                    for key, value in current_section_owners.items():
                        if key == section_id:
                            data = str(value).encode() + b' is the current owner'
                            error_code = DSCode.SECTION_NOT_AVAILABLE  # assign error code
                            section_id = section_id

                        else:
                            data = self.null_byte
                            error_code = DSCode.SECTION_DENIED
                            section_id = 0

                flag = DSFlags.finish
                changed_section = 0

                reserved_1 = self.null_byte
                reserved_2 = self.null_byte
                reserved_3 = self.null_byte

                data_size = len(data)
                checksum = client_pdu.get_checksum(timestamp, data)

                pdu_array = [message_type, timestamp, error_code, flag, changed_section, section_id, reserved_1,
                             reserved_2, reserved_3,
                             data, data_size, checksum]

                pdu = client_pdu.pack(pdu_array)
                ##################################
                # set state#
                ##################################
                client_state.set_state(DSState.AUTHENTICATED)
                self.server_log_manager.log(client_address, DSState.EDITING_DOCUMENT)
                client_socket.send(pdu)
                pass
            else:
                if section_id in self.ds_document.get_document_sections():
                    # print(self.ds_document.get_document_sections())
                    section_data_tuple = self.ds_document.get_document_sections().get(section_id)
                    section_data = section_data_tuple[0]
                    is_free = section_data_tuple[1]

                    # find out if the section the user requested for is free.
                    if is_free:
                        # print(self.ds_document.get_document_sections())
                        self.server_log_manager.add_section_owners(client_address, section_id)
                        self.ds_document.get_document_sections().update(
                            {section_id: (section_data, False)})  # set flag on data
                        # print('the section data : {}'.format(section_data))
                        # print('After dictionary flags')
                        # print(self.ds_document.get_document_sections())

                        message_type = b'S_EDIT'
                        timestamp = client_pdu.get_time()  # get timestamp\
                        flag = DSFlags.finish
                        changed_section = 0
                        section_id = section_id

                        reserved_1 = self.null_byte
                        reserved_2 = self.null_byte
                        reserved_3 = self.null_byte

                        data = section_data
                        data_size = len(data)
                        checksum = client_pdu.get_checksum(timestamp, data)

                        pdu_array = [message_type, timestamp, error_code, flag, changed_section, section_id, reserved_1,
                                     reserved_2, reserved_3,
                                     data, data_size, checksum]

                        pdu = client_pdu.pack(pdu_array)
                        ##################################
                        # set state#
                        ##################################
                        client_state.set_state(DSState.EDITING_DOCUMENT)
                        client_state.token_issued = True
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
                        if client_address is current_section_owners.get(section_id):
                            data = b'You are the current section owner'
                            error_code = DSCode.CLIENT_IS_THE_CURRENT_SECTION_OWNER  # assign error code

                        else:
                            for key, value in current_section_owners.items():
                                if key == section_id:
                                    data = str(value).encode() + b' is the current owner'
                                    error_code = DSCode.SECTION_NOT_AVAILABLE  # assign error code

                        message_type = b'S_EDIT'
                        timestamp = client_pdu.get_time()  # get timestamp\
                        flag = DSFlags.finish
                        changed_section = 0
                        section_id = 0

                        reserved_1 = self.null_byte
                        reserved_2 = self.null_byte
                        reserved_3 = self.null_byte

                        data_size = len(data)
                        checksum = client_pdu.get_checksum(timestamp, data)

                        pdu_array = [message_type, timestamp, error_code, flag, changed_section, section_id, reserved_1,
                                     reserved_2, reserved_3,
                                     data, data_size, checksum]

                        pdu = client_pdu.pack(pdu_array)
                        # print(data)
                        ##################################
                        # set state#
                        ##################################
                        client_state.set_state(DSState.BLOCKED)
                        #############################################
                        # SEND THE DOCUMENT
                        #############################################
                        client_socket.send(pdu)
                        # print(pdu)
                        issued_token = False
                        token_id = None
                        return issued_token, token_id

                        # if the section id presented by the client is invalid or they don't possess a token for it
                else:
                    error_code = DSCode.SECTION_ID_NOT_VALID
                    message_type = b'S_EDIT'
                    timestamp = client_pdu.get_time()  # get timestamp\
                    flag = DSFlags.finish
                    changed_section = 0
                    section_id = 0

                    reserved_1 = self.null_byte
                    reserved_2 = self.null_byte
                    reserved_3 = self.null_byte
                    data = b'invalid section id was presented'

                    data_size = len(data)
                    checksum = client_pdu.get_checksum(timestamp, data)

                    pdu_array = [message_type, timestamp, error_code, flag, changed_section, section_id, reserved_1,
                                 reserved_2, reserved_3,
                                 data, data_size, checksum]

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
                    issued_token = False
                    token_id = None
                    return issued_token, token_id

        # if the user is not authenticated
        else:
            self.connect(client_state, client_pdu, client_socket, client_address, client_error_correction,
                         DSCode.USER_NOT_AUTHENTICATED)

    def s_commit( self, section_id, data, client_state, client_pdu, client_socket, client_address,
                  client_error_correction,
                  client_error_code=None ):

        print('in commit, section')

        section_id = int(section_id)
        print('authenticated clients: {}'.format(self.server_log_manager.get_authenticated_clients()))
        print('section owners: {}'.format(self.server_log_manager.get_section_owners().values()))
        print(self.server_log_manager.get_section_owners())
        # we have to verify if the client have token for the section to which they are committing

        # if the client exists in the list of authenticated clients and the client possesses the token for the section

        if client_socket in self.server_log_manager.authenticated_clients and client_address in self.server_log_manager.get_section_owners().values():
            # print(self.color.yellow('client possess a token for this commit'))
            print('client address: {} section id: {}'.format(client_address, section_id))
            print('client currently with  the section token : ', end='')
            print(self.server_log_manager.get_section_owners().get(section_id))

            # we send only when the flag is now finish

            if client_address == self.server_log_manager.get_section_owners().get(int(section_id)):
                # print('data: {}'.format(data))
                self.ds_document.update_document(section_id, data)
                ##################################
                # set state#
                ##################################
                client_state.set_state(DSState.COMMITTING_CHANGES)
                self.server_log_manager.log(client_address, client_state.get_current_state())
                client_state.token_issued = False
                #############################################
                print('authenticated clients: {}'.format(self.server_log_manager.authenticated_clients))

                for auth_client_socket in self.server_log_manager.authenticated_clients:
                    # send the update to the authenticated clients, but first inform them that an update is coming

                    message_type = DSMessageType.CAUTH
                    timestamp = client_pdu.get_time()  # get timestamp
                    error_code = DSCode.COMMIT_UPDATE
                    flag = DSFlags.finish
                    changed_section = 0
                    section_id = section_id
                    reserved_1 = self.null_byte
                    reserved_2 = self.null_byte
                    reserved_3 = self.null_byte

                    data = self.null_byte
                    data_size = len(data)
                    checksum = client_pdu.get_checksum(timestamp, data)

                    pdu_array = [message_type, timestamp, error_code, flag, changed_section, section_id, reserved_1,
                                 reserved_2, reserved_3,
                                 data, data_size, checksum]

                    pdu = client_pdu.pack(pdu_array)
                    print('forwarding updates to : {}'.format(auth_client_socket))
                    auth_client_socket.send(pdu)
                    self.server_log_manager.add_authenticated_client_connection(client_socket, client_address)

                    # Now send the document.txt to the client
                    data_string = self.ds_document.get_document_as_string()  # get the entire document.txt as string
                    data_break_down = self.ds_document.break_data(data_string)

                    freq_to_send = len(data_break_down)
                    count = 0

                    previous_data_sent_to_client = client_state.received_document

                    for new_item, old_item in zip(data_break_down, previous_data_sent_to_client.values()): # we need to make provision for when

                        count += 1
                        message_type = DSMessageType.CAUTH
                        timestamp = client_pdu.get_time()  # get timestamp
                        error_code = DSCode.COMMIT_UPDATE  # assign error code

                        if count == freq_to_send:
                            flag = DSFlags.finish
                        else:
                            flag = DSFlags.more

                        if new_item == old_item[0]:
                            changed_section = 0
                        else:
                            print('----------------------------------')
                            print('new item: {}'.format(new_item))
                            print('old_item: {}'.format(old_item[0]))
                            print('----------------------------------')
                            changed_section = 1

                        reserved_1 = self.null_byte
                        reserved_2 = self.null_byte
                        reserved_3 = self.null_byte
                        section_id = count - 1
                        data = new_item
                        data_size = len(data)
                        checksum = client_pdu.get_checksum(timestamp, data)
                        pdu_array = [message_type, timestamp, error_code, flag, changed_section, section_id, reserved_1,
                                     reserved_2, reserved_3,
                                     data, data_size, checksum]
                        pdu = client_pdu.pack(pdu_array)

                        client_state.set_state(DSState.COMMITTING_CHANGES)

                        # SEND THE DOCUMENT
                        #############################################
                        client_socket.send(pdu)

                    self.server_log_manager.document_sent_to_client.update(
                        {client_address: dict(self.ds_document.document_as_dic)})
                    client_state.set_as_previous_document(self.ds_document.document_as_dic)
            else:
                print('client presented an invalid commit id')
                self.s_edit(section_id, client_state, client_pdu, client_socket, client_address,
                            DSCode.SECTION_ID_NOT_VALID)

        # if the client exist in the authenticated client list but the client doesn't possess the token for the section which they are requesting
        elif client_socket in self.server_log_manager.get_authenticated_clients() and client_address not in self.server_log_manager.get_section_owners().values():
            #
            # print(self.color.red('testing'))
            # print('testing for the keys')
            # x = [value for value in self.server_log_manager.get_section_owners().values()]
            # print(x)
            # print('testing for keys end')
            # print('client_address: ' + str(client_address))
            # print(self.server_log_manager.get_section_owners().keys())
            # print(self.server_log_manager.get_section_owners())
            # print(self.server_log_manager.get_authenticated_clients())
            print('if the client exist in the authenticated client list but the client doesn\'t possess the token for the section which they are requesting')
            data = self.null_byte
            self.cauth(data, client_state, client_pdu, client_socket, client_address, client_error_correction,
                       DSCode.SECTION_DENIED)

        # if the client is neither authenticated nor authorized
        else:
            print('client is neither authenticated nor authorized')
            self.connect(client_state, client_pdu, client_socket, client_address, client_error_correction,
                         DSCode.USER_NOT_AUTHENTICATED)

    @staticmethod
    def close( client_pdu, client_state, client_socket, client_address ):
        client_state.is_alive = False
        client_socket.close()
        client_state.set_state(DSState.CLOSE)

    def release( self, section_id, client_pdu, client_state, client_socket, client_address ):
        # first, before, the client requests for a section to be released, we need to verify if the client have the
        # token for the section

        # set the non-changing parameters
        message_type = DSMessageType.S_RELEASE
        timestamp = client_pdu.get_time()  # get timestamp
        flag = DSFlags.finish
        changed_section = 0
        reserved_1 = self.null_byte
        reserved_2 = self.null_byte
        reserved_3 = self.null_byte
        section_id = int(section_id)

        data = self.null_byte
        data_size = len(data)

        checksum = client_pdu.get_checksum(timestamp, data)

        # set a placeholder for the changing parameters
        error_code = ''

        # if the client is authenticated and the client have any section token
        if client_socket in self.server_log_manager.authenticated_clients and client_address == self.server_log_manager.get_section_owners().get(
                int(section_id)):
            client_state.set_state(DSState.RELEASE)
            self.server_log_manager.log(client_address, client_state.get_current_state())
            successful = self.ds_document.release(section_id)
            print('outcome of the release: {}'.format(successful))

            if successful:
                error_code = DSCode.RELEASE_SECTION_SUCCESSFUL
                self.server_log_manager.update_section_owners(client_address, section_id)
                client_state.token_issued = False

            else:
                error_code = DSCode.RELEASE_SECTION_NOT_SUCCESSFUL

        else:  # if client is authenticated, but they don't have a token for the session
            if client_socket in self.server_log_manager.authenticated_clients:
                section_id = int(section_id)

                # if the section requested to be released by the client is free
                if section_id in self.ds_document.get_document_sections():
                    print(self.ds_document.get_document_sections())
                    section_data_tuple = self.ds_document.get_document_sections().get(section_id)
                    section_data = section_data_tuple[0]
                    is_free = section_data_tuple[1]

                    # find out if the section the user requested for is free.
                    if is_free:
                        error_code = DSCode.SECTION_TOKEN_NOT_FOUND_SECTION_IS_FREE

                    else:
                        # if the section is not free
                        error_code = DSCode.RELEASE_SECTION_NOT_SUCCESSFUL

                else:
                    # if the section requested by the client doesn't exist, we have to deny the request
                    error_code = DSCode.SECTION_ID_NOT_VALID

                    pass

        print('section owners: {}'.format(self.server_log_manager.get_section_owners()))

        section_id = int(section_id)
        pdu_array = [message_type, timestamp, error_code, flag, changed_section, section_id, reserved_1,
                     reserved_2, reserved_3,
                     data, data_size, checksum]
        #
        # for item in pdu_array:
        #     print('{} : type: {}'.format(item, type(item)))

        pdu = client_pdu.pack(pdu_array)
        # print(data)
        ##################################
        # set state#
        ##################################
        client_state.set_state(DSState.AUTHENTICATED)
        self.server_log_manager.log(client_address, client_state.get_current_state())
        #############################################
        # SEND THE DOCUMENT
        #############################################
        client_socket.send(pdu)

    @staticmethod
    def get_time():
        return str(datetime.now()).encode('utf-8')

    @staticmethod
    def get_checksum( timestamp, data ):
        try:
            return binascii.crc32(timestamp + data)
        except TypeError as err:
            print('This value {} is not a byte'.format(data))

    @staticmethod
    def remove_space( array ):
        new_array = []
        for item in array:
            new_array.append(item.strip())

        return new_array

    def response( self, request, error_code, data ):
        """
        This is used to break server response to be sent into chucks of pdu
        ie if data = 'Access denied'
        the output is similar to [[b'S_DATA', 3434343, b'timestamp, b'Access ], [b'S_DATA', 36674545, b'timestamp, b'Denied']]
        :param error_code:
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

    def response_document( self, request, error_code, data_array ):
        """
        Used for sending documents only
        :param request:
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
        os._exit(1)

    finally:
        os._exit(1)
