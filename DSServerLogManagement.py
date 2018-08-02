#!/usr/bin/env python

"""
@author: Francis Obiagwu
@software: SecureDocumentSharing
@file: DSServerLogManagement.py
@time: 6/6/18 7:16 PM
"""

from datetime import datetime

from DSState import DSState


class DSServerLogManagement:
    def __init__( self ):
        self.connected_clients = []
        self.authenticated_clients = []
        self.failed_connection = 0
        self.successful_connection = 0
        self.section_owners = {}
        self.document_sent_to_client = {}

    def add_client_connection( self, client_socket, client_address ):
        """
        Add every connected client socket to a list of connected clients
        :param client_address:
        :param Socket client_socket:
        :return: None
        """
        if client_socket not in self.connected_clients:
            self.connected_clients.append(client_socket)
            self.successful_connection += 1
            self.log(client_address, DSState.CONNECTED)
        else:
            pass

    def add_authenticated_client_connection( self, client_socket, client_address ):
        """
        Add every authenticated client to a list of authenticated clients
        :param client_address:
        :param Socket client_socket:
        :return: None
        """
        if client_socket not in self.authenticated_clients:
            self.authenticated_clients.append(client_socket)
            self.log(client_address, DSState.AUTHENTICATED)
        else:
            pass

    def increase_failed_connections( self ):
        self.failed_connection += 1

    def add_section_owners( self, client_address, section_id ):
        print('section id type: {}'.format(type(section_id)))
        self.section_owners.update({section_id: client_address})

    def update_section_owners( self, client_address, section_id):
        section_id = int(section_id)
        if client_address in self.get_section_owners().values():
            if client_address == self.get_section_owners().get(section_id):
                print('Before update: {}'.format(self.section_owners))
                del self.section_owners[section_id]
                print('After the update {}'.format(self.section_owners))

        else:
            pass

    def get_section_owners( self ):
        return self.section_owners

    def remove_client_connection( self, client_socket, client_address ):
        """
        Once the client disconnects, remove the client from connected_client list
        :param client_address:
        :param Socket client_socket:
        :return: None
        """
        if client_socket in self.connected_clients:
            self.connected_clients.remove(client_socket)
            self.log(client_address, DSState.DISCONNECTED)

        else:
            pass

    def remove_authenticated_client_connection( self, client_socket, client_address ):
        """
        When an authenticated client connection is no longer authenticated, remove from authenticated
        list
        :param client_address:
        :param Socket client_socket:
        :return: None
        """
        if client_socket in self.authenticated_clients:
            self.authenticated_clients.remove(client_socket)
            self.log(client_address, DSState.CONNECTED)
        else:
            pass

    def get_connected_clients( self ):
        return self.connected_clients

    def get_authenticated_clients( self ):
        return self.authenticated_clients

    def get_no_failed_connections( self ):
        return self.failed_connection

    @staticmethod
    def log( client_address, state ):
        """
        Logging requires the client's address, timestamp, and the event that occurred
        :param client_address:
        :param state:
        :return:
        """
        date = str(datetime.now())
        str_to_write = date + ' ' + client_address[0] + ' ' + str(client_address[1]) + ' '  + state + '\n'
        path = 'serverlog.txt'
        with open(path, 'a') as file:
            file.write(str_to_write)


    @staticmethod
    def log_server_start( str_to_write ):
        date = str(datetime.now())
        path = 'serverlog.txt'
        with open(path, 'a') as file:
            file.write( '\n'+ date + ' '+ str_to_write)

