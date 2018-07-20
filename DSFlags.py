#!/usr/bin/env python

"""
@author: Francis Obiagwu
@software: SecureDocumentSharing
@file: DSFlag.py
@time: 6/6/18 7:16 PM
"""


class DSFlags:
    begin = b'BEGIN' # informs the recipient that this the start of data
    more = b'MORE' # informs the recipient that more data is coming
    finish = b'FINISH' # informs the recipient that the sender is done
    pass

