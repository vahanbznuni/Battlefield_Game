# BATTLEFIELD ("Battleship") GAME. A 2-player Python Terminal Game of Battleship
#
# Created in 2021 by Vahan Bznuni
#  for a CodeAcademy Portfolio Project: "Terminal Game"
# 
# http://github.com/vahanbznuni/Battlefield-Game

#Test

"""
Main Module. Controls main flow of the game.
 
The check_winner funciton checks if there is a winner.
The current_turn_string function returns custom string indicating who's turn\
     it is (Player's or Computer's).
The turn function executes a turn (targetting opposing player).
The ready_to_play contains a print statement for player readiness to start\
     - and a calls a display of the player's battlerfield.
The play_game function executes the main game - by alternating turns until\
     there\ is a winner.
The end_game function contains the closing statements - including winner\
     statement.
"""

from Elements.Player import Player, Computer
from Elements.Battlefield_Strings import Battlefield_Strings as strings
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
    """Return custom string indicating to the player who's turn it is (main\
         Player's (player1) or Computer's (player2)).

    Args:
      player (object): the Player who's turn it currently is.
    Returns:
      A customized string from the strings module to be printed,\
           indicating current turn.
    """
    if player == player1:
        string = strings.TargettingStrings.target_str
    elif player == player2:
        string = strings.TargettingStrings.incoming_str
    return string

def turn(player_x, player_y):
    """Execute a turn, targetting the opposing player by calling the target\
         method of the player who's turn it is.

    Targetting is preceded by:
      input: asking playuer to press ENTER key to continue
      print statement: letting player know who's turn it is
      input: asking playuer to press ENTER key to continue

    Args:
      player_x (object): the Player who's turn it is.
      player_y (object): the opposing Player against.
    """
    input(strings.continue_str)  
    print(strings.Formatting.line_str2 + \
        NL*2 + str(current_turn_string(player_x)))
    input(strings.continue_str)
    player_x.target(player_y)

def ready_to_play():
    """print a statement indicating that the game (i.e. first turn) is about\
         to start; and display main player's Battlefiled"""
    print(strings.Formatting.line_str2 + NL*2 + \
        strings.OpeningStatements.ready_str + NL)
    player1.battlefield.display()

def play_game():
    """Until there is a winner, alternate turns for player1 and player2."""
    while not check_winner():
        turn(player1, player2)
        if not check_winner():
            turn(player2, player1)

def end_game():
    """Declare the winner and print ending statements."""
    print(strings.ClosingStatements.winner_str.format(check_winner()))
    print(NL*2 + strings.ClosingStatements.final_str3)
    print(NL + strings.ClosingStatements.final_str1)
    input(NL + strings.ClosingStatements.final_str2)

#-----------------------------------------------------------------------------

#Start Game. Opening Statements.
strings.OpeningStatements.intro_str()

#Initialze players. Includes interactive ship placement by user.
player1 = Player()
player2 = Computer()

#Main Sequence of Game & Ending.
ready_to_play()
play_game()
end_game()