#!/usr/bin/env python

"""
@author: Francis Obiagwu
@software: SecureDocumentSharing
@file: DSInput.py
@time: 6/6/18 7:16 PM
"""

import math

from DSCodes import DSCode
from DSFlags import DSFlags
from DSMessageType import DSMessageType
from DSPdu import DSPdu


class DSInput:
    def __init__(self):
        self.user_input = ''
        self.isValid = False
        self.ds_pdu = DSPdu()
        self.ds_code = DSCode()
        self.null_byte = b'\x00'
        self.data = ''
        self.array = ''

    def get_user_input(self):
        """
        Gets user input and then formats then return them as string arrays
        :return: list
        """
        # if the didn't enter any value continue to prompt until a value is entered

        while True:
            self.user_input = input()
            array = self.get_array(self.user_input)
            if array[0] == 'LOGIN' and len(array) == 4:
                # reset self.user_input to ''

                self.reset_user_input()
                return array, ','.join(array)
            elif array[0] == 'SECTION' and len(array) == 2:
                try:
                    int(array[1])
                    self.reset_user_input()
                    return array, ','.join(array)
                except ValueError as err:
                    print(err.args)
                    print('User input is not valid')
                    continue

            elif array[0] == 'COMMIT':
                try:
                    int(array[1])
                    self.reset_user_input()
                    return array, ','.join(array)
                except ValueError as err:
                    print(err.args)
                    print('User input is not valid')
                    continue

            elif array[0] == 'LOGOFF' and len(array) == 1:
                self.reset_user_input()
                return array, ','.join(array)

            elif array[0] == 'RELEASE' and len(array) == 2:
                self.reset_user_input()
                return array, ','.join(array)

            else:
                print('User input is not valid', array, len(array))

    def get_array(self, user_input):
        """
        Gets returns an array of the user_input
        :param string user_input:
        :return: list
        """

        self.user_input = user_input.split(',')
        array = []
        for item in self.user_input:
            array.append(item.strip())

        # reset self.user_input to ''
        self.reset_user_input()
        return array

    def reset_user_input(self):
        self.user_input = ''

    def process_user_input(self, array, data):
        """
        Process user input and return the array for packing
        :param list array:
        :param string data:
        :return: array
        """
        # print(array, data)
        self.data = data
        self.array = array

        if array[0] == 'LOGIN':
            return self.login()

        elif array[0] == 'SECTION':
            return self.section()

        elif array[0] == 'RELEASE':
            return self.release()

        elif array[0] == 'COMMIT':
            return self.commit()

        elif array[0] == 'LOGOFF':
            return self.logoff()

        else:
            print('User input not valid')

    def login(self):
        message_type = DSMessageType.CAUTH
        timestamp = self.ds_pdu.get_time()  # get timestamp
        error_code = self.ds_code.OK  # assign error code
        flag = DSFlags.finish
        reserved_1 = self.null_byte
        reserved_2 = self.null_byte
        section_id = self.null_byte
        data = self.data.encode()  # data should be encoded i.e LOGIN, Admin, root, example1 in bytes
        checksum = self.ds_pdu.get_checksum(timestamp, data)
        pdu_array = [message_type, timestamp, error_code, flag, reserved_1, reserved_2, section_id, data, checksum]

        return pdu_array

    def section(self):
        message_type = DSMessageType.S_EDIT
        timestamp = self.ds_pdu.get_time()  # get timestamp
        error_code = self.ds_code.OK  # assign error code
        flag = DSFlags.finish
        reserved_1 = self.null_byte
        reserved_2 = self.null_byte
        section_id = str(self.array[1]).encode()  # obtain the section id and convert to bytes
        data = self.null_byte
        checksum = self.ds_pdu.get_checksum(timestamp, data)
        pdu_array = [message_type, timestamp, error_code, flag, reserved_1, reserved_2, section_id, data, checksum]
        return pdu_array

    def release(self):
        message_type = DSMessageType.S_RELEASE
        timestamp = self.ds_pdu.get_time()  # get timestamp
        error_code = self.ds_code.OK  # assign error code
        flag = DSFlags.finish
        reserved_1 = self.null_byte
        reserved_2 = self.null_byte
        section_id = str(self.array[1]).encode()  # obtain the section id and convert to bytes
        data = self.null_byte
        checksum = self.ds_pdu.get_checksum(timestamp, data)
        pdu_array = [message_type, timestamp, error_code, flag, reserved_1, reserved_2, section_id, data, checksum]

        return pdu_array

    def commit(self):
        data = self.array[2:]  # this will ensure that other sentences separated by comma's are used as data
        # data is retrieved as list, we need to extract it as string
        data = data[0]
        data_array = self.break_data(data)  # this is the section that contains the data
        freq_to_send = len(data_array)  # number of times we will send in order to complete send
        print('after the data is been broken: {}'.format(data_array, freq_to_send))
        count = 0
        arr = []  # this represents all the pdu_array to be sent
        # print('Data array : {}'.format(data_array))
        for item in data_array:
            count += 1

            message_type = DSMessageType.S_COMMIT
            timestamp = self.ds_pdu.get_time()  # get timestamp
            error_code = self.ds_code.OK  # assign error code
            # in order to set flags
            if count < freq_to_send:
                flag = DSFlags.more

            if count == freq_to_send:
                flag = DSFlags.finish

            reserved_1 = self.null_byte
            reserved_2 = self.null_byte
            section_id = str(self.array[1]).encode()
            try:
                data = item.encode()
            except AttributeError as err:
                data = item

            checksum = self.ds_pdu.get_checksum(timestamp, data)
            pdu_array = [message_type, timestamp, error_code, flag, reserved_1, reserved_2, section_id, data,
                         checksum]
            # print(pdu_array)

            arr.append(pdu_array)

        print(arr)

        return arr  # we are only returning array during the commit

    def logoff(self):
        message_type = DSMessageType.ABORT
        timestamp = self.ds_pdu.get_time()  # get timestamp
        error_code = self.ds_code.OK  # assign error code
        flag = DSFlags.finish
        reserved_1 = self.null_byte
        reserved_2 = self.null_byte
        section_id = str(self.array[1]).encode()  # obtain the section id and convert to bytes
        data = self.null_byte
        checksum = self.ds_pdu.get_checksum(timestamp, data)
        pdu_array = [message_type, timestamp, error_code, flag, reserved_1, reserved_2, section_id, data, checksum]

        return pdu_array

    def break_data(self, data):
        print('WE are in break data')
        print('DATA : {}'.format(data))

        allowed_data_size = self.ds_pdu.get_data_size()
        arr = []
        print('allowed data size: {}, data size {}'.format(allowed_data_size, len(data)))
        if len(data) > allowed_data_size:  # if the size is bigger than the size allocated in struct
            # break data
            print('We are in break data: {}'.format(data))
            data_size = len(data)
            number_of_breakdowns = data_size / allowed_data_size

            stop = allowed_data_size
            start = 0
            for i in range(math.ceil(number_of_breakdowns)):
                data_chunk = data[start:stop].encode('utf-8')
                arr.append(data_chunk)
                start = stop
                stop = stop + allowed_data_size

            return arr

        else:
            print('before')
            print(arr)
            arr.append(data)
            return arr
