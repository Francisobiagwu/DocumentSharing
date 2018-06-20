"""
@author: Francis Obiagwu
@software: SecureDocumentSharing
@file: SDSTimer.py
@time: 6/9/18 5:56 PM
"""

import time


class SDSTimer:
    count_down = 5  # seconds
    inactivity = 30  # seconds
    timer_finished = False

    def __int__(self, caller_countdown=count_down):  # use default if the caller didn't specify
        self.count_down = caller_countdown

    def start_timer(self, delay=count_down):
        self.count_down = delay
        while self.count_down:  # will stop once the count_down reaches 0
            print('Timer: {}'.format(self.count_down))
            time.sleep(1)
            self.count_down -= 1

        self.timer_finished = True

    def check_inactivity(self):
        while self.inactivity:
            print('Inactivity: {}'.format(self.inactivity))
