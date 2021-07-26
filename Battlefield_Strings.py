import textwrap

line_str1 = \
    """========================================================================
    """
line_str2 = line_str1.replace("=", "-")
side_str1 = line_str1[:int(len(line_str1)/2)-2].replace("=",">")
side_str2 = line_str1[:int(len(line_str1)/2)-2].replace("=","<")

def line_wrap1(str):
    return line_str1 + "\n" + str + "\n" + line_str1
def line_wrap2(str):
    return line_str2 + "\n" + str + "\n" + line_str2
def side_wrap(string):
    half = int((len(string)/2))
    return side_str1[:-half] + string + side_str2[:-half]

header_str =\
    """BATTLEFIELD GAME | for: PYTHON TERMINAL | CREATED 2021 | BY VAHAN BZNUNI
    """
welcome_str = "WELCOME!"
name_str = "Please Enter Your Name: "
continue_str = "\n>>>Please press ENTER key to continue<<<"
game_desc_str1 = \
    """
    \nThis Battlefield game is a Python Terminal version of the classic 'Battlefield' game. 
    In this version, you (player 1) are playing against the computer.
    Each player (in this case you and the computer) has their own Battlefield
    of 10 x 10 squares (coordinates), and 5 ships of different lengths.
    """
game_desc_str2 = \
    """
    \nThis is what a sample Battlefield looks like:
    
       1  2  3  4  5  6  7  8  9  10
    A [ ][ ][ ][ ][ ][ ][ ][ ][ ][ ]
    B [ ][ ][ ][ ][ ][ ][ ][ ][ ][ ]
    C [ ][ ][ ][ ][ ][ ][o][ ][ ][ ]
    D [ ][ ][ ][ ][ ][ ][ ][ ][ ][ ]
    E [ ][ ][ ][ ][+][X][+][+][ ][ ]
    F [ ][ ][ ][ ][ ][ ][ ][ ][ ][ ]
    G [ ][ ][ ][ ][ ][ ][ ][ ][ ][ ]
    H [ ][ ][o][ ][ ][ ][ ][ ][ ][ ]
    I [ ][ ][ ][ ][+][+][+][+][ ][ ]
    J [ ][ ][ ][ ][+][+][+][+][ ][ ]

    Key:
    [ ] = Empty square
    [+] = Occupied square (ship)
    [o] = Targetted square (that was previously empty)
    [X] = Targetted and hit square (that was occupied by a ship)
    """
game_desc_str3 = \
    """
    \nThe following are the ships for each player:

    1. Carrier      +++++   (length of 5 squares)
    2. Battleship   ++++    (length of 4 squares)
    3. Destroyer    +++     (length of 3 squares)
    4. Submarine    +++     (length of 3 squares)
    5. Patrol Boat  ++      (length of 2 squares)
    """
game_desc_str4 = \
    """
    \nThe game will begin by each player (you and the computer) placing 
    their ships on their own battlefields. 
    Then, each player will take turns targetting the opposing player's battlefield.
    if the player succesfully hits a ship, that player will have the next turn. 
    If not, the other player will have the next turn.

    The game is won simply by sunking the entire fleet of the opposint player.
    """
place_ships_str = "\nIt is time to place your ships! Are you ready?"

def intro_str():
    print("\n" + textwrap.dedent(line_wrap1(header_str)))
    print("\n" + textwrap.dedent(welcome_str))
    print("\n")
    input(continue_str)
    print(textwrap.dedent(line_str2 + game_desc_str1))
    input(continue_str)
    print(textwrap.dedent(line_str2 + game_desc_str2))
    input(continue_str)
    print(textwrap.dedent(line_str2 + game_desc_str3))
    input(continue_str)
    print(textwrap.dedent(line_str2 + game_desc_str4))
    input(continue_str)
    print(textwrap.dedent(line_str2 + place_ships_str))
    input(continue_str)
ready_str = "Your ships are all set! Here is your Battlefield:"
target_str = "Now it's your turn to target the enemy!"
target_cords_str = "Please enter target coordinates!"
target_complete = "We've fired our missles to target!"
incoming_str = "Now it's the Enemy's turn to target your Battlefield. Brace for impact!"
incoming_complete = "Enemy missles have landed!"
winner_str_raw = "{} HAS WON!!!"
winner_str = textwrap.dedent(line_wrap2(winner_str_raw))
final_str_raw = "THANK YOU FOR PLAYING!"
final_str = "\n" + textwrap.dedent(line_wrap1(final_str_raw))

#textwrap.dedent(place_ships_str)

#================================================================================
#TESTING

