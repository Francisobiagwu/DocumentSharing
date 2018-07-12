"""
@author: Francis Obiagwu
@software: SecureDocumentSharing
@file: DSAuthentication.py
@time: 6/6/18 7:16 PM
"""


class DSAuthentication:
    password = 'root'
    username = 'Admin'
    document_name = 'example1'

    def get_username(self):
        return self.username

    def get_password(self):
        return self.password

    def set_username(self, username):
        self.username = username

    def set_password(self, password):
        self.password = password
