## Networked Version of the Connect Four Game
###### The user plays the game of Connect Four against an artificial intelligence

import collections
import connectfour
import ConnectFour_ui
import ConnectFour_SocketHandling



def ask_for_username() -> str:
    '''
    Asks the user to input a username that contains no empty/white spaces.
    '''
    while True:
        login = input('Login: ')

        if login.find(' ') != -1:
            print('Username contains an empty space. Please try again.')
        else:
            return login.strip()

        
def server_turn(server_move, gameState):
    '''
    Handles the system when it is the server's turn. Uses the input received from
    the server to drop or pop a piece. Returns the updated board and the current
    game state
    '''
    print('\nIt is Player', gameState.turn + "'s turn.")
            
    if server_move[0] == 'DROP':
        gameState = connectfour.drop_piece(gameState, int(server_move[-1])-1)
        ConnectFour_ui.print_gameboard(gameState)
        print('\nPlayer Y {}ped a piece in column {}.'.format(server_move[0].lower(), server_move[-1]))
        print('\n---------------------------------\n')
        
    elif server_move[0] == 'POP':
        gameState = connectfour.pop_piece(gameState, int(server_move[-1])-1)
        ConnectFour_ui.print_gameboard(gameState)
        print('\nPlayer Y {}ped a piece in column {}.'.format(server_move[0].lower(), server_move[-1]))
        print('\n---------------------------------\n')

    return gameState



def play_game(myConnectFourConnection):
    '''
    The client and server take turns playing the game when there is no winner
    '''
    print('\nHere is the gameboard:\n')
    gameState = ConnectFour_ui.game_state()
    ConnectFour_ui.print_gameboard(gameState)
    
    server_move = []
    
    Cond = True
    while Cond:

        if connectfour.winning_player(gameState) != connectfour.NONE:
            print('\nPlayer', connectfour.winning_player(gameState), 'wins!')
            return

        elif gameState.turn == 'R':
            user = ConnectFour_ui.user_move(gameState)
            if connectfour.winning_player(user[0]) == connectfour.RED:
                print('Player', connectfour.winning_player(user[0]), 'wins!')
                Cond = False
            else:
                server_move = ConnectFour_SocketHandling.servers_next_move(myConnectFourConnection, user[1]) 
                gameState = user[0]
    
        else:
            server = server_turn(server_move, gameState)
            gameState = server
            
            


if __name__ == '__main__':
    ConnectFour_SocketHandling.run_user_interface()


    
