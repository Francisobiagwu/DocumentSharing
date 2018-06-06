"""
@author: Francis Obiagwu
@software: SecureDocumentSharing
@file: SDSServer.py
@description: This is the server side that services client request
@time: 6/6/18 6:44 PM
"""

import socket


class SDSServer:
    HOST = 'localhost'  # Symbolic name meaning all available interfaces
    PORT = 50007  # Arbitrary non-privileged port

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print(HOST, PORT)
    s.bind((HOST, PORT))
    s.listen(1)
    conn, addr = s.accept()
    print('Connected by', addr)
    while 1:
        data = conn.recv(1024)
        if not data: break
        conn.sendall(data)
