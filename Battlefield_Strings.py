import textwrap

NL = "\n"
line_str1 = \
    """=================================================================================="""
line_str2 = line_str1.replace("=", "-")
line_str3 = line_str1.replace("=", "*")
side_str1 = line_str1[:int(len(line_str1)/2)-2].replace("=",">")
side_str2 = line_str1[:int(len(line_str1)/2)-2].replace("=","<")
side_str3 = line_str1[:int(len(line_str1)/2)-2].replace("="," ")

def line_wrap1(str):
    return line_str1 + NL + str + NL + line_str1
def line_wrap2(str):
    return line_str2 + NL + str + NL + line_str2
def line_wrap3(str):
    return line_str3 + NL + str + NL + line_str3
def side_wrap(string):
    half = int((len(string)/2))
    return side_str1[:-half] + string + side_str2[:-half]
def center_wrap(string):
    half = int((len(string)/2))
    return side_str3[:-half] + string + side_str3[:-half]

header_str =\
    """BATTLEFIELD GAME | for: PYTHON TERMINAL | CREATED 2021 | BY VAHAN BZNUNI"""
welcome_str = "WELCOME!"
name_str = "Please Enter Your Name: "
continue_str = "\n\n>>>Please press ENTER key to continue<<<"
game_desc_str1 = \
"""\n\nThis Battlefield game is a Python Terminal version of the classic 'Battlefield' game. 
In this version, you (player 1) are playing against the computer.
Each player (in this case you and the computer) has their own Battlefield
of 10 x 10 squares (coordinates), and 5 ships of different lengths."""
game_desc_str2 = \
    """\n\nThis is what a sample Battlefield looks like:
    
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
    [X] = Targetted and hit square (that was occupied by a ship)"""
game_desc_str3 = \
    """\n\nThe following are the ships for each player:

    1. Carrier      +++++   (length of 5 squares)
    2. Battleship   ++++    (length of 4 squares)
    3. Destroyer    +++     (length of 3 squares)
    4. Submarine    +++     (length of 3 squares)
    5. Patrol Boat  ++      (length of 2 squares)"""
game_desc_str4 = \
"""\n\nThe game will begin by each player (you and the computer) placing 
their ships on their own battlefields. 
Then, each player will take turns targetting the opposing player's battlefield.
if the player succesfully hits a ship, that player will have the next turn. 
If not, the other player will have the next turn.

The game is won simply by sunking the entire fleet of the opposint player."""
place_ships_str = "\n\nIt is time to place your ships! Are you ready?"

def intro_str():
    print(NL + line_wrap1(center_wrap(header_str)))
    print(NL*2 + line_wrap3(center_wrap(welcome_str)))
    input(continue_str)
    print(textwrap.dedent(NL + line_str1 + game_desc_str1))
    input(continue_str)
    print(textwrap.dedent(NL + line_str1 + game_desc_str2))
    input(continue_str)
    print(textwrap.dedent(NL + line_str1 + game_desc_str3))
    input(continue_str)
    print(textwrap.dedent(NL + line_str1 + game_desc_str4))
    input(continue_str)
    print(textwrap.dedent(NL + line_str1 + place_ships_str))
    input(continue_str)
ready_str = "Your ships are all set! Here is your Battlefield:"
target_str = "Now it's your turn to target the enemy!"
enemy_battlefield_str = "Enemy Battlefield: "

incoming_str = "Now it's the Enemy's turn to target your Battlefield. Brace for impact!"
player_battlefield_str = "Your Battlefield: "

winner_str_raw = "{} HAS WON!!!"
winner_str = textwrap.dedent(line_wrap3(winner_str_raw))
final_str_raw = "THANK YOU FOR PLAYING!"
final_str = NL + textwrap.dedent(line_wrap1(final_str_raw))

class object_strings:
    error_str = NL*2 + "INCORRECT INPUT! \n{} Please try again!"
    target_cords_str = "Please enter target coordinates!"
    value_error_str = "Make sure to enter exact coordinates (for starting coordinate) \nor exact choice number (for ending coordinate)."
    key_error_str = "Make sure your coordinates are in range!"
    index_error_str = "Make sure to enter exact coordinates (for starting coordinate) \nor exact choice number (for ending coordinate)."
    busy_coord_error_str = "There is already a ship in that location!!"
    targetted_coord_error_str = "These Coordinates have already been targetted!!"
    not_enough_room_error_str = "There is no enough room for this ship at that coordinate!"
    gen_coords_input1_str = "Please enter {0} coordinate for the position of {1} ({2}): "
    gen_coords_input2_str_addon = "Enter the *NUMBER* corresponding to the coordinates option of your choice : "
    target_complete = "We've fired our missles to target!"
    incoming_complete = "Enemy missles have landed!"
    ship_hit_str = "Ship hit at target!"
    empty_waters_str = "Empty waters hit. No ships at target."

#textwrap.dedent(place_ships_str)

#================================================================================
#TESTING

