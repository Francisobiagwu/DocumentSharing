"""
@author: Francis Obiagwu
@software: SecureDocumentSharing
@file: SDSClient.py
@description: Client class that request for service from the server
@time: 6/6/18 6:24 PM
"""

import socket
import sys

from Client import SDSClientInfo
from SDSPdu import SDSPdu


class SDSClient:
    HOST = 'localhost'  # The remote host
    PORT = 50007  # The same port as used by the server
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    SDSClientInfo.start_info()
    try:
        s.connect((HOST, PORT))
        BUFFER = 1024
        SDSClientInfo.print_instruction()
        packet_assembly = SDSPdu.SDSPacketAssembly()

        while 1:
            data = s.recv(BUFFER)
            print(data)
            s.send(b'hello server')


    except ConnectionRefusedError as err:
        print('Server not started')
        sys.exit(1)
