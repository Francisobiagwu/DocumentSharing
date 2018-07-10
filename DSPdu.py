#!/usr/bin/env python

"""
@author: Francis Obiagwu
@software: SecureDocumentSharing
@file: DSPdu.py
@time: 6/6/18 7:16 PM
"""
import binascii
import struct
from datetime import datetime

from DSCodes import DSCode
from DSDocument import DSDocument


class DSPdu:
    """
    The DSPdu class is used to create a generic pdu object. The user have the option
    of modifying the changing the size of the pdu, adding additional parts to the pdu also
    """


    def __init__( self ):
        """
        This is used to initialize the pdu components and their respective sizes
        """
        ##########################
        # MESSAGE_TYPE    : 12 BYTES  #
        # TIMESTAMP  : 32 BYTES  #
        # ERROR CODE : 4 BYTES   #
        # FLAGS      : 6 BYTES   #
        # RESERVED 1 : 32 BYTES  #
        # RESERVED 2 : 32 BYTES  #
        # SECTION_ID : 32 BYTES  #
        # DATA       : 100 BYTES #
        # CHECKSUM   : 8 BYTES   #
        ##########################
        # TOTAL      : 658 BYTES #
        ##########################
        array = [('MESSAGE_TYPE', '12s'), ('TIMESTAMP', '32s'), ('ERROR_CODES', 'i'), ('FLAG', '6s'),
                 ('RESERVED-1', '32s'), ('RESERVED-2', '32s'), ('SECTION-ID', '32s'),
                 ('DATA', '100s'), ('CHECKSUM', 'q')]

        self.pdu_dic = {}
        self.size = None
        self.format = ''
        self.s = None
        self.null_bytes = b'\x00'
        self.data_size = None
        self.parts_index = []
        for index, item in enumerate(array):
            name, size = item
            self.parts_index.append(index)

            self.format += ' ' + size
            self.pdu_dic[name] = struct.Struct(size).size
            self.s = struct.Struct(self.format)
            self.size = self.s.size
            # print('{:>11}    {:>11}'.format(name, struct.Struct(size).size))

        self.data_size = self.pdu_dic.get('DATA')
        # print(self.data_size)
        # print(self.pdu_dic)
        # print(self.size)

        # for index, pdu_part in enumerate(array):
        #     print(pdu_part[0], index)
        #     self.pdu_parts_index.update({pdu_part[0]: index})

    def get_pdu_parts_index(self):
        return self.parts_index

    def get_data_size(self):
        return self.data_size

    def get_other_pdu_parts( self, request, data ):
        """
        :param byte request:
        :param byte data:
        :return: list
        """
        timestamp = self.get_time()
        checksum = self.get_checksum(timestamp, data)
        # return all the parameters including the DSCode.OK. The client is only allowed to use DSCode.OK
        return [request, checksum, timestamp, DSCode.OK, data]

    def get_time( self ):
        return str(datetime.now()).encode('utf-8')

    def get_checksum( self, timestamp, data ):
        try:
            return binascii.crc32(timestamp + data)
        except TypeError as err:
            print('This value {} is not a byte'.format(data))

    def get_reserved_1( self ):
        return self.null_bytes

    def get_reserved_2( self ):
        return self.null_bytes

    def get_reserved_3( self ):
        return self.null_bytes

    def get_flag( self ):
        pass

    def pack( self, array ):
        """
        Used to return the pdu after it is created
        :return: Struct object
        """
        self.s = struct.Struct(self.format)
        self.size = self.s.size
        return self.s.pack(*array)

    def unpack( self, packed_pdu ):
        """
        Used to unpack pdu
        :param Struct packed_pdu:
        :return: Struct Object
        """
        self.s = struct.Struct(self.format)
        # print(self.s.size)
        # print(self.s.unpack(packed_pdu))
        # print('size of the packed pdu: {}'.format(len(packed_pdu)))
        return self.s.unpack(packed_pdu)

    def get_pdu_part_names( self ):
        """
        Used to return the parts name. When the user is unsure of the pdu parts, they
        can use this to return the pdu component names
        :return: string array
        """
        return self.pdu_part_list

    def remove_padding( self, unpacked_pdu ):
        """
        This processes an unpacked pdu that is padded.
        Then returns the unpacked_pdu without padding
        :param unpacked_pdu:
        :return: list
        """
        array = []
        # print(unpacked_pdu)
        for item in unpacked_pdu:
            if type(item) is bytes:  # this means it is string
                item = item.decode('utf-8')
                padding_index = item.find('\x00')
                if padding_index > 0:
                    array.append(item[:padding_index])
                    # print(array)
                else:  # there is no null bytes
                    array.append(item)
            else:
                array.append(item)

        return array


    def get_size( self ):
        return self.size

