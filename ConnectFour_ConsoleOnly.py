## Console-only Version of the Connect Four Game
###### The user plays for both the Red and Yellow players

import collections
import connectfour
import ConnectFour_ui



def play_console_only_game():
    '''
    The user plays for both the Red and Yellow players until there is a winner
    and the game ends
    '''
    print('\nHere is the gameboard:\n')
    gameState = ConnectFour_ui.game_state()
    ConnectFour_ui.print_gameboard(gameState)
    
    while True:
        if connectfour.winning_player(gameState) != connectfour.NONE:
            print('\nPlayer', connectfour.winning_player(gameState), 'wins!\nThank you. Good-bye!')
            return

        else:
            move = ConnectFour_ui.user_move(gameState)
            gameState = move[0]
            


if __name__ == '__main__':
    play_console_only_game()
    
