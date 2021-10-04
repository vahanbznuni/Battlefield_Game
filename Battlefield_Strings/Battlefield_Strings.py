"""
Strings Module. Contains all the strings used by Main and Object modules,\
     and string formatting functionality.

The numbered line_str and side_str variables contain different single-line
  seperator strings.
The numbered line_wrap - as well as side_wrap and center_wrap funcitons assist
  with formatting using seperator strings.
The Intro_str function displays all of the introductory text of the game, and 
  includes user input to continue.
The Object_strings class organizes the main strings used by the Objects module.
"""

import textwrap
import os
dir_path = os.environ.get("HOME") + \
    "\\OneDrive\\Documents\\Computer Science\\_6_Projects\\_1_Code Academy - CS101\\Final Project\\Battlefield Game\\Battlefield_Strings\\"
NL = "\n"

def exctract_str(text_file_name):
    """Extract and return contents of a provided text file

    Args:
      text_file_name (str) : name (with extention) of text file within directory
       of this module.
    Returns:
      string containint entire contents of provided text file
    """
    with open(dir_path + text_file_name, 'r') as filename:
        text = filename.read()
    return text

#Seperator line string for visual formatting, using "=" character.
line_str1 = \
    """=================================================================\
================="""

#Seperator line string for visual formatting, 
# using alternate characters "-" or "*".
line_str2 = line_str1.replace("=", "-")
line_str3 = line_str1.replace("=", "*")

#Formatting line-stringa for headings, to be added from each side, 
# using characters ">", "<".
side_str1 = line_str1[:int(len(line_str1)/2)-2].replace("=",">")
side_str2 = line_str1[:int(len(line_str1)/2)-2].replace("=","<")

#Formatting empty-space string to be added from each side of
#  a heading-type string, acting as center-align.
side_str3 = line_str1[:int(len(line_str1)/2)-2].replace("="," ")

#Formatting functions:
def line_wrap1(str):
    """Return formatted the provided string by adding seperator\
         line_str1 string above and below, with empty space in between."""
    return line_str1 + NL + str + NL + line_str1

def line_wrap2(str):
    """Return formatted the provided string by adding seperator \
        line_str2 string above and below, with empty space in between."""
    return line_str2 + NL + str + NL + line_str2

def line_wrap3(str):
    """Return formatted the provided string by adding seperator \
        line_str3 string above and below, with empty space in between."""
    return line_str3 + NL + str + NL + line_str3

def side_wrap(string):
    """Return formatted the provided string by center-aligning and \
        wrapping with side_str1 from the left, and side_str2 from the right."""
    half = int((len(string)/2))
    return side_str1[:-half] + string + side_str2[:-half]

def center_wrap(string):
    """Return formatted the provided string by center-aligning it \
        (using measured side_str3 empty-space-string)."""
    half = int((len(string)/2))
    return side_str3[:-half] + string + side_str3[:-half]


#Opening statements.
header_str =\
    """BATTLEFIELD GAME | for: PYTHON TERMINAL | CREATED 2021 | BY VAHAN BZNUNI"""
welcome_str = "WELCOME!"

#(Currently not utilized).
name_str = "Please Enter Your Name: "

#To be used with input prompt (asking user to press ENTER key to continue).
continue_str = "\n\n>>>Please press ENTER key to continue<<<"

#Introductory statements, describing the game.



game_desc_str1 = exctract_str("game_desc_str1.txt")
game_desc_str2 = exctract_str("game_desc_str2.txt")
game_desc_str3 = exctract_str("game_desc_str3.txt")
game_desc_str4 = exctract_str("game_desc_str4.txt")
place_ships_str = "\n\nIt is time to place your ships! Are you ready?"
ready_str = "Your ships are all set! Here is your Battlefield:"


def intro_str():
    """print opening and introductory statements, \
        broken up with user input to continue."""
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

#Closing Statements, and formatting.
winner_str_raw = "{} HAS WON!!!"
winner_str = line_wrap3(center_wrap(winner_str_raw))
final_str1_raw = "THANK YOU FOR PLAYING!"
final_str1 = NL + line_wrap3(center_wrap((final_str1_raw)))
final_str2_raw = "\n\n>>>Please press ENTER key to Exit<<<"
final_str2 = NL + center_wrap(final_str2_raw)
final_str3 = NL + line_wrap1(center_wrap(header_str))
final_str4_raw = "THE END."
final_str4 = NL + line_wrap1(center_wrap(final_str4_raw))

class object_strings:
    """Grouping of strings intended for object_strings module.\
    (current version uses strings outside of this class as well.)"""

    #Used for exception handling of interactive ship placement functionaliry of Battlefiled class\
    #and targetting funcitonality of player class
    error_str = NL*2 + "INCORRECT INPUT! \n{} Please try again!"
    value_error_str = \
        "Make sure to enter exact coordinates (for starting coordinate) \nor exact choice number (for ending coordinate)."
    key_error_str = "Make sure your coordinates are in range!"
    index_error_str = "Make sure to enter exact coordinates (for starting coordinate) \nor exact choice number (for ending coordinate)."
    busy_coord_error_str = "There is already a ship in that location!!"
    targetted_coord_error_str = "These Coordinates have already been targetted!!"
    not_enough_room_error_str = "There is no enough room for this ship at that coordinate!"
    
    #Gameplay statements.
    target_str = "Now it's your turn to target the enemy!"
    incoming_str = "Now it's the Enemy's turn to target your Battlefield.\
    Brace for impact!"
    
    #Used for interactive ship placement functionaliry of Battlefiled class and targetting funcitonality ofplayer class
    target_cords_str = "Please enter target coordinates!"
    gen_coords_input1_str = "Please enter {0} coordinate for the position of {1} ({2}): "
    gen_coords_input2_str_addon = "Enter the *NUMBER* corresponding to the coordinates option of your choice : "
    
    #Used during targetting (target method of PLayer or Computer(Player) classes).
    target_complete = "We've fired our missles to target!"
    incoming_complete = "Enemy missles have landed!"
    ship_hit_str = "Target at {} - Ship hit at target!!!"
    empty_waters_str = "Empty waters hit. Target at {}. No ships at target."
    
    #Used when displaying the ships of either player.
    display_ships_intro = "The following are {} ships:"
    display_ships_str_main = "{}. {}\t\t{}"

    #Battlefield caption, for display functionality of Battlefiled class.
    enemy_battlefield_str = "Enemy Battlefield: "
    player_battlefield_str = "Your Battlefield: "
    battlefield_str = "{} Battlefield: "