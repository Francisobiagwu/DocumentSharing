"""
@author: Francis Obiagwu
@software: SecureDocumentSharing
@file: SDSStates.py
@time: 6/7/18 4:40 AM
"""


class SDSClientStates:
    states_dic = {'WAITING_FOR_CONNECTION': 0, 'CONNECTED': 1, 'AUTHORIZED': 2, 'BLOCKED': 2, 'EDITING': 3}

    def get_states(self):
        return self.states_dic

    def get_state_value(self, key):
        if key == 'WAITING_FOR_CONNECTION':
            return self.states_dic.get('WAITING_FOR_CONNECTION')
        elif key == 'CONNECTED':
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

