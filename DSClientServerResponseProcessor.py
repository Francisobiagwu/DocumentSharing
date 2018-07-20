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

    global color
    global style
    global error
    color = Color()
    style = Style()
    error = DSCode()
    is_logged_in = False

    def __init__(self):
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

        self.color = Color()
        self.style = Style()
        self.error = DSCode()

    def process_response(self, response, client_socket, client_obj):
        """
        This is the main response processor
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
        self.reserved_1 = self.response[self.reserved_1_index]
        self.reserved_2 = self.response[self.reserved_2_index]
        self.section_id = self.response[self.section_id_index]
        self.data = self.response[self.data_index]
        self.checksum = self.response[self.checksum_index]
        self.client_socket = client_socket

        if client_obj.is_authenticated is False and self.error_code == DSCode.LOGIN_SUCCESS and self.flag == DSFlags.begin:
            # we only need to print this once.
            print('1')
            print(color.red(error.dscode_print(self.error_code)))
            client_obj.is_authenticated = True

        elif client_obj.is_authenticated is True and self.error_code != DSCode.LOGIN_SUCCESS:
            print('2')
            print(color.red('checking this out'))
            print(self.error_code)
            print(color.red(error.dscode_print(self.error_code)))

        elif self.error_code == DSCode.LOGIN_NOT_SUCCESS:
            print('3')
            client_obj.is_authenticated = False
            print(color.red(error.dscode_print(self.error_code)))

        elif self.error_code == DSCode.SECTION_DENIED:
            print('4')
            print(color.red(error.dscode_print(self.error_code)))


        elif self.error_code == DSCode.USER_NOT_AUTHENTICATED:
            print('5')
            print(color.red(error.dscode_print(self.error_code)))

        elif self.error_code == DSCode.CONNECTED:
            print('6')
            print('{:^30}'.format(color.yellow(error.dscode_print(self.error_code))))

        elif self.error_code == DSCode.LOGIN_SUCCESS and self.flag.encode() == DSFlags.begin:
            print('7')
            print(color.green(error.dscode_print(self.error_code)))
            pass

        elif self.error_code == DSCode.LOGIN_SUCCESS and self.flag.encode() == DSFlags.more:
            pass

        elif self.error_code == DSCode.LOGIN_SUCCESS and self.flag.encode() == DSFlags.finish:
            pass

        else:
            print(color.green(error.dscode_print(self.error_code)))




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

    def connect(self):

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
        print(color.green('{:^60}'.format('--Welcome to Document Sharing Software 1.0--')))
        print('------------------------COMMANDS----------------------------\n'
              'LOGIN: LOGIN, USERNAME, PASSWORD, DOCUMENT_NAME             |\n'
              'CREATE NEW DOCUMENT: CREATE, DOCUMENT_NAME                  |\n'
              'REQUEST SECTION: SECTION, SECTION_ID,                       |\n'
              'COMMIT: COMMIT, SECTION_ID, DATA                            |\n'
              'LOGOFF: LOGOFF                                              |\n'
              '------------------------------------------------------------\n')

        return 0

    def cauth(self):
        if self.flag == DSFlags.begin.decode() or self.flag == DSFlags.more.decode():
            print('{}: {}'.format(self.count, self.data))
            self.count += 1

        else:
            print(self.data)

    def s_data(self):
        # print('section #{} successfully retrieved'.format(self.section_id))
        if self.flag == DSFlags.more.decode():
            print('{}: {}'.format(self.count, self.data))
            self.count += 1

        else:
            print(self.data)

        self.count = 0

    def s_revoke(self):
        print('Permission revoked for section #{}'.format(self.section_id))
        print(self.error_code)
        print(self.data)

    def s_release(self):
        print('Section #{} successfully released'.format(self.section_id))
        print(self.error_code)
        print(self.data)

    def s_denied(self):
        print('Section #{} request was denied'.format(self.section_id))
        print(self.error_code)
        print(self.data)

    def abort(self):
        print('The server have successfully disconnected')
        print(self.error_code)
        print(self.data)

    def commit(self):
        # the server is not meant to respond with this messagetype since once the client is done updating a section
        # server is supposed to move the state back to S_DATA
        pass

    def send_ack(self):
        message_type = DSMessageType.ACK
        timestamp = self.server_processor_pdu.get_time()  # get timestamp
        error_code = DSCode.OK  # assign error code
        flag = DSFlags.finish
        reserved_1 = self.null_byte
        reserved_2 = self.null_byte
        section_id = self.null_byte
        data = str(
            self.checksum).encode()  # we are sending the checksum as data, since the server will use this to verify if the
        # client received the message without any tampering
        checksum = self.server_processor_pdu.get_checksum(timestamp, data)
        pdu_array = [message_type, timestamp, error_code, flag, reserved_1, reserved_2, section_id, data, checksum]
        pdu = self.server_processor_pdu.pack(pdu_array)
        self.client_socket.send(pdu)
