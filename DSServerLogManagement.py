#!/usr/bin/env python

__author__ = "Francis Obiagwu"
__copyright__ = "Copyright 2018"
__version__ = "1.0"

from DSState import DSState
from datetime import datetime


class DSServerLogManagement:
    def __init__( self ):
        self.connected_clients = []
        self.authenticated_clients = []
        self.failed_connection = 0
        self.successful_connection = 0
        self.section_owners = {}

    def add_client_connection( self, client_socket, client_address ):
        """
        Add every connected client socket to a list of connected clients
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
        self.section_owners.update({section_id: client_address})

    def update_section_owners( self, client_address ):
        del self.section_owners[client_address]

    def get_section_owners( self ):
        return self.section_owners

    def remove_client_connection( self, client_socket, client_address ):
        """
        Once the client disconnects, remove the client from connected_client list
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

    def log( self, client_address, state ):
        """
        Logging requires the client's address, timestamp, and the event that occured
        :param client_address:
        :param state:
        :param text_to_write:
        :return:
        """
        date = str(datetime.now())
        str_to_write = date + ' ' + client_address[0] + ' ' + str(client_address[1]) + ' '  + state + '\n'
        path = 'serverlog.txt'
        with open(path, 'a') as file:
            file.write(str_to_write)


    def log_server_start(self, str_to_write):
        date = str(datetime.now())
        path = 'serverlog.txt'
        with open(path, 'a') as file:
            file.write( '\n'+ date + ' '+ str_to_write)

