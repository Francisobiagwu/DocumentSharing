#!/usr/bin/env python

__author__ = "Francis Obiagwu"
__copyright__ = "Copyright 2018"
__version__ = "1.0"

from DSMessageType import DSMessageType
from DSPdu import DSPdu
from DSFlags import DSFlags
from DSCodes import DSCode


class DSServerResponseProcessor:
    def __init__( self ):
        self.message_type = ''
        self.timestamp = ''
        self.error_code = ''
        self.flag = ''
        self.reserved_1 = ''
        self.reserved_2 = ''
        self.section_id = ''
        self.data = ''
        self.checksum = ''

        self.response = ''
        self.count = 0
        self.null_byte = b'\x00'
        self.server_processor_pdu = DSPdu()
        self.client_socket = ''
        self.message_type_index, self.timestamp_index, self.error_code_index, self.flag_index, self.reserved_1_index, self.reserved_2_index, self.section_id_index, self.data_index, self.checksum_index = self.server_processor_pdu.get_pdu_parts_index()

    def process_response( self, response, client_socket ):
        """
        :param array response:
        :return:
        """
        self.response = response
        self.client_socket = client_socket
        self.message_type = self.response[self.message_type_index]
        self.timestamp = self.response[self.timestamp_index]
        self.error_code = self.response[self.error_code_index]
        self.flag = self.response[self.flag_index]
        self.reserved_1 = self.response[self.reserved_1_index]
        self.reserved_2 = self.response[self.reserved_2_index]
        self.section_id = self.response[self.section_id_index]
        self.data = self.response[self.data_index]
        self.checksum = self.response[self.checksum_index]
        self.client_socket = client_socket

        if self.response[self.message_type_index] == DSMessageType.CONNECT.decode():
            self.connect()
            return True

        elif self.response[self.message_type_index] == DSMessageType.CAUTH.decode():
            self.cauth()
            return True

        elif self.response[self.message_type_index] == DSMessageType.S_EDIT.decode():
            self.s_data()
            return True

        elif self.response[self.message_type_index] == DSMessageType.S_RELEASE.decode():
            self.s_release()
            return True


        elif self.response[self.message_type_index] == DSMessageType.CLOSE.decode():
            self.abort()
            return True

        elif self.response[self.message_type_index] == DSMessageType.S_COMMIT.decode():
            self.commit()
            return True
        else:
            return False

    def connect( self ):
        print('Connected to the server')
        # print(self.error_code)
        # print(self.data)
        message_type = DSMessageType.CONNECT
        timestamp = self.server_processor_pdu.get_time()  # get timestamp
        error_code = DSCode.OK  # assign error code
        flag = DSFlags.finish
        reserved_1 = self.null_byte
        reserved_2 = self.null_byte
        section_id = self.null_byte
        data = b'HELLO'
        checksum = self.server_processor_pdu.get_checksum(timestamp, data)
        pdu_array = [message_type, timestamp, error_code, flag, reserved_1, reserved_2, section_id, data, checksum]
        pdu = self.server_processor_pdu.pack(pdu_array)

        self.client_socket.send(pdu)
        print('------------------------COMMANDS----------------------------\n'
              'LOGIN: LOGIN, USERNAME, PASSWORD, DOCUMENT_NAME             |\n'
              'REQUEST SECTION: SECTION, SECTION_ID,                       |\n'
              'COMMIT: COMMIT, SECTION_ID, DATA                            |\n'
              'LOGOFF: LOGOFF                                              |\n'
              '------------------------------------------------------------\n')

        return 0

    def cauth( self ):
        # print(self.error_code)
        if self.flag == DSFlags.more.decode():
            print('{}: {}'.format(self.count, self.data))
            self.count += 1

        else:
            print(self.data)

    def s_data( self ):
        # print('section #{} successfully retrieved'.format(self.section_id))
        if self.flag == DSFlags.more.decode():
            print('{}: {}'.format(self.count, self.data))
            self.count += 1

        else:
            print(self.data)

        self.count = 0

    def s_revoke( self ):
        print('Permission revoked for section #{}'.format(self.section_id))
        print(self.error_code)
        print(self.data)

    def s_release( self ):
        print('Section #{} successfully released'.format(self.section_id))
        print(self.error_code)
        print(self.data)

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
