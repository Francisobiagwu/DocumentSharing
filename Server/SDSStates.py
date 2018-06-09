"""
@author: Francis Obiagwu
@software: SecureDocumentSharing
@file: SDSStates.py
@time: 6/7/18 4:40 AM
"""


class SDSClientStates:
    """
    STATES and ACCEPTABLE MESSAGE TYPE
    -----------------------------------
    WAITING_FOR_CONNECTION: in this state, the server will only accept CONNECT message type
    CONNECTED: in this state, the server will only accept CAUTH message type
    AUTHORIZED: in this state, the server can CAUTH, CONNECT but will choose how to process them
    BLOCKED: in this state, the server will not accept any request from the client
    EDITING: in this state, the server will accept, COMMIT, CAUTH, CONNECT but will choose how to process them
    """
    states_dic = {'WAITING_FOR_CONNECTION': 0, 'CONNECTED': 1, 'AUTHORIZED': 2, 'BLOCKED': 2, 'EDITING': 3}

    def get_states(self):
        """
        Used to return all the states and the associated values
        :return: state dictionary
        """
        return self.states_dic

    def get_state_value(self, key):
        if key == 'WAITING_FOR_CONNECTION':  #
            return self.states_dic.get('WAITING_FOR_CONNECTION')
        elif key == 'CONNECTED':  # in this state, the server will only accept, CAUTH message type
            return self.states_dic.get('CONNECTED')

        elif key == 'AUTHORIZED':
            return self.states_dic.get('AUTHORIZED')
        elif key == 'BLOCKED':
            return self.states_dic.get('BLOCKED')

        elif key == 'EDITING':
            return self.states_dic.get('EDITING')
        else:
            print('key not found')
            return None
