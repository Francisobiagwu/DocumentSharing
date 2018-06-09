"""
@author: Francis Obiagwu
@software: SecureDocumentSharing
@file: SDSServerResponseProcessor.py
@time: 6/9/18 11:31 AM
"""


class SDSServerResponseProcessor:

    def __init__(self, client_socket, client_address):
        self.CLIENT_SOCKET = client_socket
        self.CLIENT_ADDRESS = client_address
        self.continue_to_accept_and_process = True

    def accept_data_and_process(self):
        while self.continue_to_accept_and_process:
            self.CLIENT_SOCKET.recv()
            pass

    def stop_accept_data_and_process(self):
        self.continue_to_accept_and_process = False
