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


class DSTimer:

    def __init__(self, client_socket, client_pdu_obj,
                 client_error_correction_obj):  # use default if the caller didn't specify
        self.count_down = 5
        self.inactivity = 30  # seconds
        self.timer_finished = False
        self.is_ACK_received = False
        self.error_correction_obj = client_error_correction_obj
        self.client_socket = client_socket
        self.client_pdu_obj = client_pdu_obj

    def start_timer(self):
        # will stop once the count_down reaches 0 or when an ACK is received
        print('in start timer')
        # print('countdown {} is_ack_received: {}'.format(self.count_down, self.is_ACK_received))
        # print(self.count_down, self.is_ACK_received)
        while self.count_down and not self.is_ACK_received:
            if self.count_down == 0:
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

                pdu = self.client_pdu.pack(pdu_array)
                self.client_socket.send(pdu)
                self.server_log_manager.add_authenticated_client_connection(self.client_socket, self.client_address)

                # Now send the document.txt to the client
                data_string = self.ds_document.get_document_as_string()  # get the entire document.txt as string
                data_break_down = self.ds_document.break_data(data_string)

                freq_to_send = len(data_break_down)

                pass

            else:
                print(self.is_ACK_received)
                print('Timer: {}'.format(self.count_down))
                time.sleep(1)
                self.count_down -= 1

        self.timer_finished = True

    def check_inactivity(self):
        while self.inactivity:
            print('Inactivity: {}'.format(self.inactivity))
