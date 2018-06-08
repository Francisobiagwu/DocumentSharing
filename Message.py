#!/usr/bin/env python

__author__ = "Francis Obiagwu"
__copyright__ = "Copyright 2017, GSCE IDS Project"
__version__ = "1.0"
__email__ = "francis.c.obiagwu.civ@mail.mil"

from enum import Enum


class Messages(Enum):
    """
    The use this enums for Deterministic Finite Automata (DFA) to keep track of server's state
    """
    HELLO = 1
    PROCESSING = 2
    SIGN_IN = 2
    CREATE_NEW_ACCOUNT = 2
    DEPOSIT = 3
    WITHDRAWAL = 3
    CLOSE_ACCOUNT = 3
    CHANGE_NAME = 3
    CHANGE_ADDRESS = 3
    GOOD_BYE = 4
