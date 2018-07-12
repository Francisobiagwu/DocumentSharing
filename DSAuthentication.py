"""
@author: Francis Obiagwu
@software: SecureDocumentSharing
@file: DSAuthentication.py
@time: 6/6/18 7:16 PM
"""


class DSAuthentication:
    password = 'root'
    username = 'Admin'
    document_name = 'document'

    def get_username(self):
        return self.username

    def get_password(self):
        return self.password

    def set_username(self, username):
        self.username = username

    def set_password(self, password):
        self.password = password

    def get_document_name(self):
        return self.document_name
