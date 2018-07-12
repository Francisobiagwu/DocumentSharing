#!/usr/bin/env python


"""
@author: Francis Obiagwu
@software: SecureDocumentSharing
@file: DSInstruction.py
@time: 6/6/18 7:16 PM
"""


class DSInstruction:

    @staticmethod
    def opening_instruction():
        print('------------------------COMMANDS----------------------------\n'
              'LOGIN: LOGIN, USERNAME, PASSWORD, DOCUMENT_NAME             |\n'
              'REQUEST SECTION: SECTION, SECTION_ID,                       |\n'
              'COMMIT: COMMIT, SECTION_ID, DATA                            |\n'
              'LOGOFF: LOGOFF                                              |\n'
              '------------------------------------------------------------\n')
