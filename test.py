"""
@author: Francis Obiagwu
@software: SecureDocumentSharing
@file: test.py
@time: 6/7/18 5:54 PM
"""

import Server.SDSAuthentication

t = Server.SDSAuthentication.SDSAuthentication()
print(t.get_password())
print(t.get_username())
