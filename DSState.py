#!/usr/bin/env python

"""
@author: Francis Obiagwu
@software: SecureDocumentSharing
@file: DSState.py
@time: 6/6/18 7:16 PM
"""


from DSMessageType import DSMessageType


class DSState:
    """
    This object is used to inform the client and the server of the next line of action
    to take
    STATES and ACCEPTABLE MESSAGE TYPE
    -----------------------------------
    WAITING_FOR_CONNECTION: in this state, the server will only accept CONNECT message type
    CONNECTED: in this state, the server will only accept CAUTH message type
    AUTHORIZED: in this state, the server can CAUTH, CONNECT but will choose how to process them
    BLOCKED: in this state, the server will not accept any request from the client
    EDITING: in this state, the server will accept, COMMIT, CAUTH, CONNECT but will choose how to process them

    """

    __states = {}
    __current_state = ''  # placeholder value
    CONNECTED = 'CONNECTED'
    AUTHENTICATED = 'AUTHENTICATED'
    EDITING_DOCUMENT = 'EDITING_DOCUMENT'
    RELEASE = 'RELEASING_SECTION'
    BLOCKED = 'BLOCKED'
    COMMITTING_CHANGES = 'COMMITTING_CHANGES'
    CLOSE = 'CLOSE_CONNECTION'
    DISCONNECTED = 'DISCONNECTED'

    def __init__( self ):
        """
        Set default states and assign value to them
        """
        array = [(DSState.CONNECTED, 0), (DSState.AUTHENTICATED, 1), (DSState.BLOCKED, 1),
                 (DSState.EDITING_DOCUMENT, 2), (DSState.COMMITTING_CHANGES, 3), (DSState.CLOSE, -1)]

        for state, value in array:  # update the states dictionary in the states
            # print(state, value)
            self.__states.update({state: value})

        self.__current_state = DSState.CONNECTED
        self.token_issued = False
        self.received_document = {}
        self.is_client_alive = False
        self.is_server_listening = False

    def get_states( self ):
        """
        :return: dictionary
        """
        # print(self.__states)
        return self.__states


    def get_token_status(self):
        return self.token_issued

    def get_current_state( self ):
        """
        :return: string
        """
        print(self.__current_state)
        return self.__current_state

    def get_state_value( self, state ):
        return self.__states.get(state)

    def set_state( self, new_state ):
        """
        Used to set new state
        :param bytes new_state:
        :return: bool
        """

        if new_state in self.__states.keys():
            if self.__states.get(self.__current_state) - self.__states.get(new_state) > 1:
                # reject
                return False

            elif new_state == self.__current_state:
                pass  # do nothing

            else:
                self.__current_state = new_state
                print(self.__current_state)

                return True
        else:
            print('state {} not found in states dictionary'.format(new_state))
            return False

    @staticmethod
    def convert_request( message_type ):
        """
        converts the messagetype received to figure out the next state the client or the server wishes to transition to
        :return:
        """
        if message_type == DSMessageType.CONNECT:
            return DSState.AUTHENTICATED  #


    def set_as_previous_document(self, dictionary):
        self.received_document = dict(dictionary)

