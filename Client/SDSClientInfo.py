"""
@author: Francis Obiagwu
@software: SecureDocumentSharing
@file: SDSClientInfo.py
@time: 6/7/18 6:42 PM
"""


def start_info():
    text = 'Client started\n' \
           '--------------\n'
    print(text)


def print_instruction():
    print('----------------------------------------------\n'
          'Welcome to Secure Document Sharing Application\n'
          '----------------------------------------------\n'
          '              Instructions                    \n'
          'Login: Login, username, password, document_name\n'
          'Request section: Section, section_id\n'
          'Release section: Release\n'
          'Commit section: Commit, text\n')
