"""
Objects Module. Contains all the classes of the game, which contain all data, display, interactivity, and internal game funcitonality elements.
 
The Battlefield class contains the main data structure(s) for players' Battlefields'; display functionality, and interactive ship placement for player.
The ComputerBattlefield subclass of Battlefield class overrides display and ship placement functionality of the parent class (custumized for computer).
The Ship class contains data structure(s) relating to each ship, including its coordinates, it's name/type, and it's health status.
The Player class stores each player's individual Battlefield, a listing of their ships, as well as interagtive targetting functionality.
The Computer subclass of Player overrides targetting functionality and related attributes/methods of parent class (custumized for computer).
The InputException subclass of the built-in Exception class - as well as subclasses of InputException - assist with the game's exception handling.
"""

import string
from Battlefield_Strings import line_str1, line_str2, NL, continue_str, line_wrap3, object_strings as obj_str, \
    battlefield_str, ready_str, target_str, incoming_str
import random

class Battlefield:
    """Serves as each player's individual "Battlefield" - using a grid coordinate system containing data for ships placed by the player\
        and otherwise tracking each coordinate's status (empty, untargetted ("healthy") ship, targetted & missed,  targetted and hit ship). 
    
    Includes functionality for displaying battlefiled to terminal, placing ships on battlefiled (based on user input),
    and providing a muiltitude of helper funcitons that assist with the coordinate system, from generating coordinate 
    options for ship placement (based on coordinate input from the player) to checking maximum clearance size of a given 
    coordinate for evaluation as a valid target by smart targetting funcitonality of the Computer(Player) (sub)class.

    Subclassed by ComputerBattlefield, which overrides ship placement for the computer, including coordinate generator
    method (since it does not require user input), as well as the display funcitonality - so as not to display the computer's ships
    to the player (player1) when otherwise displaying the computer's battlefiled to the main player.

    Class variables:
      states (list): List of possible statuses ("states") for coordinates in grid
    Instance Variables:
      rows (list): A list of alphabetical rows the Battlefield instance is comprised of 
      columns (list): A list of columns the Battlefield instance is comprised of.
      coordinates (list): A list of coordinates the Battlefield instance is comprised of.
      grid (dict): The main data structure for the coordinate system, containing coordinates of the Battlefiled as\ 
        keys, and the data for each coordinate indicating it's status ("state" - i.e. empty, hit, etc.) as values.
      states (list): A class variable list containing all different possible statuses for a given grid coordinate. Whenever the state of a\
          given coordinate needs to be accessed or overwrittene by a new state, it is accessed via the list, instead of being referenced\
              explicitly.
    Methods:
      __init__, display, display_wrapped, coord_to_str, row_index, get_row, get_column, coord_up, coord_down, coord_left
      coord_right, next_targetted_coord, horizontal_target_size, vertical_target_size, coord_opts, gen_coords, generate_ships
    """
    
    states = [None, 1, 2, 3, 4, "healthy", "targetted", "hit", "*", "#"]
        #List of possible states for coordinates in grid
        #Numbers 1-4 and star symbol (*) are used temporarily for interactive ship generation prompt.
        #Hashtag symbol (#) is used for sunk ship coordinates.

    def __init__(self, num_rows, num_columns):
        """initialize an instance of a Battlefield.
        
        Args:
          num_rows (int): number of rows for the Battlefield's grid coordinate system.
          num_columns (int): number of columns for the Battlefield's grid coordinate system.
        """
        self.rows = [row for row in string.ascii_uppercase[:num_rows]]
        self.columns = [column for column in range(1, num_columns+1)]
        self.coordinates = []
        for row in self.rows:
            for column in self.columns:
                self.coordinates.append((row, column))
        self.grid = {coordinate: None for coordinate in self.coordinates}

    def display(self):
        """Display Battlefield to the terminal based on data contained in grid. **(Overridden by ComputerBattlefiled subclass)**."""
        print("   " + "  ".join([str(column) for column in self.columns]))
        for row_name in self.rows:
            row = []
            for key in self.grid.keys():
                if key[0] == row_name:
                    if not self.grid[key]:
                        row.append("[ ]")
                    elif self.grid[key]==Battlefield.states[1]:
                        row.append("[1]")
                    elif self.grid[key]==Battlefield.states[2]:
                        row.append("[2]")
                    elif self.grid[key]==Battlefield.states[3]:
                        row.append("[3]")
                    elif self.grid[key]==Battlefield.states[4]:
                        row.append("[4]")
                    elif self.grid[key]==Battlefield.states[5]:
                        row.append("[+]")
                    elif self.grid[key]==Battlefield.states[6]:
                        row.append("[o]")
                    elif self.grid[key]==Battlefield.states[7]:
                        row.append("[X]")
                    elif self.grid[key]==Battlefield.states[8]:
                        row.append("[*]")
                    elif self.grid[key]==Battlefield.states[9]:
                        row.append("[#]")                      
            print(row_name + " " + "".join(row))
   
    def display_wrapped(self, string):
        """Add visual formatting to display of the Battlefield (using seperator strings form strings module)."""
        print(line_str1)
        print(NL)
        print(battlefield_str.format(string))
        print(NL)
        self.display()
        print(NL)
    
    @staticmethod
    def coord_to_str(coordinate):
        """Convert the provided coordinate (tuple) into a string."""
        return str(coordinate[0]) + str(coordinate[-1])
    
    def row_index(self, coordinate):
        """Return the index, in the rows list, of the row the provided coordinate belongs to"""
        return self.rows.index(coordinate[0])

    def get_row(self, coordinate):
        """Return a list containing all the coordinates from the row that the provided coordinate belongs to."""
        row = []
        for column in self.columns:
            row.append((coordinate[0], column))
        return row

    def get_column(self, coordinate):
        """Return a list containing all the coordinates from the column that the provided coordinate belongs to."""
        column = []
        for row in self.rows:
            column.append((row, coordinate[-1]))
        return column

    def coord_up(self, coordinate):
        """Return the coordinate above (North) of the provided coordinate."""
        if self.row_index(coordinate) - 1 >= 0:
            return (self.rows[self.row_index(coordinate) - 1], coordinate[-1])

    def coord_down(self, coordinate):
        """Return the coordinate below (South) of the provided coordinate."""
        if self.row_index(coordinate) + 1 < len(self.rows):
            return (self.rows[self.row_index(coordinate) + 1], coordinate[-1])

    def coord_left(self, coordinate):
        """Return the coordinate to the left (West) of the provided coordinate."""
        if (coordinate[-1]) - 1 >= 1:
            return (coordinate[0], coordinate[-1] - 1)

    def coord_right(self, coordinate):
        """Return the coordinate to the right (East) of the provided coordinate."""
        if (coordinate[-1]) + 1 <= len(self.columns):
            return (coordinate[0], coordinate[-1] + 1)

    def coord_opts_direction(self, coordinate, ship_size, direction_func):
        """Return a list of coordinates of a ship of given size in a given direction, starting at given coordinate.
        
        Args:
          coordinate (tuple): a coordinate.
          ship_size (int): ship size.
          direction_func: one of coord_up/down/left/right "direction" helper methods.
        Returns:
          a list of coordinates.
        """
        coords = [coordinate]
        current_coord = coordinate
        for num in range(ship_size - 1):
            next_coord = direction_func(current_coord)
            if self.grid[next_coord] == Battlefield.states[5]:
                coords = None
                break
            coords.append(next_coord)
            current_coord = next_coord
        return coords
    
    def next_targetted_coord(self, direction_func, coord, targetted_coordinates):
        """Find next coordinate on the grid, in a given direction, that has already been targetted (either hit or missed). 

        Args:
          direction_func (function): one of coord_up/down/left/right "direction" helper methods.
          coord (tuple): a coordinate.
          targetted_coordinates (list): a list of targetted coordinates (either hit or missed).
        Returns:
          The next coordinate (tuple), if any.
        """
        coord_up = self.coord_up                    
        coord_down = self.coord_down                   
        coord_left = self.coord_left                   
        coord_right = self.coord_right
        row_index = self.row_index
        
        #range_value (used with range function) is the measure of length until the border of the Battlefield in a given direction.
        if direction_func == coord_up:
            range_value = row_index(coord)
        elif direction_func == coord_down:
            range_value = len(self.rows) - row_index(coord)
        elif direction_func == coord_left:
            range_value = coord[-1]
        elif direction_func == coord_right:
            range_value = len(self.columns) - coord[-1]
        
        current_coord = coord
        if direction_func(coord) and direction_func(coord) not in targetted_coordinates:
            for num in range(range_value):
                next_coord = direction_func(current_coord)
                if next_coord in targetted_coordinates:
                    return next_coord
                elif next_coord:
                    current_coord = next_coord
    
    def horizontal_target_size(self, coord, targetted_coordinates):
        """Calculate maximum availble horizontal non-targetted space around a given coordinate (to determine if it is big enouth to hide a ship).

        Args:
          coord (tuple): a coordinate.
          targetted_coordinates (list): a list of targetted coordinates (either hit or missed).
        Returns:
          the linear horizontal size (int) of adjascent available (non-targetted) space around the coordinate. 
        """              
        coord_left = self.coord_left                   
        coord_right = self.coord_right
        left_border = self.next_targetted_coord(coord_left, coord, targetted_coordinates)
        right_border = self.next_targetted_coord(coord_right, coord, targetted_coordinates)
        
        if left_border and right_border:
            difference = right_border[-1] - left_border[-1]
            target_size = difference - 1
        elif left_border and not right_border:
            difference = len(self.rows) - left_border[-1]
            target_size = difference
        elif not left_border and right_border:
            difference = right_border[-1]
            target_size = difference - 1
        elif not left_border and not right_border:
            target_size = len(self.rows)
        return target_size
    
    def vertical_target_size(self, coord, targetted_coordinates):
        """Calculate maximum availble vertical non-targetted space around a given coordinate (to determine if it is big enouth to hide a ship).

        Args:
          coord (tuple): a coordinate.
          targetted_coordinates (list): a list of targetted coordinates (either hit or missed).
        Returns:
          the linear vertical size (int) of adjascent available (non-targetted) space around the coordinate. 
        """ 
        coord_up = self.coord_up                    
        coord_down = self.coord_down                   
        row_index = self.row_index
        top_border = self.next_targetted_coord(coord_up, coord, targetted_coordinates)
        bottom_border = self.next_targetted_coord(coord_down, coord, targetted_coordinates)
        
        if top_border and bottom_border:
            difference = row_index(bottom_border) - row_index(top_border) 
            target_size = difference - 1
        if top_border and not bottom_border:
            difference = len(self.rows) - 1 - row_index(top_border)
            target_size = difference
        if not top_border and bottom_border:
            difference = row_index(bottom_border)
            target_size = difference
        if not top_border and not bottom_border:
            target_size = len(self.rows)
        return target_size
    
    def coord_opts(self, coordinate, ship_type):
        """Return coordinate options for a ship placed starting at provcided coordinate, in all four directions.

        Args:
          coordinate (tuple): a Coordinate
          ship_type (str): name of the type of ship
        Returns:
          a dictionary with keys identifying direction, and values as a list of coordinates of a ship placed in that directrion\
              from the provided coordinate as a starting point, given there is enouth space.
        """
        ship_size = Ship.types[ship_type]
        options = {"Up: ": None, "Down: ": None, "Left: ": None, "Right: ": None, }
        
        if self.row_index(coordinate) - (ship_size - 1) >= 0:
            options["Up: "] = self.coord_opts_direction(coordinate, ship_size, self.coord_up)
        
        if self.row_index(coordinate) + (ship_size - 1) < len(self.rows):
            options["Down: "] = self.coord_opts_direction(coordinate, ship_size, self.coord_down)
        
        if (coordinate[-1]) - (ship_size - 1) >= 1:
            options["Left: "] = self.coord_opts_direction(coordinate, ship_size, self.coord_left)
        
        if (coordinate[-1]) + (ship_size - 1) <= len(self.columns):
            options["Right: "] = self.coord_opts_direction(coordinate, ship_size, self.coord_right)
        
        return {key: value for (key, value) in options.items() if value != None}
    
    def gen_coords(self, ship_type):
        """Generate coordinates for a given ship type, using user input. **(Overridden by ComputerBattlefiled subclass)**

        Args:
          ship_type (str): name of the type of ship/
        Returns:
          sorted list of valid coordinates of a ship of the provided type, starting on coordinate chosen by user\
              and placed in the direction of the user's choosing.
        Exceptions Raised:
          BusyCoordinateException: when chosen coordinate already contains a ship
          NotEnoughRoomException: when there is no room for any ship starting at chosen coordinate
        """
        self.display_wrapped("Your")
        
        ship_size = Ship.types[ship_type]
        coordinates = []
        
        #Prompt for user input of starting coordinate of a given ship type. Raise exception if a ship already exist at input coordinate.
        input_str = obj_str.gen_coords_input1_str
        input1 = input(input_str.format("starting", str(ship_type), ship_size*"+"))
        start_coordinate = (input1[0].upper(), int(input1[1:]))
        if self.grid[start_coordinate] == Battlefield.states[5]:
            raise BusyCoordinateException
        coordinates.append(start_coordinate)
        
        print(NL)
        #Backup copy of grid to be used to restore it back from temporary changes maide for purposes of visual aide in ship selection process.
        copy_grid = self.grid.copy()
        self.grid[start_coordinate] = "*"
        
        #Customizing string for next selection
        input2_str_addon = obj_str.gen_coords_input2_str_addon
        input2_str = input_str.format("ending", str(ship_type), ship_size*"+").replace("enter", "choose").replace(":", ".") + "\n" +\
            input2_str_addon + NL*2
        
        #Obtain valid options for ship placement from starting coordinate. Raise exception if there is not enough room for any ship.
        options = self.coord_opts(start_coordinate, ship_type)
        if not options:
            self.grid.update(copy_grid)
            raise NotEnoughRoomException
        
        #Display options to user and prompt user to select option using a numerical identifier displayed
        num = 1
        for key in options.keys():
            last_coord = options[key][-1]
            input2_str += str(num) + " ({}): ".format(key[:-2]) + Battlefield.coord_to_str(last_coord) +"\n"
            self.grid[last_coord] = num
            num += 1
        self.display()
        print(NL)
        input2 = input(input2_str)
        
        #Restore original grid
        self.grid.update(copy_grid)
        
        #Add the rest of the coordinates (except for starting) from the chosen option to a list & return sorted list
        for coord in list(options.values())[int(input2) - 1][1:]:
            coordinates.append(coord)
        coordinates.sort()
        return coordinates
     
    def generate_ships(self):
        """Call coordinate generator for each ship, check if coordinates are valid, and place ship on the player's Battlefield.\
            **(Overridden by ComputerBattlefiled subclass)**

        Returns:
          Fleet (dict): with keys as names of ship type, and values as the ship (object).
        
        Exceptions Raised:
          ValueError: for when coordinates are not entered; or option number is not entered, correctly as prompted.
          KeyError: for when entered coordinates are out of range.
          IndexError: for when coordinates are not entered; or option number is not entered, correctly as prompted.
          BusyCoordinateException: for when there is already a ship at a chosen coordinate.
          NotEnoughRoomException: for when there is no enough room for a ship to be placed at a chosen coordinate.
        """
        fleet = {}
        for ship_type in Ship.types.keys():
            error_str = obj_str.error_str
            while True:
                try:
                    ship = Ship(self.gen_coords(ship_type), ship_type, self)
                    break
                except ValueError:
                    print(error_str.format(obj_str.value_error_str))
                except KeyError:
                    print(error_str.format(obj_str.key_error_str))
                except IndexError:
                    print(error_str.format(obj_str.index_error_str))
                except BusyCoordinateException:
                    print(error_str.format(obj_str.busy_coord_error_str))
                except NotEnoughRoomException:
                    print(error_str.format(obj_str.not_enough_room_error_str))
            fleet[ship_type] = ship
        return fleet

class ComputerBattlefield(Battlefield):
    """ Subclasses parent in order to override ship placement funcitonality, replacing user input with random input, as well as battlefiled display\
         - to hide computer ships."""

    def gen_coords(self, ship_type):
        """Generate coordinates for a given ship type, using random input. **(Overrides parent class)**.

        Args:
          ship_type (str): name of the type of ship/
        Returns:
          sorted list of valid coordinates of a ship of the provided type, starting on a randomly generated coordinate\
              and placed in a random direction.
        Exceptions Raised:
          BusyCoordinateException: when randomly chosen coordinate already contains a ship
          NotEnoughRoomException: when there is no room for any ship starting at a randomly chosen coordinate
        """
        coordinates = []
        
        #Randomly generate starting cooriundate. Raise exception if a ship already exist at randomly chosen coordinate
        start_coordinate = (self.rows[random.randint(0, len(self.rows)-1)], random.randint(1, len(self.columns)))
        if self.grid[start_coordinate] == Battlefield.states[5]:
            raise BusyCoordinateException
        coordinates.append(start_coordinate)
        
        #Obtain valid options for ship placement from starting coordinate. Raise exception if there is not enough room for any ship.
        options = list(self.coord_opts(start_coordinate, ship_type).values())
        if not options:
            raise NotEnoughRoomException
        
        #Add the rest of the coordinates (except for starting) from the chosen option to a list & return sorted list
        for coord in options[random.randint(0, len(options)-1)][1:]:
            coordinates.append(coord)
        coordinates.sort()
        return coordinates

    def display(self):
        """Display Battlefield to the terminal based on data contained in grid, except for non-hit ship coordinates\
            which are to remain hidden. **(Overrides parent class)**."""
        print("   " + "  ".join([str(column) for column in self.columns]))
        for row_name in self.rows:
            row = []
            for key in self.grid.keys():
                if key[0] == row_name:
                    if not self.grid[key]:
                        row.append("[ ]")
                    elif self.grid[key]==Battlefield.states[1]:
                        row.append("[ ]")
                    elif self.grid[key]==Battlefield.states[2]:
                        row.append("[ ]")
                    elif self.grid[key]==Battlefield.states[3]:
                        row.append("[ ]")
                    elif self.grid[key]==Battlefield.states[4]:
                        row.append("[ ]")
                    elif self.grid[key]==Battlefield.states[5]:
                        row.append("[ ]")
                    elif self.grid[key]==Battlefield.states[6]:
                        row.append("[o]")
                    elif self.grid[key]==Battlefield.states[7]:
                        row.append("[X]")
                    elif self.grid[key]==Battlefield.states[8]:
                        row.append("[ ]")
                    elif self.grid[key]==Battlefield.states[9]:
                        row.append("[#]")                    
            print(row_name + " " + "".join(row))

    def generate_ships(self):
        """Call coordinate generator for each ship, check if coordinates are valid, and place ship on the player's Battlefield.\
            **(Overrides parent class)**.

        The reason for overriding parent class is to remove print statements during exception handling, and 
        to remove ValueError, KeyError, and IndexError from exception handling. 
        
        Returns:
          Fleet (dict): with keys as names of ship type, and values as the ship (object).
        
        Exceptions Raised:
          BusyCoordinateException: for when there is already a ship at a chosen coordinate.
          NotEnoughRoomException: for when there is no enough room for a ship to be placed at a chosen coordinate.
        """
        fleet = {}
        for ship_type in Ship.types.keys():
            error_str = obj_str.error_str
            while True:
                try:
                    ship = Ship(self.gen_coords(ship_type), ship_type, self)
                    break
                except BusyCoordinateException as a:
                    pass
                except NotEnoughRoomException as b:
                    pass
            fleet[ship_type] = ship
        return fleet

class Ship:
    """contains data structure(s) relating to each ship, including its coordinates, it's name/type, and it's health status.

    Class variables:
      types (dict): contains names of ship types as keys, and sizes for each ship as values.
    Instance Variables:
      coordinates (list): the coordinates of the ship.
      type (str): the name of the ship type, from the list of ship types.
      battlefield (object): a Battlefiled class bject - the Battlefiled to which the ship has been added.
      size (int): the number of coordinates that a ship occupipes on the Battlefiled grid.
      sunk (bool): whether all of the ship's coordinates have been hit.
    Methods:
      __init__, __repr__, check_sunk
    """

    types = {"Carrier": 5, "Battleship": 4, "Destroyer": 3, "Submarine": 3,\
         "Patrol Boat": 2}
    
    def __init__(self, coordinates, type, battlefield):
        """initialize an instance of a Ship.
        
        Args:
          coordinates (list): the coordinates of the ship (where the ship will be placed on a Battlefield)
          type (str): the name of the ship type, from the list of ship types.
          battlefield (object): a Battlefiled class bject - the Battlefiled to which the ship will be added.
        """
        self.coordinates = coordinates
        self.type = type
        self.battlefield = battlefield
        self.size = Ship.types[self.type]
        self.sunk = False
        for coordinate in self.coordinates:
            self.battlefield.grid[coordinate] = Battlefield.states[5]

    def __repr__(self):
        """String representation of Ship containing it's type and coordinates"""
        return "Type " + str(self.type) + ". Coordinates: " + str(self.coordinates)

    def check_sunk(self):
        """Check if the ship has sunk (if all of the ship's coordinates have been hit.
        
        If the ship has sunk, a stetement identifyuing the sunk ship is printed.
        """
        hit_coordinates = 0
        battlefield = self.battlefield
        for coordinate in self.coordinates:
            if battlefield.grid[coordinate] == battlefield.states[7]:
                hit_coordinates += 1
        if hit_coordinates == self.size:
            self.sunk = True
            for coordinate in self.coordinates:
                battlefield.grid[coordinate] = Battlefield.states[9]
            print(NL*2 + line_wrap3(self.type + " HAS BEEN SUNK!!!!") + NL*2)

class Player:
    player_count = 0

    def __init__(self):
        Player.player_count += 1
        self.id = Player.player_count
        self.battlefield = Battlefield(10, 10)
        self.fleet = self.battlefield.generate_ships()
        self.fleet_sunk = False
        # self.targetted_coordinates = []
        # self.hit_coordinates = []
        # self.active_targets = []

    def __repr__(self):
        return "Player" + str(self.id)
    
    def check_fleet_sunk(self):
        sunk_ships = 0
        for ship in self.fleet.values():
            if ship.sunk:
                sunk_ships += 1
        if sunk_ships == len(self.fleet):
            self.fleet_sunk = True
        return self.fleet_sunk
    
    def display_ships(self):
        if self.id == 1:
            player_str = "YOUR"
        elif self.id == 2:
            player_str = "ENEMY"
        ships = [ship for ship in self.fleet.values() if not ship.sunk]
        print(NL + line_str1 + NL)
        print(obj_str.display_ships_intro.format(player_str))
        num = 1
        for ship in ships:
            print(obj_str.display_ships_str_main.format(num, ship.type, "+"*ship.size), end="\n")
            num += 1
        print(NL)

    def target(self, player):

        shot = 0
        last_shot_hit = False
        while shot < 1 or last_shot_hit:
            battlefield = player.battlefield
            grid = player.battlefield.grid
            while True:
                player.display_ships()
                input(continue_str)
                battlefield.display_wrapped("Enemy")
                error_str = obj_str.error_str
                try:
                    input1 = (input(obj_str.target_cords_str))
                    coordinate = (input1[0].upper(), int(input1[1:]))
                    if grid[coordinate] == Battlefield.states[6] or grid[coordinate] == Battlefield.states[7]\
                        or grid[coordinate] == Battlefield.states[9]:
                        raise TargettedCoordinateException
                    break
                except ValueError:
                    print(error_str.format(obj_str.value_error_str))
                except KeyError:
                    print(error_str.format(obj_str.key_error_str))
                except IndexError:
                    print(error_str.format(obj_str.index_error_str))
                except TargettedCoordinateException:
                    print(error_str.format(obj_str.targetted_coord_error_str))
            if not grid[coordinate]:
                grid[coordinate] = Battlefield.states[6]
                print(NL*2 + obj_str.target_complete + NL)
                battlefield.display()
                print(NL*2 + obj_str.empty_waters_str.format(str(coordinate)) + NL*2)
                shot += 1
                last_shot_hit = False
            elif grid[coordinate] == Battlefield.states[5]:
                grid[coordinate] = Battlefield.states[7]
                print(NL*2 + obj_str.target_complete + NL)
                battlefield.display()
                print(NL*2 + line_wrap3(obj_str.ship_hit_str.format(str(coordinate))) + NL*2)
                last_shot_hit = True
                shot += 1
                for ship in player.fleet.values():
                    if coordinate in ship.coordinates:
                        ship.check_sunk()
                if player.check_fleet_sunk():
                    break
                input(continue_str)
                print(line_str2 + NL*2 + target_str)
                input(continue_str)

class Computer(Player):
    def __init__(self):
        Player.player_count += 1
        self.id = Player.player_count
        self.battlefield = ComputerBattlefield(10, 10)
        self.fleet = self.battlefield.generate_ships()
        self.fleet_sunk = False
        self.targetted_coordinates = []
        self.hit_coordinates = []
        self.active_targets = []

    def __repr__(self):
        return "Computer"
    
    def smart_targetting_1(self, coordinate, player):
        battlefield = player.battlefield
        options = []                 
        coord_down = battlefield.coord_down                                    
        coord_right = battlefield.coord_right
        row_index = battlefield.row_index
        row = battlefield.get_row(coordinate)
        column = battlefield.get_column(coordinate)
        targets_in_row = [target for target in self.active_targets if target in row]
        targets_in_column = [target for target in self.active_targets if target in column]
        largest_ship_size = 0
        for ship in self.fleet.values():
            if not ship.sunk:
                if ship.size >= largest_ship_size:
                    largest_ship_size = ship.size
        if len(targets_in_row) > 1:
            target_columns = [target[-1] for target in targets_in_row]
            target_columns.sort()
            if target_columns.index(coordinate[-1]) < len(target_columns) - 1:
                row_options = []
                current_coord = coordinate
                index_difference = target_columns[target_columns.index(coordinate[-1]) + 1] - \
                    target_columns[target_columns.index(coordinate[-1])]
                seperation = index_difference - 1
                if (largest_ship_size - 2) >= seperation >= 1:
                    for num in range(seperation):
                        next_coord = coord_right(current_coord)
                        if next_coord in self.targetted_coordinates and next_coord not in self.hit_coordinates:
                            row_options = None
                            break
                        elif next_coord not in self.targetted_coordinates:
                            row_options.append(next_coord)
                        current_coord = next_coord
                    options.extend([option for option in row_options if option not in options])    
        if len(targets_in_column) > 1:
            target_row_indices = [row_index(target) for target in targets_in_column]
            target_row_indices.sort()
            if target_row_indices.index(row_index(coordinate[0])) < len(target_row_indices) - 1:
                column_options = []
                current_coord = coordinate
                index_difference = target_row_indices[target_row_indices.index(row_index(coordinate[0])) + 1] - \
                    target_row_indices[target_row_indices.index(row_index(coordinate[0]))]
                seperation = index_difference - 1
                if (largest_ship_size - 2) >= seperation >= 1:
                    for num in range(seperation):
                        next_coord = coord_down(current_coord)
                        if next_coord in self.targetted_coordinates and next_coord not in self.hit_coordinates:
                            column_options = None
                            break
                        elif next_coord not in self.targetted_coordinates:
                            column_options.append(next_coord)
                        current_coord = next_coord
                    options.extend([option for option in column_options if option not in options])
        return options
    
    def adjascent_targets(self, direction_func, coord, player):
        battlefield = player.battlefield
        options = []
        coord_up = battlefield.coord_up                    
        coord_down = battlefield.coord_down                   
        coord_left = battlefield.coord_left                   
        coord_right = battlefield.coord_right
        row_index = battlefield.row_index
        if direction_func == coord_up:
            range_value = row_index(coord)
        elif direction_func == coord_down:
            range_value = len(battlefield.rows) - row_index(coord)
        elif direction_func == coord_left:
            range_value = coord[-1]
        elif direction_func == coord_right:
            range_value = len(battlefield.columns) - coord[-1]
        current_coord = coord
        if direction_func(coord) and direction_func(coord) in self.hit_coordinates:
            for num in range(range_value):
                next_coord = direction_func(current_coord)
                if next_coord in self.targetted_coordinates and next_coord not in self.hit_coordinates:
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
                options.extend(self.smart_targetting_1(coordinate, player))
            if options:
                target_options.extend([option for option in options if option not in target_options])
                return target_options
            else:
                for coordinate in self.active_targets:   
                    if coord_up(coordinate):
                        options.extend(self.adjascent_targets(coord_up, coordinate, player))
                    if coord_down(coordinate):
                        options.extend(self.adjascent_targets(coord_down, coordinate, player))
                    if coord_left(coordinate):
                        options.extend(self.adjascent_targets(coord_left, coordinate, player))
                    if coord_right(coordinate):
                        options.extend(self.adjascent_targets(coord_right, coordinate, player))
                if options:
                    target_options.extend([option for option in options if option not in target_options])
                    return target_options
                else:    
                    for coordinate in self.active_targets:
                        if coord_up(coordinate):
                            if coord_up(coordinate) not in self.targetted_coordinates and coord_up not in target_options:
                                options.append(coord_up(coordinate))
                        if coord_down(coordinate):
                            if coord_down(coordinate) not in self.targetted_coordinates and coord_down not in target_options:
                                options.append(coord_down(coordinate))
                        if coord_left(coordinate):
                            if coord_left(coordinate) not in self.targetted_coordinates and coord_left not in target_options:
                                options.append(coord_left(coordinate))
                        if coord_right(coordinate):
                            if coord_right(coordinate) not in self.targetted_coordinates and coord_right not in target_options:
                                options.append(coord_right(coordinate))
                    target_options.extend([option for option in options if option not in target_options])
                    return target_options
        else:
            available_targets = [coordinate for coordinate in battlefield.coordinates if not battlefield.grid[coordinate]\
                 or battlefield.grid[coordinate] == Battlefield.states[5]]  
            options = []
            options_preferred_A = []
            options_preferred_B = []
            options_preferred_C = []
            options_preferred_D = []
            options_preferred_E = []
            options_preferred_F = []
            options_preferred_G = []
            preferred_lists_temp_1 = [options_preferred_A, options_preferred_B, options_preferred_C, options_preferred_D,\
                 options_preferred_E, options_preferred_F, options_preferred_G]
            preferred_lists_temp_2 = [options_preferred_A, options_preferred_B, options_preferred_C, options_preferred_D]
            for coordinate in available_targets:
                for ship in player.fleet.values():
                    if not ship.sunk:
                        if ship.size <= battlefield.horizontal_target_size(coordinate, self.targetted_coordinates)\
                             or ship.size <= battlefield.vertical_target_size(coordinate, self.targetted_coordinates):
                            if coordinate not in options:
                                options.append(coordinate)
            for option in options:
                up_2x = (coord_up(option) and coord_up(option) in available_targets)\
                    and (coord_up(coord_up(option)) and coord_up(coord_up(option)) in available_targets)
                
                down_2x = (coord_down(option) and coord_down(option) in available_targets)\
                    and (coord_down(coord_down(option)) and coord_down(coord_down(option)) in available_targets)
                
                left_2x = (coord_left(option) and coord_left(option) in available_targets)\
                    and (coord_left(coord_left(option)) and coord_left(coord_left(option)) in available_targets)
                
                right_2x = (coord_right(option) and coord_right(option) in available_targets)\
                    and (coord_right(coord_right(option)) and coord_right(coord_right(option)) in available_targets)
                
                up_1x = (coord_up(option) and coord_up(option) in available_targets)
                down_1x = (coord_down(option) and coord_down(option) in available_targets)
                left_1x = (coord_left(option) and coord_left(option) in available_targets)
                right_1x = (coord_right(option) and coord_right(option) in available_targets)
                
                A = (up_2x and down_2x and left_2x and right_2x)
                B = (up_2x and down_2x and left_1x and right_1x) or (up_1x and down_1x and left_2x and right_2x)
                C = (up_1x and down_1x and left_1x and right_1x)
                D = (up_2x and down_2x and (left_1x or right_1x)) or ((up_1x or down_1x) and left_2x and right_2x)
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
                    target_options.extend([option for option in preferred_lists_1[0] if option not in target_options])
                else:
                    target_options.extend([option for option in preferred_lists_2[random.randint(0, len(preferred_lists_2) - 1)] if option not in target_options])
                return target_options
            else:
                target_options.extend([option for option in options if option not in target_options])
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
                            coordinate = options[random.randint(0, len(options)-1)]
                    else:
                        coordinate = (rows[random.randint(0, len(rows)-1)], random.randint(1, len(columns)))
                    if grid[coordinate] == Battlefield.states[6] or grid[coordinate] == Battlefield.states[7]\
                        or grid[coordinate] == Battlefield.states[9]:
                            raise TargettedCoordinateException
                    break
                except Exception as e:
                    pass
            self.targetted_coordinates.append(coordinate)
            if not grid[coordinate]:
                grid[coordinate] = Battlefield.states[6]
                print(NL*2 + obj_str.incoming_complete + NL)
                battlefield.display()
                print(NL*2 + obj_str.empty_waters_str.format(str(coordinate)) + NL*2)
                shot += 1
                last_shot_hit = False
            elif grid[coordinate] == Battlefield.states[5]:
                grid[coordinate] = Battlefield.states[7]
                print(NL*2 + obj_str.incoming_complete + NL)
                battlefield.display()
                print(NL*2 + line_wrap3(obj_str.ship_hit_str.format(str(coordinate))) + NL*2)
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
                print(line_str2 + NL*2 + incoming_str)
                input(continue_str)

class InputException(Exception):
    """
    For Bad Inputs
    """     

class BusyCoordinateException(InputException):
    """
    For Bad coordinate inputs when input coordinate already contains Ship
    """ 

class TargettedCoordinateException(InputException):
    """
    For Bad coordinate inputs when input coordinate has already been targetted
    """ 

class NotEnoughRoomException(Exception):
    """
    For Bad coordinate inputs when input coordinate does not allow enough room for given ship
    """ 