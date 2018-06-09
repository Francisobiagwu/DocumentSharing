"""
@author: Francis Obiagwu
@software: SecureDocumentSharing
@file: SDSClientInput.py
@time: 6/9/18 11:08 AM
"""


class SDSClientInput:
    user_input = None  # input entered by the user

    def get_input(self):
        self.user_input = input()  # get user input
        return self.user_input

    def get_user_input_formatted(self):
        """
        This function split user input and removes white spaces
        :return: array of user input
        """
        self.get_input()
        array = [item.rstrip().lstrip() for item in self.user_input.split(',')]  # split and remove white spaces
        return array
