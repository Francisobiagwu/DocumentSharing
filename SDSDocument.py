#!/usr/bin/env python

__author__ = "Francis Obiagwu"
__copyright__ = "Copyright 2017, GSCE IDS Project"
__version__ = "1.0"
__email__ = "francis.c.obiagwu.civ@mail.mil"


class BSCADocument:
    __default_path = "document"

    def __init__(self, path=__default_path):
        self.__path = self.__default_path

    def get_document(self):
        try:
            with open(self.__path, 'r', encoding='utf-8') as file:
                print('about getting document')
                document = file.read()
                return document

        except (FileNotFoundError, FileExistsError) as err:
            print(err.args)
