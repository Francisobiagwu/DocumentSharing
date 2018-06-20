#!/usr/bin/env python

__author__ = "Francis Obiagwu"
__copyright__ = "Copyright 2018"
__version__ = "1.0"

import math
import os


class DSDocument:
    __default_path = os.path.abspath("document.txt")

    def __init__( self, allowed_data_size, path=__default_path ):
        self.__path = self.__default_path
        self.document_as_dic = {}
        self.document = ''
        self.free = True
        self.not_Free = False
        self.data_broken = False
        self.__set_document_as_string()  # set document.txt as string
        self.allowed_data_size = allowed_data_size
        self.__set_document_as_string()
        self.__set_document_as_sections()

    def __set_document_as_string( self ):
        """
        Used to assign a value to self.document.txt
        :param data:
        :return: String
        """
        try:
            with open(self.__path, 'r', encoding='utf-8') as file:
                self.document = file.read()

        except (FileNotFoundError, FileExistsError) as err:
            print(err.args, self.__path)

    def get_document_as_string( self ):
        """
        Used to get the document_string
        :return: string
        """
        return self.document

    def __set_document_as_sections( self ):
        """
        Used to set the document.txt into sections
        :return:
        """
        arr = []
        if len(self.document) > self.allowed_data_size:  # if the size is bigger than the size allocated in struct
            # break data
            # print('We are in break data: {}'.format(self.document.txt))
            data_size = len(self.document)
            number_of_breakdowns = data_size / self.allowed_data_size

            stop = self.allowed_data_size
            start = 0
            for i in range(math.ceil(number_of_breakdowns)):
                data_chunk = self.document[start:stop].encode('utf-8')
                self.document_as_dic[i] = (data_chunk, self.free)
                arr.append(data_chunk)
                # print('length of data {}'.format(len(data_chunk)))
                start = stop
                stop = stop + self.allowed_data_size

            # print(self.document_as_dic)
            # print(arr)

            return arr

        else:
            arr.append(self.document.encode('utf-8'))
            self.document_as_dic[0] = (arr[0], self.free)
            print(arr)
            return arr

    def get_document_sections( self ):
        """
        Used to get document.txt sections
        :return: dictionary
        """
        return self.document_as_dic

    def update_document( self, section_id, data = None ):
        """
        Used to update the document.txt, and the dictionary
        :param int section_id:
        :param string data:
        :return:
        """
        # Note: after the update, the length of the section may be greater that the allowed number
        section_id = int(section_id)
        if data is not None:
            print('data {}'.format(data))
            self.document_as_dic.update({section_id: (data.encode('utf-8'), self.free)})
            # print(self.document_as_dic)
            print(self.document_as_dic)
            try:
                # write to the document.txt file
                print('Now writing to the document.txt')
                with open(self.__path, 'w', encoding='utf-8') as file:  # update the main ds_document
                    for item in self.document_as_dic.values():
                        item = item[0]
                        file.write(item.decode('utf-8'))

                # Now read from file and convert the dictionary to the appropriate sizes
                self.__set_document_as_string()
                self.__set_document_as_sections()

            except (FileNotFoundError, FileExistsError) as err:
                print(err.args)

        else:

            section_id = int(section_id)
            section_data, _ = self.document_as_dic.get(section_id)
            print('section id {}'.format(section_id))
            print('Performing a test---------')
            print(self.document_as_dic.get(0))
            print('End of test')
            print('section_data {}'.format(section_data))
            self.document_as_dic.update({section_id: (section_data, self.free)})
            # WE HAVE TO FIND THE KEY SOMEHOW AND THE CONTENT
            # for item in self.document_as_dic.values(): # we don't care about flags
            #
            #     section_data, _ = item
            #     if
            #




    def break_data( self, data ):
        arr = []
        if len(data) > self.allowed_data_size:  # if the size is bigger than the size allocated in struct
            # break data
            # print('We are in break data: {}'.format(self.document.txt))
            data_size = len(data)
            number_of_breakdowns = data_size / self.allowed_data_size

            stop = self.allowed_data_size
            start = 0
            for i in range(math.ceil(number_of_breakdowns)):
                data_chunk = self.document[start:stop].encode('utf-8')
                print(data_chunk, len(data_chunk))
                arr.append(data_chunk)
                start = stop
                stop = stop + self.allowed_data_size

            return arr

        else:
            arr.append(data)
            return data


    def release(self, section_id):
        self.update_document(section_id)
