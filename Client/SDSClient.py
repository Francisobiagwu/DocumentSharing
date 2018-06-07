"""
@author: Francis Obiagwu
@software: SecureDocumentSharing
@file: SDSClient.py
@description: Client class that request for service from the server
@time: 6/6/18 6:24 PM
"""

import socket
import time

from Client import SDSMenu
from SDSPdu import SDSPdu


class SDSClient:
    HOST = 'localhost'  # The remote host
    PORT = 50007  # The same port as used by the server
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    BUFFER = 1024
    SDSMenu.print_instruction()
    packet_assembly = SDSPdu.SDSPacketAssembly()

    while 1:
        data = s.recv(BUFFER)
        print(data)
        time.sleep(2)
        s.send(b'hello server')
