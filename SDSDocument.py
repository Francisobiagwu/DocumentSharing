#!/usr/bin/env python

__author__ = "Francis Obiagwu"
__copyright__ = "Copyright 2017, GSCE IDS Project"
__version__ = "1.0"
__email__ = "francis.c.obiagwu.civ@mail.mil"


class SDSDocument:
    """
    This class is used to read the contents of a text file
    """

    import os
    __default_path = os.path.abspath("document.txt")
    __path = None

    def __init__(self, path=__default_path):
        if path is None:  # is during the initialization there no path is specified, then use the default path
            self.__path = self.__default_path

        else:  # if the during the initialization, the user specified a path, then use the specified path
            self.__path = path

    def get_document(self):
        """
        Used to return the content of the text file
        :return:
        """
        try:
            with open(self.__path, 'r', encoding='utf-8') as file:
                print('about getting document.txt')
                document = file.read()
                return document

        except (FileNotFoundError, FileExistsError) as err:
            print(err.args)
            print('the document.txt was not found')
