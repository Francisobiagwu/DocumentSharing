#!/usr/bin/env python

__author__ = "Francis Obiagwu"
__copyright__ = "Copyright 2018"
__version__ = "1.0"

class DSCode:
    OK = 000
    LOGIN_SUCCESS = 100
    SECTION_RETRIEVED = 101
    COMMIT_SUCCESS = 102
    COMMIT_UPDATE = 103
    TIMEOUT = 104

    LOGIN_NOT_SUCCESS = 110
    SECTION_DENIED = 111
    SECTION_NOT_AVAILABLE = 112
    SECTION_ID_NOT_VALID = 113
    RELEASE_SECTION = 114
    COMMIT_DENIED = 115
    LOGOFF = 116
    OPERATION_DENIED = 117
    RELEASE_SECTION_SUCCESSFUL = 118
    RELEASE_SECTION_NOT_SUCCESSFUL = 119
    ABORT_SUCCESSFUL = 220
    ABORT_NOT_SUCCESSFUL = 221
    SECTION_REVOKED = 222




    def dscode_print(self, code):
        if code == DSCode.OK:
            return '----Connection Successful----'

        elif code == DSCode.LOGIN_SUCCESS:
            return '----Login Successful----'

        elif code == DSCode.SECTION_RETRIEVED:
            return '----Section successfully retrieved----'

        elif code == DSCode.COMMIT_SUCCESS:
            return







