"""
Battlefield Module. Contains the main data and display elements of the game.
 
The Battlefield class contains the main data structure(s) for players' 
  "Battlefield" (coordinate system and ship positions); various helper functions
  for accesing and processing the data, and display (to Terminal) functionality.
The ComputerBattlefield subclass of Battlefield class overrides the display 
  functionality of the parent class (to hide computer ships).

"""

if __name__ == "__main__":
    import sys
    import os
    sys.path.append(os.path.join( os.path.dirname( __file__ ), '..' ))

import string
from Elements.Battlefield_Strings.Battlefield_Strings import\
    NL, Formatting, DisplayStrings

class Battlefield:
    """Serves as each player's individual "Battlefield"
    
    Uses a grid coordinate system, and tracking each coordinate's status (empty,
    untargetted ("healthy") ship, targetted & missed, targetted and hit ship). 
    
    Includes functionality for displaying battlefiled to terminal and providing
    a muiltitude of helper funcitons that assist with the coordinate system, from 
    generating coordinate options for ship placement (based on input from either 
    Player or Computer classes) to checking maximum clearance size of a given 
    coordinate for evaluation as a valid target for smart targetting funcitonality 
    of the Computer class.

    Subclassed by ComputerBattlefield, which overrides the display funcitonality,
    so as not to display the computer's ships to the user (player1) 
    when otherwise displaying the computer's battlefiled.

    Class variables:
      states (list): possible statuses ("states") for coordinates in grid
    Instance Variables:
      rows (list): alphabetical rows the Battlefield instance is comprised of 
      columns (list): columns the Battlefield instance is comprised of.
      coordinates (list): coordinates the Battlefield instance is comprised of.
      grid (dict): containings coordinates of the Battlefield as keys, each 
        coordinate indicating it's status (i.e. empty, hit, etc.) as values.
        states (list): list containing possible statuses for any given coordinate.
        Whenever the state of a given coordinate needs to be accessed or
        overwrittene by a new state, it is accessed via the list, 
        instead of being referenced explicitly.
    Methods:
      __init__, display, display_wrapped, coord_to_str, row_index, get_row,
      get_column, coord_up, coord_down, coord_left, coord_right, get_range_value,
      coord_opts_direction, next_targetted_coord, horizontal_target_size, 
      vertical_target_size, coord_opts
    """
    
    states = [None, 1, 2, 3, 4, "healthy", "targetted", "hit", "*", "#"]
        #List of possible states for coordinates in grid
        #Numbers 1-4 and star symbol (*) are used temporarily for interactive
        #  ship generation prompt.
        #Hashtag symbol (#) is used for sunk ship coordinates.

    def __init__(self, num_rows, num_columns):
        """initialize an instance of a Battlefield.
        
        Args:
          num_rows (int): For the Battlefield's grid coordinate system.
          num_columns (int):  For the Battlefield's grid coordinate system.
        """
        self.rows = [row for row in string.ascii_uppercase[:num_rows]]
        self.columns = [column for column in range(1, num_columns+1)]
        self.coordinates = []
        for row in self.rows:
            for column in self.columns:
                self.coordinates.append((row, column))
        self.grid = {coordinate: None for coordinate in self.coordinates}

    def display(self):
        """Display Battlefield to the terminal based on data contained in grid.\
             **(Overridden by ComputerBattlefiled subclass)**."""
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
        """Add visual formatting to display of the Battlefield\
             (using seperator strings form strings module)."""
        print(Formatting.line_str1)
        print(NL)
        print(DisplayStrings.battlefield_str.format(string))
        print(NL)
        self.display()
        print(NL)
    
    @staticmethod
    def coord_to_str(coordinate):
        """Convert the provided coordinate (tuple) into a string."""
        return str(coordinate[0]) + str(coordinate[-1])
    
    def row_index(self, coordinate):
        """Return the index, in the rows list, of the row the provided\
             coordinate belongs to"""
        return self.rows.index(coordinate[0])

    def get_row(self, coordinate):
        """Return a list containing all the coordinates from the row that the\
             provided coordinate belongs to."""
        row = []
        for column in self.columns:
            row.append((coordinate[0], column))
        return row

    def get_column(self, coordinate):
        """Return a list containing all the coordinates from the column that\
             the provided coordinate belongs to."""
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

    def get_range_value(self, direction_func, coordinate):
        """Return measure of length until the border of the Battlefield\
             in a given direction toe be used as a range value.
                 
        Args:
          direction_func (function): one of coord_up/down/left/right "direction"
            helper methods.
          coordinate (tuple): a coordinate.
        Returns:
          Value (int) representing length (range) until the bortder of the
            Battlefiled.
        """
        
        if direction_func == self.coord_up:
            range_value = self.row_index(coordinate)
        elif direction_func == self.coord_down:
            range_value = len(self.rows) - self.row_index(coordinate)
        elif direction_func == self.coord_left:
            range_value = coordinate[-1]
        elif direction_func == self.coord_right:
            range_value = len(self.columns) - coordinate[-1]
        return range_value
    
    def coord_opts_direction(self, coordinate, ship_size, direction_func):
        """Return a list of coordinates of a ship of given size in a given\
             direction, starting at given coordinate.
        
        Args:
          coordinate (tuple): (a coordinate).
          ship_size (int): representing number of coordinates the ship occupies.
          direction_func: one of coord_up/down/left/right "direction"
             helper methods.
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
        """Find next coordinate on the grid, in a given direction, that has\
             already been targetted (either hit or missed). 

        Args:
          direction_func (function): one of coord_up/down/left/right 
            "direction" helper methods.
          coord (tuple): a coordinate.
          targetted_coordinates (list): a list of targetted coordinates
            (either hit or missed).
        Returns:
          The next coordinate (tuple), if any.
        """
        range_value = self.get_range_value(direction_func, coord)
        current_coord = coord
        if direction_func(coord) and \
            direction_func(coord) not in targetted_coordinates:
            for num in range(range_value):
                next_coord = direction_func(current_coord)
                if next_coord in targetted_coordinates:
                    return next_coord
                elif next_coord:
                    current_coord = next_coord
    
    def horizontal_target_size(self, coord, targetted_coordinates):
        """Calculate maximum availble horizontal non-targetted space around a\
             given coordinate (to determine if it is big enouth to hide a ship).

        Args:
          coord (tuple): a coordinate.
          targetted_coordinates (list): a list of targetted coordinates
            (either hit or missed).
        Returns:
          the linear horizontal size (int) of adjascent available
             (non-targetted) space around the coordinate. 
        """              
        coord_left = self.coord_left                   
        coord_right = self.coord_right
        left_border = \
            self.next_targetted_coord(coord_left, coord, targetted_coordinates)
        right_border = \
            self.next_targetted_coord(coord_right, coord, targetted_coordinates)
        
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
        """Calculate maximum availble vertical non-targetted space around a\
             given coordinate (to determine if it is big enouth to hide a ship).

        Args:
          coord (tuple): a coordinate.
          targetted_coordinates (list): a list of targetted coordinates
            (either hit or missed).
        Returns:
          the linear vertical size (int) of adjascent available (non-targetted)
            space around the coordinate. 
        """ 
        coord_up = self.coord_up                    
        coord_down = self.coord_down                   
        row_index = self.row_index
        top_border = \
            self.next_targetted_coord(coord_up, coord, targetted_coordinates)
        bottom_border = \
            self.next_targetted_coord(coord_down, coord, targetted_coordinates)
        
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
        """Return coordinate options for a ship placed starting at provcided\
             coordinate, in all four directions.

        Args:
          coordinate (tuple): a Coordinate
          ship_type (str): name of the type of ship
        Returns:
          a dictionary with keys identifying direction, and values as a list of
            coordinates of a ship placed in that directrion from the provided
            coordinate as a starting point, given there is enouth space.
        """
        from Elements.Ship import Ship
        ship_size = Ship.types[ship_type]
        options = \
            {"Up: ": None, "Down: ": None, "Left: ": None, "Right: ": None, }
        
        #In each direction (up/down/leftr/right), if a ship of a given size
        #  can fit, return coordinates for that option (direction).
        if self.row_index(coordinate) - (ship_size - 1) >= 0:
            options["Up: "] = \
                self.coord_opts_direction(coordinate, ship_size, self.coord_up)

        if self.row_index(coordinate) + (ship_size - 1) < len(self.rows):
            options["Down: "] = \
                self.coord_opts_direction(coordinate, ship_size, self.coord_down)

        if (coordinate[-1]) - (ship_size - 1) >= 1:
            options["Left: "] = \
                self.coord_opts_direction(coordinate, ship_size, self.coord_left)

        if (coordinate[-1]) + (ship_size - 1) <= len(self.columns):
            options["Right: "] = \
                self.coord_opts_direction(coordinate, ship_size, self.coord_right)

        return {key: value for (key, value) in options.items() if value != None}
    
class ComputerBattlefield(Battlefield):
    """ Subclasses parent in order to override battlefiled display, 
      hiding computer ships fomr the user.
         
    Methods:
      display (overrides parent)
    """
    def display(self):
        """Display Battlefield to the terminal based on data contained in grid,\
             except for non-hit ship coordinates which are to remain hidden. \
                 **(Overrides parent class)**."""
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
