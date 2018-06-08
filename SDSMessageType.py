"""
@author: Francis Obiagwu
@software: SecureDocumentSharing
@file: SDSMessageType.py
@time: 6/7/18 5:51 PM
"""


class MessageType:
    """
    This is the class used to create various messages used to send pdu back and fourth
    """
    CONNECT = b'CONNECT'
    AUTHORIZE = b'AUTHORIZE'
    SECTION_EDIT = b'SECTION_EDIT'
    COMMIT = b'COMMIT'
    CLOSE = b'CLOSE'
