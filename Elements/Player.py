
"""
Player Module. Contains interactive user - and AI gameplay elements.

The Player class stores each player's individual Battlefield, a listing of their 
  ships; contains interagtive ship placement and targetting functionality.
The Computer subclass of Player overrides the ship placement and targetting
  functionality of parent class (custumized for AI).
The Ship module contains the Ship object (i.e. ship-related data).
The Battlefield_Strings package
"""

if __name__ == "__main__":
    import sys
    import os
    sys.path.append(os.path.join( os.path.dirname( __file__ ), '..' ))

from Elements.Battlefield import Battlefield, ComputerBattlefield
from Elements.Ship import Ship
from Elements.Battlefield_Strings.Battlefield_Strings import \
    NL, continue_str, Formatting, DisplayStrings, ShipPLacementStrings, \
        TargettingStrings, ErrorStrings
from Elements.Exceptions.InputExceptions import \
    BusyCoordinateException, TargettedCoordinateException, NotEnoughRoomException
import random

class Player:
    """Stores each player's individual Battlefield, a listing of their ships, \
        as well as interagtive ship placement abd targetting functionality.

    Subclassed by Computer(Player), which overrides __init__ (so that a
    ComputerBattlefiled is assigned instead of Battlefiled as an attribute),
    gen_coords (to replace user prompt with random input for computer),
    generate_ships (to customize exception handling; ex. removing error statements),
    __repr__, target (replacing user-input targetting random selection from
    smart targetting options), and adds functions that supply the smart
    (AI) targetting: non_adjascent_targets, adjascent_targets, target_options.

    Class Variables:
      player_count (int): number of players - increased with each new Player
        initialized.
    Instance Variables:
      id (int): The assigned number of player (increased by one for each new player)
      battlefield (object): The player's personal Battlefield, on which the
        player's ships are placed.
      fleet (dict): A dictionary listing player's ships type names (str) as keys,
        and ships (obnject) as values.
      fleet_sunk (bool): True if the player's entire fleet has been sunk
    Methods:
      __init__, __repr__, , gen_coords, generate_ships, check_fleet_sunk, 
      display_ships, display_targetting_results, target
    """

    player_count = 0

    def __init__(self):
        """initialize an instance of a Player."""
        Player.player_count += 1
        self.id = Player.player_count
        self.battlefield = Battlefield(10, 10)
        self.fleet = self.generate_ships()
        self.fleet_sunk = False
        # self.targetted_coordinates = []
        # self.hit_coordinates = []
        # self.active_targets = []

    def __repr__(self):
        """String representation of Player containing the Player's \
            number (ex. Player 1)."""
        return "Player" + str(self.id)

    def gen_coords(self, ship_type):
        """Generate coordinates for a given ship type, using user input.\
             **(Overridden by Computer subclass)**

        Args:
          ship_type (str): name of the type of ship/
        Returns:
          sorted list of valid coordinates of a ship of the provided type,
            starting on coordinate chosen by user and placed in the direction of
            the user's choosing.
        Exceptions Raised:
          BusyCoordinateException: when chosen coordinate already contains a ship
          NotEnoughRoomException: when there is no room for any ship starting at
            chosen coordinate
        """
        self.battlefield.display_wrapped("Your")
        
        ship_size = Ship.types[ship_type]
        coordinates = []
        
        #Prompt for user input of starting coordinate of a given ship type.
        #  Raise exception if a ship already exist at input coordinate.
        input_str = ShipPLacementStrings.gen_coords_input1_str
        input1 = \
            input(input_str.format("starting", str(ship_type), ship_size*"+"))
        start_coordinate = (input1[0].upper(), int(input1[1:]))
        if self.battlefield.grid[start_coordinate] == Battlefield.states[5]:
            raise BusyCoordinateException
        coordinates.append(start_coordinate)
        
        print(NL)
        #Backup copy of grid to be used to restore it back from temporary
        #  changes maide for purposes of visual aide in ship selection process.
        copy_grid = self.battlefield.grid.copy()
        self.battlefield.grid[start_coordinate] = "*"
        
        #Customizing string for next selection
        input2_str_addon = ShipPLacementStrings.gen_coords_input2_str_addon
        input2_str = \
            input_str.format(
                "ending", str(ship_type), ship_size*"+").replace(
                    "enter", "choose").replace(
                        ":", ".")\
                             + "\n" +input2_str_addon + NL*2
        
        #Obtain valid options for ship placement from starting coordinate.
        #  Raise exception if there is not enough room for any ship.
        options = self.battlefield.coord_opts(start_coordinate, ship_type)
        if not options:
            self.battlefield.grid.update(copy_grid)
            raise NotEnoughRoomException
        
        #Display options to user and prompt user to select option using a
        #  numerical identifier displayed
        num = 1
        for key in options.keys():
            last_coord = options[key][-1]
            input2_str += \
                str(num) + " ({}): ".format(key[:-2]) + \
                    Battlefield.coord_to_str(last_coord) +"\n"
            self.battlefield.grid[last_coord] = num
            num += 1
        self.battlefield.display()
        print(NL)
        input2 = input(input2_str)
        
        #Restore original grid
        self.battlefield.grid.update(copy_grid)
        
        #Add the rest of the coordinates (except for starting) from the chosen
        #  option to a list & return sorted list
        for coord in list(options.values())[int(input2) - 1][1:]:
            coordinates.append(coord)
        coordinates.sort()
        return coordinates
     
    def generate_ships(self):
        """Call coordinate generator for each ship type, check if coordinates\
             are valid, and generate ship \
                 **(Overridden by Computer subclass)**

        Returns:
          Fleet (dict): with keys as names of ship type, 
            and values as the ship (object).
        
        Exceptions Raised:
          ValueError: for when coordinates are not entered; or option number
            is not entered, correctly as prompted.
          KeyError: for when entered coordinates are out of range.
          IndexError: for when coordinates are not entered; or option number 
           is not entered, correctly as prompted.
          BusyCoordinateException: for when there is already a ship at a chosen 
            coordinate.
          NotEnoughRoomException: for when there is no enough room for a ship to
            be placed at a chosen coordinate.
        """
        fleet = {}
        for ship_type in Ship.types.keys():
            error_str = ErrorStrings.error_str
            while True:
                try:
                    ship = Ship(
                        self.gen_coords(ship_type), ship_type, self.battlefield)
                    break
                except ValueError:
                    print(error_str.format(ErrorStrings.value_error_str))
                except KeyError:
                    print(error_str.format(ErrorStrings.key_error_str))
                except IndexError:
                    print(error_str.format(ErrorStrings.index_error_str))
                except BusyCoordinateException:
                    print(error_str.format(ErrorStrings.busy_coord_error_str))
                except NotEnoughRoomException:
                    print(error_str.format(ErrorStrings.not_enough_room_error_str))
            fleet[ship_type] = ship
        return fleet
    
    def check_fleet_sunk(self):
        """Check if the entire fleet has been sunk. If so, update fleet_sunk \
            attribute to True.
        
        Returns:
          fleet_sunk (bool): (True if all ships have been sunk).
        """
        sunk_ships = 0
        for ship in self.fleet.values():
            if ship.sunk:
                sunk_ships += 1
        if sunk_ships == len(self.fleet):
            self.fleet_sunk = True
        return self.fleet_sunk
    
    def display_ships(self):
        """Print a listing of all of the non-sunk ships of the player, \
            and a visual representation of each ship."""
        #Customization for caption to be displayed
        if self.id == 1:
            player_str = "YOUR"
        elif self.id == 2:
            player_str = "ENEMY"
        
        #Obtain non-sunk ships.
        ships = [ship for ship in self.fleet.values() if not ship.sunk]
        
        #print caption statement
        print(NL + Formatting.line_str1 + NL)
        print(DisplayStrings.display_ships_intro.format(player_str))
        
        #print each afloat ship's name, followed by a representation of
        #  correct size (with "+" character")
        num = 1
        for ship in ships:
            print(DisplayStrings.display_ships_str_main.format(
                num, ship.type, "+"*ship.size), end="\n")
            num += 1
        print(NL)

    @staticmethod
    def display_targetting_results(player, coordinate, target_hit):
        if target_hit:
            result_str = NL*2 + \
                Formatting.line_wrap3(
                    TargettingStrings.ship_hit_str.format(str(coordinate)))\
                         + NL*2
        else:
            result_str = NL*2 + \
                TargettingStrings.empty_waters_str.format(str(coordinate))\
                     + NL*2
        print(NL*2 + TargettingStrings.target_complete + NL)
        player.battlefield.display()
        print(result_str)
    
    def target(self, player):
        """target the opposing player's battlefield based on coordinates \
            input by the user (intended for player1)

        Args:
          player (object): the being targetted
        """
        #Track targetting attempt, and whether last attempt was successful
        shot = 0
        last_shot_hit = False
        
        #if last attempt successful (target hit), the targetting repeats.
        while shot < 1 or last_shot_hit:
            battlefield = player.battlefield
            grid = player.battlefield.grid
            #Display enemy ships, enemy battlefield, and prompt user input for
            #  cooordinate to target. 
            #Raise exception if input coordinate has already been targetted.
            #Handle exceptions and print error message. If exceptions occur,
            #  targetting is attempted again.
            while True:
                player.display_ships()
                input(continue_str)
                battlefield.display_wrapped("Enemy")
                error_str = ErrorStrings.error_str
                try:
                    input1 = (input(TargettingStrings.target_cords_str))
                    coordinate = (input1[0].upper(), int(input1[1:]))
                    if grid[coordinate] == Battlefield.states[6] \
                        or grid[coordinate] == Battlefield.states[7]\
                        or grid[coordinate] == Battlefield.states[9]:
                        raise TargettedCoordinateException
                    break
                except ValueError:
                    print(error_str.format(ErrorStrings.value_error_str))
                except KeyError:
                    print(error_str.format(ErrorStrings.key_error_str))
                except IndexError:
                    print(error_str.format(ErrorStrings.index_error_str))
                except TargettedCoordinateException:
                    print(error_str.format(
                        ErrorStrings.targetted_coord_error_str))
            
            shot += 1
            #If no target hit, update coordinate status on the grid to show a
            #  targetted (missed) coordiante, display battlefield, print a
            #  status statement, and update attempt count & success tracket
            #  (exiting function)
            if not grid[coordinate]:
                grid[coordinate] = Battlefield.states[6]
                self.display_targetting_results(player, coordinate, False)
                last_shot_hit = False
            
            #If a target was hit, update coordinate status on the grid to show
            #  a hit coordiante,\
            #  display battlefield, print a status statement, and update attempt
            #  count & success tracket (exiting function)
            elif grid[coordinate] == Battlefield.states[5]:
                grid[coordinate] = Battlefield.states[7]
                self.display_targetting_results(player, coordinate, True)
                last_shot_hit = True
                
                #Check each enemy ship to see if they've been sunk (updating
                #  sunk attribute of the ship).
                #Check if entire fleet has been sunk (updating fleet_sunk
                #  attribute of the player)
                #If the fleet has been sunk, break out - to end the game
                for ship in player.fleet.values():
                    if coordinate in ship.coordinates:
                        ship.check_sunk()
                if player.check_fleet_sunk():
                    break
                
                input(continue_str)
                print(Formatting.line_str2 + NL*2 + TargettingStrings.target_str)
                input(continue_str)

class Computer(Player):
    """Stores each player's individual Battlefield, a listing of their ships, \
        as well as interagtive targetting functionality.

    Overrides the following from parent class: __init__ (so that a
    ComputerBattlefiled is assigned instead of Battlefiled as an attribute),
    gen_coords (to replace user prompt with random input for computer),
    generate_ships (to customize exception handling; ex. removing error statements),
    __repr__, target (replacing user-input targetting random selection from
    smart targetting options), and adds functions that supply the smart
    (AI) targetting: non_adjascent_targets, adjascent_targets, target_options.

    Instance Variables:
      id (int): The assigned number of player (increased by one for each new
        player/computer)
      battlefield (object): The computer's personal ComputerBattlefield,
        on which the computer's ships are placed.
      fleet (dict): A dictionary listing computer's ships type names (str)
        as keys, and ships (object) as values.
      fleet_sunk (bool): True if the computer's entire fleet has been sunk.
      self.targetted_coordinates (list): list of targetted coordinates
        (hit or missed)
      self.hit_coordinates (list): list of hit coordinates
      self.active_targets (list): list of hit coordinates of a ships that
        have not yet fully been sunk
    Methods:
      __init__ (overrides parent), __repr__ (overrides parent), 
      gen_coords (overrides parent), generate_ships (overrides parent), 
      target (overrides parent), non_adjascent_targets, adjascent_targets,
      target_options
    """
    
    def __init__(self):
        """initialize an instance of a Computer."""
        Player.player_count += 1
        self.id = Player.player_count
        self.battlefield = ComputerBattlefield(10, 10)
        self.fleet = self.generate_ships()
        self.fleet_sunk = False
        self.targetted_coordinates = []
        self.hit_coordinates = []
        self.active_targets = []

    def __repr__(self):
        """String representation of Computer."""
        return "Computer"
    
    def gen_coords(self, ship_type):
        """Generate coordinates for a given ship type, using random input. \
            **(Overrides parent class)**.

        Args:
          ship_type (str): name of the type of ship/
        Returns:
          sorted list of valid coordinates of a ship of the provided type, 
           starting on a randomly generated coordinate and placed in a random 
           direction.
        Exceptions Raised:
          BusyCoordinateException: when randomly chosen coordinate already
            contains a ship
          NotEnoughRoomException: when there is no room for any ship starting at
            a randomly chosen coordinate
        """
        coordinates = []
        
        #Randomly generate starting cooriundate. Raise exception if a ship
        #  already exist at randomly chosen coordinate
        start_coordinate = \
            (self.battlefield.rows[
                random.randint(0, len(self.battlefield.rows)-1)], \
                random.randint(1, len(self.battlefield.columns)))
        if self.battlefield.grid[start_coordinate] == Battlefield.states[5]:
            raise BusyCoordinateException
        coordinates.append(start_coordinate)
        
        #Obtain valid options for ship placement from starting coordinate.
        #  Raise exception if there is not enough room for any ship.
        options = list(
            self.battlefield.coord_opts(start_coordinate, ship_type).values())
        if not options:
            raise NotEnoughRoomException
        
        #Add the rest of the coordinates (except for starting) from the chosen
        #  option to a list & return sorted list
        for coord in options[random.randint(0, len(options)-1)][1:]:
            coordinates.append(coord)
        coordinates.sort()
        return coordinates

    def generate_ships(self):
        """Call coordinate generator for each ship, check if coordinates are\
             valid, and place ship on the player's Battlefield. \
                 **(Overrides parent class)**.

        The reason for overriding parent class is to remove print statements
        during exception handling, and to remove ValueError, KeyError, and
        IndexError from exception handling. 
        
        Returns:
          Fleet (dict): with keys as names of ship type, and values as the ship
            (object).
        Exceptions Raised:
          BusyCoordinateException: for when there is already a ship at a chosen
            coordinate.
          NotEnoughRoomException: for when there is no enough room for a ship
            to be placed at a chosen coordinate.
        """
        fleet = {}
        for ship_type in Ship.types.keys():
            while True:
                try:
                    ship = Ship(
                        self.gen_coords(ship_type), ship_type, self.battlefield)
                    break
                except BusyCoordinateException as a:
                    pass
                except NotEnoughRoomException as b:
                    pass
            fleet[ship_type] = ship
        return fleet

    def non_adjascent_targets_inner(
        self, coordinate, player, direction_func,
            target_rows_or_columns, largest_ship_size):
        """Helper method (inner logic) for non_adjascent_targets method.
        
        Check the seperation between a provided active target (coordinate
        belonging to a partially hit ship), and the next active target within
        the same row or column, and return a list of coordinates in between the
        targets if they are close enough to belong to the same ship.

        Args:
          coordinate (tuple): a coordinate.
          player (object): 
          direction_func (function): one of coord_up/down/left/right "direction"
            helper methods.
          target_rows_or_colukmns (list): 
          largest_ship_size (int):
        Returns:
          A list of coordinate options for targetting
        """
        options = []
        row_index = player.battlefield.row_index
        current_coord = coordinate
        
        #Determine if evaluating non-adjascent active targets in the same column
        # (direction=right) or those in the same
        # row (direction=down), and calculate seperation between provided 
        # coordinate and next coordinate in the given direction
        if direction_func == player.battlefield.coord_right:
                target_columns = target_rows_or_columns
                index_difference = \
                    target_columns[
                        target_columns.index(coordinate[-1]) + 1] - coordinate[-1]
        elif direction_func == player.battlefield.coord_down:
                target_row_indices = target_rows_or_columns
                index_difference = \
                    target_row_indices[
                        target_row_indices.index(row_index(coordinate[0])) + 1] \
                            - row_index(coordinate[0])
        seperation = index_difference - 1
        
        #If the non-adjascent active targets are close enough to potentially
        # belong to a ship (as compared to the largest non-sunk ship),
        # append the coordinates in between to the options list and return it, 
        # unless one of them has already been discovered to be void of ships.
        if (largest_ship_size - 2) >= seperation >= 1:
            for num in range(seperation):
                next_coord = direction_func(current_coord)
                if next_coord in self.targetted_coordinates \
                    and next_coord not in self.hit_coordinates:
                    options = None
                    break
                elif next_coord not in self.targetted_coordinates:
                    options.append(next_coord)
                current_coord = next_coord
        return options
    
    def non_adjascent_targets(self, coordinate, player):
        """Evaluate non-adjascent partially hit coordinates (active targets)\
             for potentially belonging to a single ship, \
                 and return inner coordinates as targetting options, if so.

        Args:
          coordinate (tuple): a coordinate.
          player (object): 
        Returns:
          A list of coordinate options for targetting
        """
        battlefield = player.battlefield
        options = []                 
        row_index = battlefield.row_index
        row = battlefield.get_row(coordinate)
        column = battlefield.get_column(coordinate)
        
        #Obtain active targets (partially hit ship coordinates) within the 
        # same row and same column
        targets_in_row = [
            target for target in self.active_targets if target in row]
        targets_in_column = [
            target for target in self.active_targets if target in column]
        
        largest_ship_size = 0
        for ship in self.fleet.values():
            if not ship.sunk:
                if ship.size >= largest_ship_size:
                    largest_ship_size = ship.size
        
        #If multiple active targets within the same row as provided coordinate, 
        # check if they are close enough to possibly contain a single ship
        if len(targets_in_row) > 1:
            target_columns = [target[-1] for target in targets_in_row]
            target_columns.sort()
            if target_columns.index(coordinate[-1]) < len(target_columns) - 1:
                row_options = self.non_adjascent_targets_inner(
                    coordinate, player, battlefield.coord_right, 
                    target_columns, largest_ship_size)
                options.extend(
                    [option for option in row_options if option not in options])    
        
        #Same as above - except for column
        if len(targets_in_column) > 1:
            target_row_indices = [
                row_index(target) for target in targets_in_column]
            target_row_indices.sort()
            if target_row_indices.index(
                row_index(coordinate[0])) < len(target_row_indices) - 1:
                column_options = self.non_adjascent_targets_inner(
                    coordinate, player, battlefield.coord_down, 
                    target_row_indices, largest_ship_size)
                options.extend(
                    [option for option in column_options if option not in options])

        return options
    
    def adjascent_targets(self, direction_func, coord, player):
        """Check adjascent coordinate if it is also hit, and if so, return the\
             next non-targetted coordinate in the same direction as a likely\
                  smart target option

        Args:
          direction_func (function): one of coord_up/down/left/right 
            "direction" helper methods.
          coord (tuple): a coordinate.
          player (object): 
        Returns:
          list containing smart coordinate option for adjascent hit targets 
            (next non-targetted coordinate over).
        """
        options = []
        range_value = player.battlefield.get_range_value(direction_func, coord)
        current_coord = coord
        if direction_func(coord) \
            and direction_func(coord) in self.hit_coordinates:
            for num in range(range_value):
                next_coord = direction_func(current_coord)
                if next_coord in self.targetted_coordinates \
                    and next_coord not in self.hit_coordinates:
                    break
                elif next_coord not in self.targetted_coordinates:
                    if next_coord not in options:
                        options.append(next_coord)
                    break
                else:
                    pass
                current_coord = next_coord
        return options
    
    def target_options(self, player):
        battlefield = player.battlefield
        target_options = []
        coord_up = battlefield.coord_up                    
        coord_down = battlefield.coord_down                   
        coord_left = battlefield.coord_left                   
        coord_right = battlefield.coord_right
        
        if self.active_targets:
            options = []
            for coordinate in self.active_targets:
                options.extend(self.non_adjascent_targets(coordinate, player))
            if options:
                target_options.extend(
                    [option for option in options if option not in target_options])
                return target_options
            
            else:
                for coordinate in self.active_targets:   
                    if coord_up(coordinate):
                        options.extend(
                            self.adjascent_targets(coord_up, coordinate, player))
                    if coord_down(coordinate):
                        options.extend(
                            self.adjascent_targets(coord_down, coordinate, player))
                    if coord_left(coordinate):
                        options.extend(
                            self.adjascent_targets(coord_left, coordinate, player))
                    if coord_right(coordinate):
                        options.extend(
                            self.adjascent_targets(coord_right, coordinate, player))
                if options:
                    target_options.extend([option for option in options \
                        if option not in target_options])
                    return target_options
                
                else:    
                    for coordinate in self.active_targets:
                        if coord_up(coordinate):
                            if coord_up(coordinate) \
                                not in self.targetted_coordinates \
                                and coord_up not in target_options:
                                options.append(coord_up(coordinate))
                        if coord_down(coordinate):
                            if coord_down(coordinate) \
                                not in self.targetted_coordinates \
                                and coord_down not in target_options:
                                options.append(coord_down(coordinate))
                        if coord_left(coordinate):
                            if coord_left(coordinate) \
                                not in self.targetted_coordinates \
                                and coord_left not in target_options:
                                options.append(coord_left(coordinate))
                        if coord_right(coordinate):
                            if coord_right(coordinate) \
                                not in self.targetted_coordinates \
                                and coord_right not in target_options:
                                options.append(coord_right(coordinate))
                    target_options.extend(
                        [option for option in options \
                            if option not in target_options])
                    return target_options
        
        else:
            available_targets = \
                [coordinate for coordinate in battlefield.coordinates \
                    if not battlefield.grid[coordinate]\
                 or battlefield.grid[coordinate] == Battlefield.states[5]]  
            options = []
            options_preferred_A = []
            options_preferred_B = []
            options_preferred_C = []
            options_preferred_D = []
            options_preferred_E = []
            options_preferred_F = []
            options_preferred_G = []
            
            preferred_lists_temp_1 = [options_preferred_A, options_preferred_B,
             options_preferred_C, options_preferred_D, options_preferred_E, 
             options_preferred_F, options_preferred_G]
            
            preferred_lists_temp_2 = [options_preferred_A, options_preferred_B, 
             options_preferred_C, options_preferred_D]
            
            for coordinate in available_targets:
                for ship in player.fleet.values():
                    if not ship.sunk:
                        if ship.size <= battlefield.horizontal_target_size(
                            coordinate, self.targetted_coordinates)\
                             or ship.size <= battlefield.vertical_target_size(
                                 coordinate, self.targetted_coordinates):
                            if coordinate not in options:
                                options.append(coordinate)
            
            for option in options:
                up_2x = (coord_up(option) \
                    and coord_up(option) in available_targets)\
                    and (coord_up(coord_up(option)) \
                        and coord_up(coord_up(option)) in available_targets)
                
                down_2x = (coord_down(option) \
                    and coord_down(option) in available_targets)\
                    and (coord_down(coord_down(option)) \
                        and coord_down(coord_down(option)) in available_targets)
                
                left_2x = (coord_left(option) \
                    and coord_left(option) in available_targets)\
                    and (coord_left(coord_left(option)) \
                        and coord_left(coord_left(option)) in available_targets)
                
                right_2x = (coord_right(option) \
                    and coord_right(option) in available_targets)\
                    and (coord_right(coord_right(option)) \
                        and coord_right(coord_right(option)) in available_targets)
                
                up_1x = (coord_up(option) \
                    and coord_up(option) in available_targets)
                down_1x = (coord_down(option) \
                    and coord_down(option) in available_targets)
                left_1x = (coord_left(option) \
                    and coord_left(option) in available_targets)
                right_1x = (coord_right(option) \
                    and coord_right(option) in available_targets)
                
                A = (up_2x and down_2x and left_2x and right_2x)
                B = (up_2x and down_2x and left_1x and right_1x) \
                    or (up_1x and down_1x and left_2x and right_2x)
                C = (up_1x and down_1x and left_1x and right_1x)
                D = (up_2x and down_2x and (left_1x or right_1x)) \
                    or ((up_1x or down_1x) and left_2x and right_2x)
                E = ((up_2x and down_2x) or (left_2x and right_2x))
                F = ((up_1x and down_1x) or (left_1x and right_1x))
                G = (up_1x or down_1x or left_1x or right_1x)
                
                if A and option not in options_preferred_A:
                    options_preferred_A.append(option)
                elif B and option not in options_preferred_B:
                    options_preferred_B.append(option)
                elif C and option not in options_preferred_C:
                    options_preferred_C.append(option)
                elif D and option not in options_preferred_D:
                    options_preferred_D.append(option)
                elif E and option not in options_preferred_E:
                    options_preferred_E.append(option)
                elif F and option not in options_preferred_F:
                    options_preferred_F.append(option)
                elif G and option not in options_preferred_G:
                    options_preferred_G.append(option)
                    
            preferred_lists_1 = [x for x in preferred_lists_temp_1 if x]
            preferred_lists_2 = [x for x in preferred_lists_temp_2 if x]
            
            if preferred_lists_1:
                alternative_num = random.randint(0, 1)
                if alternative_num == 0 or not preferred_lists_2:
                    target_options.extend(
                        [option for option in preferred_lists_1[0]\
                             if option not in target_options])
                else:
                    target_options.extend(
                        [option for option in preferred_lists_2[
                            random.randint(0, len(preferred_lists_2) - 1)]\
                                 if option not in target_options])
                return target_options
            else:
                target_options.extend([option for option in options \
                    if option not in target_options])
                return target_options

    def target(self, player):
        shot = 0
        last_shot_hit = False
        while shot < 1 or last_shot_hit:
            battlefield = player.battlefield
            grid = player.battlefield.grid
            rows = battlefield.rows
            columns = battlefield.columns
            player.display_ships()
            input(continue_str)
            battlefield.display_wrapped("Your")
            input(continue_str)
            while True:
                try:
                    options = self.target_options(player)
                    if options:
                            coordinate = options[
                                random.randint(0, len(options)-1)]
                    else:
                        coordinate = (rows[
                            random.randint(0, len(rows)-1)], 
                            random.randint(1, len(columns)))
                    if grid[coordinate] == Battlefield.states[6] \
                        or grid[coordinate] == Battlefield.states[7]\
                        or grid[coordinate] == Battlefield.states[9]:
                            raise TargettedCoordinateException
                    break
                except Exception as e:
                    pass
            self.targetted_coordinates.append(coordinate)
            if not grid[coordinate]:
                grid[coordinate] = Battlefield.states[6]
                print(NL*2 + TargettingStrings.incoming_complete + NL)
                battlefield.display()
                print(NL*2 + TargettingStrings.empty_waters_str.format(
                    str(coordinate)) + NL*2)
                shot += 1
                last_shot_hit = False
            elif grid[coordinate] == Battlefield.states[5]:
                grid[coordinate] = Battlefield.states[7]
                print(NL*2 + TargettingStrings.incoming_complete + NL)
                battlefield.display()
                print(NL*2 + Formatting.line_wrap3(
                    TargettingStrings.ship_hit_str.format(
                    str(coordinate))) + NL*2)
                last_shot_hit = True
                shot += 1
                self.hit_coordinates.append(coordinate)
                self.active_targets.append(coordinate)
                for ship in player.fleet.values():
                    if coordinate in ship.coordinates:
                        ship.check_sunk()
                        if ship.sunk:
                            for coord in ship.coordinates:
                                self.active_targets.remove(coord)
                if player.check_fleet_sunk():
                    break
                input(continue_str)
                print(Formatting.line_str2 + NL*2 + \
                    TargettingStrings.incoming_str)
                input(continue_str)