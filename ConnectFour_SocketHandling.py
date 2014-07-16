## Implements the I32CFSP and all socket handling.
###### Contains functions that allow the Connect Four game to
###### connect, read, write, etc., via a socket

import collections
import socket
import ConnectFour_NetworkConsole




CONNECTFOUR_HOST = ''
CONNECTFOUR_PORT = ''


ConnectFourConnection = collections.namedtuple(
    'ConnectFourConnection',
    ['socket', 'socket_input', 'socket_output'])


def connect(host: str, port: int) -> ConnectFourConnection:
    '''
    Connects to a Connect Four server running on the given host and listening
    on the given port, returning a ConnectFourConnection object describing
    that connection if successful, or raising an exception if the attempt
    to connect fails.
    '''

    connectfour_socket = socket.socket()
    
    connectfour_socket.connect((host, port))

    connectfour_input = connectfour_socket.makefile('r')
    connectfour_output = connectfour_socket.makefile('w')

    return ConnectFourConnection(
        socket = connectfour_socket,
        socket_input = connectfour_input,
        socket_output = connectfour_output)


def run_user_interface(): # nothing -> interaction
    '''
    Handles the interaction between the user and the server
    '''
    print('Welcome to the Connect Four Game!')
    print('---------------------------------')
    cond = True
    while cond:
        try:
            CONNECTFOUR_HOST = input('Please specify the hostname: ')
            CONNECTFOUR_PORT = int(input('Please specify the port: '))
            connectfour_socket = socket.socket()
            myConnectFourConnection = connect(CONNECTFOUR_HOST, CONNECTFOUR_PORT)
            
            print('Connected successfully!\n')
            print('Please log in with your username.')
            print('Remember that usernames cannot have any empty spaces.')
            username = ConnectFour_NetworkConsole.ask_for_username()
      
            
            ''' Send Message'''
            message_to_send = 'I32CFSP_HELLO ' + username
            myConnectFourConnection.socket_output.write(message_to_send + '\r\n')
            myConnectFourConnection.socket_output.flush()
            reply_message = myConnectFourConnection.socket_input.readline()
            

            if reply_message == 'WELCOME ' + username + '\n':  
                message_to_send = 'AI_GAME'
                myConnectFourConnection.socket_output.write(message_to_send + '\r\n')
                myConnectFourConnection.socket_output.flush()
                reply_message = myConnectFourConnection.socket_input.readline()

                print("\n***********************************\nLet's play,", username + "!"
                      "\nYou are player R.")
                ConnectFour_NetworkConsole.play_game(myConnectFourConnection)
                cond = False
            else:
                print('*****There is a problem with the server.*****')
                cond = False
        except:
            print('***** Invalid host/port or connection problem *****')
    print('\nThank you. Good-bye.')


def client_send_command(myConnectFourConnection, move: str):
    '''
    Sends the client/user's move to the server, returning the server's move
    '''
    message_to_send = move
    myConnectFourConnection.socket_output.write(message_to_send + '\r\n')
    myConnectFourConnection.socket_output.flush()
    

    while True:
        mylist = []
        reply_message = myConnectFourConnection.socket_input.readline()
        
        if (reply_message[0] == 'D') or (reply_message[0] == 'P'):
            mylist.append(reply_message)
            myConnectFourConnection.socket_input.readline()
            return mylist[0].split('\n')[0]
        elif reply_message[0] == 'W':
            mylist.append(reply_message)
            return mylist
        else:
            mylist.append(reply_message)

            
def servers_next_move(myConnectFourConnection, move):
    '''
    Returns the server's response in list form
    '''
    reply = client_send_command(myConnectFourConnection,move)
    servers_move = reply.split()
    return servers_move

