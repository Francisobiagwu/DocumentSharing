"""
@author: Francis Obiagwu
@software: SecureDocumentSharing
@file: SDSClient.py
@description: Client class that request for service from the server
@time: 6/6/18 6:24 PM
"""

import socket

from Client import SDSMenu


class SDSClient:
    HOST = 'localhost'  # The remote host
    PORT = 50007  # The same port as used by the server
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    SDSMenu.print_instruction()
    s.sendall(b'Hello, world')
    data = s.recv(1024)
    s.close()
    print('Received', repr(data))
