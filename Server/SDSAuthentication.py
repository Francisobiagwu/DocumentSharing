"""
@author: Francis Obiagwu
@software: SecureDocumentSharing
@file: SDSAuthentication.py
@time: 6/6/18 7:16 PM
"""


class Credentials:
    password = 'root'
    username = 'Admin'

    def get_username(self):
        return self.username

    def get_password(self):
        return self.password

    def set_username(self, username):
        self.username = username

    def set_password(self, password):
        self.password = password
