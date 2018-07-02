"""
@author: Francis Obiagwu
@software: SecureDocumentSharing
@file: DSTimer.py
@time: 6/9/18 5:56 PM
"""

import time

from DSCodes import DSCode
from DSFlags import DSFlags
from DSMessageType import DSMessageType
from DSServerLogManagement import DSServerLogManagement


class DSTimer:

    def __init__(self, client_socket, client_address, client_pdu_obj,
                 client_error_correction_obj):  # use default if the caller didn't specify
        self.count_down = 5
        self.inactivity = 30  # seconds
        self.timer_finished = False
        self.is_ACK_received = False
        self.error_correction_obj = client_error_correction_obj
        self.client_socket = client_socket
        self.client_pdu_obj = client_pdu_obj
        self.client_address = client_address
        self.null_byte = b'\x00'
        self.server_logger = DSServerLogManagement()

    def start_timer(self, message_type):
        # will stop once the count_down reaches 0 or when an ACK is received
        print('in start timer')
        # print('countdown {} is_ack_received: {}'.format(self.count_down, self.is_ACK_received))
        # print(self.count_down, self.is_ACK_received)
        while self.count_down and not self.is_ACK_received:
            print(self.is_ACK_received)
            print('Timer: {}'.format(self.count_down))
            time.sleep(1)
            self.count_down -= 1

        if self.count_down == 0 and not self.is_ACK_received:  # if the timer stops and the ACK is not received
            recently_sent_data = self.error_correction_obj.sent_data
            # resend the data to the client
            # so I need client_socket, and I will need to call the pdu class in order to do this
            timestamp = self.client_pdu_obj.get_time()  # get timestamp
            reserved_1 = self.null_byte
            reserved_2 = self.null_byte
            ACK_data = self.null_byte
            checksum = self.client_pdu_obj.get_checksum(timestamp, ACK_data)
            pdu_array = [DSMessageType.CAUTH, timestamp, DSCode.LOGIN_SUCCESS, DSFlags.finish, reserved_1,
                         reserved_2,
                         self.null_byte, ACK_data, checksum]

            pdu = self.client_pdu_obj.pack(pdu_array)
            self.client_socket.send(pdu)
            self.server_logger.add_authenticated_client_connection(self.client_socket, self.client_address)

            # Now send the document.txt to the client
            self.client_socket.send(recently_sent_data)
            pass

        self.timer_finished = True

    def check_inactivity(self):
        while self.inactivity:
            print('Inactivity: {}'.format(self.inactivity))
