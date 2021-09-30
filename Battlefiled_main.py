# BATTLEFIELD GAME. A 2-player Python Terminal Game of Battlefield.
#
# Created in 2021 by Vahan Bznuni. For CodeAcademy Portfolio Project: "Terminal Game"
# 
# http://github.com/vahanbznuni/Battlefield-Game

"""
Main Module. Controls main flow of the game.
 
The check_winner funciton checks if there is a winner.
The current_turn_string function returns custom string indicating who's turn it is (Player's or Computer's).
The turn function executes a turn (targetting opposing player).
The ready_to_play contains a print statement for player readiness to start - and a calls a display of the player's battlerfield.
The play_game function executes the main game - by alternating turns until there is a winner.
The end_game function contains the closing statements - including winner statement.
"""

import Battlefield_Objects as obj
import Battlefield_Strings as strings
NL ="\n"

def check_winner():
    """Check if there is a winner.

    Returns:
      The winner (player1 or player2), or <None>, if no winner.
    """
    if player1.check_fleet_sunk():
        winner = player2
    elif player2.check_fleet_sunk():
        winner = player1
    else:
        winner = None
    return winner

def current_turn_string(player):
    """Return custom string indicating to the player who's turn it is (Player's or Computer's).

    Args:
      player: Player object, the Player who's turn it currently is.
    Returns:
      A customized string from the strings module to be printed, indicating current turn.
    """
    if player == player1:
        string = strings.target_str
    elif player == player2:
        string = strings.incoming_str
    return string

def turn(player_x, player_y):
    """Execute a turn, targetting the opposing player using target method of Player or Computer(Player) class/subclass.

    Args:
      player_x: Player object, the Player who's turn it is to target the opposing Player.
      player_y: Player object, the opposing Player against whom the turn is being executed.
    """
    input(strings.continue_str)  
    print(strings.line_str2 + NL*2 + str(current_turn_string(player_x)))
    input(strings.continue_str)
    player_x.target(player_y)

def ready_to_play():
    """print statement indicating that the game (i,e, first turn) is about to start and main player's Battlefiled."""
    print(strings.line_str2 + NL*2 + strings.ready_str + NL)
    player1.battlefield.display()

def play_game():
    """Until there is a winner, alternate turns for player1 and player2."""
    while not check_winner():
        turn(player1, player2)
        if not check_winner():
            turn(player2, player1)

def end_game():
    """Declare the winner and print ending statements."""
    print(strings.winner_str.format(check_winner()))
    print(NL*2 + strings.final_str3)
    print(NL + strings.final_str1)
    input(NL + strings.final_str2)

strings.intro_str()
player1 = obj.Player()
player2 = obj.Computer()

ready_to_play()
play_game()
end_game()