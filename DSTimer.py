"""
@author: Francis Obiagwu
@software: SecureDocumentSharing
@file: DSTimer.py
@time: 6/9/18 5:56 PM
"""

import time


class DSTimer:
    count_down = 5  # seconds

    def __init__( self, caller_countdown=count_down ):  # use default if the caller didn't specify
        self.count_down = caller_countdown
        self.inactivity = 30  # seconds
        self.timer_finished = False
        self.is_ACK_received = False

    def start_timer( self, delay=count_down ):
        self.count_down = delay
        # will stop once the count_down reaches 0 or when an ACK is received
        print('in start timer')
        # print('countdown {} is_ack_received: {}'.format(self.count_down, self.is_ACK_received))
        # print(self.count_down, self.is_ACK_received)
        while self.count_down and not self.is_ACK_received:
            print(self.is_ACK_received)
            print('Timer: {}'.format(self.count_down))
            time.sleep(1)
            self.count_down -= 1

        self.timer_finished = True

    def check_inactivity( self ):
        while self.inactivity:
            print('Inactivity: {}'.format(self.inactivity))




