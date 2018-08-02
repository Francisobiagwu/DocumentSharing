#!/usr/bin/env python

"""
@author: Francis Obiagwu
@software: SecureDocumentSharing
@file: DSClientServerResponseProcessor.py
@time: 6/6/18 7:16 PM
"""

from DSCodes import DSCode
from DSFlags import DSFlags
from DSMessageType import DSMessageType
from DSPdu import DSPdu
from DSPrintStyle import Color, Style


class DSClientServerResponseProcessor:
    """
    This class in charge of processing server replies
    """


    is_logged_in = False

    def __init__( self ):
        self.message_type = ''
        self.timestamp = ''
        self.error_code = ''
        self.flag = ''
        self.changed_section = ''
        self.section_id = ''
        self.reserved_1 = ''
        self.reserved_2 = ''
        self.reserved_3 = ''

        self.data = ''
        self.data_size = ''
        self.checksum = ''

        self.response = ''
        self.count = 0
        self.null_byte = b'\x00'
        self.server_processor_pdu = DSPdu()
        self.client_socket = ''
        self.message_type_index, self.timestamp_index, self.error_code_index, self.flag_index, self.changed_section_index, self.section_id_index, self.reserved_1_index, self.reserved_2_index, self.reserved_3_index, self.data_index,self.data_size_index,  self.checksum_index = self.server_processor_pdu.get_pdu_parts_index()

        self.color = Color()
        self.style = Style()
        self.error = DSCode()
        self.is_commit_message = False

    def process_response( self, response, client_socket, client_obj ):
        """
        This is the main response processor
        :param client_obj:
        :param response: pdu array
        :param client_socket: client's socket object
        :return:
        """

        # assign various pdu parts from the response parameter
        self.response = response
        self.client_socket = client_socket
        self.message_type = self.response[self.message_type_index]
        self.timestamp = self.response[self.timestamp_index]
        self.error_code = self.response[self.error_code_index]
        self.flag = self.response[self.flag_index]
        self.changed_section = self.response[self.changed_section_index]
        self.section_id = self.response[self.section_id_index]
        self.reserved_1 = self.response[self.reserved_1_index]
        self.reserved_2 = self.response[self.reserved_2_index]
        self.reserved_3 = self.response[self.reserved_3_index]

        self.data = self.response[self.data_index]
        self.data_size = self.response[self.data_size_index]
        self.checksum = self.response[self.checksum_index]
        self.client_socket = client_socket

        if client_obj.is_authenticated is False and self.error_code == DSCode.LOGIN_SUCCESS and self.flag == DSFlags.begin:
            # we only need to print this once.
            print(self.color.red(self.error.dscode_print(self.error_code)))
            client_obj.is_authenticated = True

        elif client_obj.is_authenticated is True and self.error_code != DSCode.LOGIN_SUCCESS:
            print(self.color.red('checking this out'))
            print(self.error_code)
            print(self.color.red(self.error.dscode_print(self.error_code)))

        elif self.error_code == DSCode.LOGIN_NOT_SUCCESS:
            client_obj.is_authenticated = False
            print(self.color.red(self.error.dscode_print(self.error_code)))

        elif self.error_code == DSCode.RELEASE_SECTION_SUCCESSFUL:
            print(self.color.green(self.error.dscode_print(self.error_code)))

        elif self.error_code == DSCode.SECTION_DENIED:
            print(self.color.red(self.error.dscode_print(self.error_code)))

        elif self.error_code == DSCode.USER_NOT_AUTHENTICATED:
            print(self.color.red(self.error.dscode_print(self.error_code)))

        elif self.error_code == DSCode.CONNECTED:
            pass
            # print('{:^70}'.format(color.yellow(error.dscode_print(self.error_code))))
            # print()

        elif self.error_code == DSCode.LOGIN_SUCCESS and self.flag.encode() == DSFlags.begin:
            print(self.color.green(self.error.dscode_print(self.error_code)))
            pass

        elif self.error_code == DSCode.LOGIN_SUCCESS and self.flag.encode() == DSFlags.more:
            pass

        elif self.error_code == DSCode.LOGIN_SUCCESS and self.flag.encode() == DSFlags.finish:
            pass

        elif self.error_code == DSCode.COMMIT_UPDATE:
            pass

        elif self.error_code == DSCode.COMMIT_DENIED:
            print(self.color.red(self.error.dscode_print(self.error_code)))

        else:
            print(self.color.green(self.error.dscode_print(self.error_code)))

        if self.response[self.message_type_index] == DSMessageType.CONNECT.decode():
            self.connect()
            return True

        elif self.response[self.message_type_index] == DSMessageType.CAUTH.decode():
            self.cauth()
            return True

        elif self.response[self.message_type_index] == DSMessageType.S_EDIT.decode():
            self.s_edit()
            return True

        elif self.response[self.message_type_index] == DSMessageType.S_RELEASE.decode():
            self.s_release()
            return True

        elif self.response[self.message_type_index] == DSMessageType.LOGOFF.decode():
            self.abort()
            return True

        elif self.response[self.message_type_index] == DSMessageType.S_COMMIT.decode():
            self.commit()
            return True
        else:
            return False

    def connect( self ):
        message_type = DSMessageType.CONNECT
        timestamp = self.server_processor_pdu.get_time()  # get timestamp
        error_code = DSCode.OK  # assign error code
        flag = DSFlags.finish
        changed_section = 0
        section_id = 0
        reserved_1 = self.null_byte
        reserved_2 = self.null_byte
        reserved_3 = self.null_byte
        data = b'HELLO SERVER'
        data_size = len(data)
        checksum = self.server_processor_pdu.get_checksum(timestamp, data)

        pdu_array = [message_type, timestamp, error_code, flag, changed_section, section_id, reserved_1, reserved_2, reserved_3,
                     data, data_size,checksum]
        pdu = self.server_processor_pdu.pack(pdu_array)

        self.client_socket.send(pdu)
        print(self.color.green('{:^60}'.format('--Welcome to Document Sharing Software 1.0--')))
        print('------------------------COMMANDS----------------------------\n'
              'LOGIN: LOGIN, USERNAME, PASSWORD, DOCUMENT_NAME             |\n'
              'CREATE NEW DOCUMENT: CREATE, DOCUMENT_NAME                  |\n'
              'REQUEST SECTION: SECTION, SECTION_ID,                       |\n'
              'COMMIT: COMMIT, SECTION_ID, DATA                            |\n'
              'LOGOFF: LOGOFF                                              |\n'
              '------------------------------------------------------------\n')

        return 0

    def cauth( self ):

        if self.flag == DSFlags.begin.decode() and self.error_code == DSCode.COMMIT_UPDATE:
            print(self.color.yellow(self.error.dscode_print(self.error_code)))

        if self.flag == DSFlags.begin.decode() or self.flag == DSFlags.more.decode():
            if self.changed_section == 1:
                print('{}: {}'.format(self.color.yellow(str(self.count)), self.color.yellow(self.data)))

            else:
                print('{}: {}'.format(str(self.count), self.data))

            self.count += 1

        elif self.flag == DSFlags.finish.decode():
            if '\n' == self.data.strip():
                pass

            elif self.count >= 1 and len(self.data.strip()) > 1:
                if self.changed_section == 1:
                    print('{}: {}'.format(self.color.yellow(str(self.count)), self.color.yellow(self.data)))

                else:
                    print('{}: {}'.format(self.count, self.data))

            else:
                print(self.data)

            self.count = 0  # reset the count

    def s_edit( self ):
        if self.error_code == DSCode.CLIENT_IS_THE_CURRENT_SECTION_OWNER:
            print('client is the current owner of the section id: {}'.format(self.section_id))

        elif self.error_code == DSCode.SECTION_NOT_AVAILABLE:
            print(self.data)

        elif self.error_code == DSCode.SECTION_DENIED:
            print(self.data)

        elif self.error_code == DSCode.SECTION_ID_NOT_VALID:
            print(self.data)

        else:
            print('{}: {} '.format(self.section_id, self.data))


    def s_revoke( self ):
        print('Permission revoked for section #{}'.format(self.section_id))
        print(self.error_code)
        print(self.data)

    def s_release( self ):
        # if self.error_code == DSCode.RELEASE_SECTION_NOT_SUCCESSFUL:
        #     print('section #{} not released'.format(self.section_id))
        #
        # elif self.error_code == DSCode.SECTION_ID_NOT_VALID:
        #     print('client presented an invalid section id')
        #
        # elif self.error_code == DSCode.CLIENT_IS_THE_CURRENT_SECTION_OWNER:
        #     print('client is not the current section owner for section id: {}'.format(self.section_id))
        #
        # elif self.error_code == DSCode.SECTION_TOKEN_NOT_FOUND_SECTION_IS_FREE:
        #     print('client is not the current section owner, however, the section id #{} is free'.format(self.section_id))
        #
        # elif self.error_code == DSCode.RELEASE_SECTION_SUCCESSFUL:
        #     print('Section #{} successfully released'.format(self.section_id))
        pass

    def s_denied( self ):
        print('Section #{} request was denied'.format(self.section_id))
        print(self.error_code)
        print(self.data)

    def abort( self ):
        print('The server have successfully disconnected')
        print(self.error_code)
        print(self.data)

    def commit( self ):
        # the server is not meant to respond with this messagetype since once the client is done updating a section
        # server is supposed to move the state back to S_DATA
        pass

