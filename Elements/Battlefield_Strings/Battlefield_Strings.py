"""
Strings Module. Contains the collection of majority if strings used by the\
    various modules of the game, organized into classes.


The exctract_str function extracts larger strings saved into seperate text files
"""

import textwrap
import os

#Path of current module's directory
dir_path = os.path.dirname(__file__)

NL = "\n"

#To be used with input prompt (asking user to press ENTER key to continue).
continue_str = "\n\n>>>Please press ENTER key to continue<<<"

def exctract_str(text_file_name):
    """Extract and return contents of a provided text file

    Args:
      text_file_name (str) : name (with extention) of text file within directory
       of this module.
    Returns:
      string containint entire contents of provided text file
    """
    with open(os.path.join(dir_path, text_file_name), 'r') as filename:
        text = filename.read()
    return text

class Formatting:
    """Collection of variables and methods for visual formatting of stirngs.

    Instance Variables:
      line_str1 (str): Seperator line string for visual formatting,
         using "=" character.
      line_str2 (str): Seperator line string for visual formatting, 
        using alternate character ("-")
      line_str3 (str): Seperator line string for visual formatting, 
        using alternate character ("*")
      side_str1 (str): Formatting line-stringa for headings, 
        to be added from each side, using ">" character
      side_str2 (str): Formatting line-stringa for headings, 
        to be added from each side, using "<" character
      side_str3 (str): Formatting empty-space string to be added from each side
       of a heading-type string, acting as center-align.
    Methods:
      line_wrap1, line_wrap12, line_wrap13, side_wrap, center_wrap
    """

    #Seperator line string for visual formatting, using "=" character.
    str_base = "="
    line_str1 = str_base*86

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

    #Formatting methods:
    @classmethod
    def line_wrap1(cls, str):
        """Return formatted the provided string by adding seperator\
            line_str1 string above and below, with empty space in between."""
        return cls.line_str1 + NL + str + NL + cls.line_str1

    @classmethod
    def line_wrap2(cls, str):
        """Return formatted the provided string by adding seperator \
            line_str2 string above and below, with empty space in between."""
        return cls.line_str2 + NL + str + NL + cls.line_str2

    @classmethod
    def line_wrap3(cls, str):
        """Return formatted the provided string by adding seperator \
            line_str3 string above and below, with empty space in between."""
        return cls.line_str3 + NL + str + NL + cls.line_str3

    @classmethod
    def side_wrap(cls, str):
        """Return formatted the provided string by center-aligning and \
            wrapping with side_str1 from the left, \
                and side_str2 from the right."""
        half = int((len(str)/2))
        return cls.side_str1[:-half] + str + cls.side_str2[:-half]

    @classmethod
    def center_wrap(cls, str):
        """Return formatted the provided string by center-aligning it \
            (using measured side_str3 empty-space-string)."""
        half = int((len(str)/2))
        return cls.side_str3[:-half] + str + cls.side_str3[:-half]

class OpeningStatements:
    """Opening statements and formatting"""
    #Opening statements.
    header_str =\
        """BATTLEFIELD GAME | for: PYTHON TERMINAL | CREATED 2021 | BY VAHAN BZNUNI"""
    welcome_str = "WELCOME!"

    #Introductory statements, describing the game.
    game_desc_str1 = exctract_str("game_desc_str1.txt")
    game_desc_str2 = exctract_str("game_desc_str2.txt")
    game_desc_str3 = exctract_str("game_desc_str3.txt")
    game_desc_str4 = exctract_str("game_desc_str4.txt")
    place_ships_str = "\n\nIt is time to place your ships! Are you ready?"
    ready_str = "Your ships are all set! Here is your Battlefield:"

    @classmethod
    def intro_str(cls):
        """print opening and introductory statements, \
            broken up with user input to continue."""
        print(NL + \
            Formatting.line_wrap1(Formatting.center_wrap(cls.header_str)))
        print(NL*2 + \
            Formatting.line_wrap3(Formatting.center_wrap(cls.welcome_str)))
        input(continue_str)
        print(textwrap.dedent(NL + Formatting.line_str1 + cls.game_desc_str1))
        input(continue_str)
        print(textwrap.dedent(NL + Formatting.line_str1 + cls.game_desc_str2))
        input(continue_str)
        print(textwrap.dedent(NL + Formatting.line_str1 + cls.game_desc_str3))
        input(continue_str)
        print(textwrap.dedent(NL + Formatting.line_str1 + cls.game_desc_str4))
        input(continue_str)
        print(textwrap.dedent(NL + Formatting.line_str1 + cls.place_ships_str))
        input(continue_str)

class ClosingStatements:
    """Closing Statements, and formatting."""

    winner_str_raw = "{} HAS WON!!!"
    winner_str = Formatting.line_wrap3(Formatting.center_wrap(winner_str_raw))
    final_str1_raw = "THANK YOU FOR PLAYING!"
    final_str1 = NL + Formatting.line_wrap3(
        Formatting.center_wrap((final_str1_raw)))
    final_str2_raw = "\n\n>>>Please press ENTER key to Exit<<<"
    final_str2 = NL + Formatting.center_wrap(final_str2_raw)
    final_str3 = NL + Formatting.line_wrap1(
        Formatting.center_wrap(OpeningStatements.header_str))
    final_str4_raw = "THE END."
    final_str4 = NL + Formatting.line_wrap1(
        Formatting.center_wrap(final_str4_raw))

class DisplayStrings:
    """Used for Battlefield or Ship display captions"""
    
    #Battlefield caption, for display functionality of Battlefiled class.
    enemy_battlefield_str = "Enemy Battlefield: "
    player_battlefield_str = "Your Battlefield: "
    battlefield_str = "{} Battlefield: "

    #Used when displaying the ships of either player.
    display_ships_intro = "The following are {} ships:"
    display_ships_str_main = "{}. {}\t\t{}"

class ShipPLacementStrings:
    """Used for interactive ship placement"""

    gen_coords_input1_str = \
        "Please enter {0} coordinate for the position of {1} ({2}): "
    gen_coords_input2_str_addon = \
        "Enter the *NUMBER* corresponding to the coordinates option of your choice : "
    
class TargettingStrings:
    """Used during targettinhg"""

    target_str = "Now it's your turn to target the enemy!"
    target_cords_str = "Please enter target coordinates!"
    target_complete = "We've fired our missles to target!"
    incoming_str = \
        "Now it's the Enemy's turn to target your Battlefield. Brace for impact!"
    incoming_complete = "Enemy missles have landed!"
    ship_hit_str = "Target at {} - Ship hit at target!!!"
    empty_waters_str = "Empty waters hit. Target at {}. No ships at target."

class ErrorStrings:
    """Used for exception handling of interactive ship placement functionaliry\
         of Battlefiled class and targetting funcitonality of player class
    """

    error_str = NL*2 + "INCORRECT INPUT! \n{} Please try again!"
    value_error_str_p1 = \
        "Make sure to enter exact coordinates (for starting coordinate)"
    value_error_str_p2 = \
        "or exact choice number (for ending coordinate)."
    value_error_str = value_error_str_p1 + NL + value_error_str_p2
    key_error_str = "Make sure your coordinates are in range!"
    index_error_str_p1 = \
        "Make sure to enter exact coordinates (for starting coordinate)"
    index_error_str_p2 = \
        "or exact choice number (for ending coordinate)."
    index_error_str = index_error_str_p1 + NL + index_error_str_p2
    busy_coord_error_str = "There is already a ship in that location!!"
    targetted_coord_error_str = \
        "These Coordinates have already been targetted!!"
    not_enough_room_error_str = \
        "There is no enough room for this ship at that coordinate!"
    