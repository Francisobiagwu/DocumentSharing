"""
@author: Francis Obiagwu
@software: SecureDocumentSharing
@file: DSStringBuilder.py
@time: 6/6/18 7:16 PM
"""

class DSStringBuilder:

    def __init__(self):
        self.text = ''


    def append(self, string_to_be_appended):
        self.text += string_to_be_appended


    def reset(self):
        self.text = ''


