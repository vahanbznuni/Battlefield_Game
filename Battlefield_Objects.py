import string

class Battlefield:
    states = [None, 1, 2, 3, 4, "healthy", "targetted", "hit", "*"]

    def __init__(self, num_rows, num_columns):
        self.rows = [row for row in string.ascii_uppercase[:num_rows]]
        self.columns = [column for column in range(1, num_columns+1)]
        self.coordinates = []
        for row in self.rows:
            for column in self.columns:
                self.coordinates.append((row, column))
        self.grid = {coordinate: None for coordinate in self.coordinates}

    def display(self):
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
            print(row_name + " " + "".join(row))

    @staticmethod
    def coord_to_str(coordinate):
        return str(coordinate[0]) + str(coordinate[-1])
    
    def row_index(self, coordinate):
        return self.rows.index(coordinate[0])

    def coord_up(self, coordinate):
        return (self.rows[self.row_index(coordinate) - 1], coordinate[-1])

    def coord_down(self, coordinate):
        return (self.rows[self.row_index(coordinate) + 1], coordinate[-1])

    def coord_left(self, coordinate):
        return (coordinate[0], coordinate[-1] - 1)

    def coord_right(self, coordinate):
        return (coordinate[0], coordinate[-1] + 1)

    def coord_opts(self, coordinate, ship_type):
        ship_size = Ship.types[ship_type]
        options = {"Up: ": None, "Down: ": None, "Left: ": None, "Right: ": None, }
        if self.row_index(coordinate) - (ship_size - 1) >= 0:
            up_coords = [coordinate]
            current_coord = coordinate
            for num in range(ship_size - 1):
                next_coord = self.coord_up(current_coord)
                if self.grid[next_coord] == Battlefield.states[5]:
                    up_coords = None
                    break
                up_coords.append(next_coord)
                current_coord = next_coord
            options["Up: "] = up_coords
        if self.row_index(coordinate) + (ship_size - 1) < len(self.rows):
            down_coords = [coordinate]
            current_coord = coordinate
            for num in range(ship_size - 1):
                next_coord = self.coord_down(current_coord)
                if self.grid[next_coord] == Battlefield.states[5]:
                    down_coords = None
                    break
                down_coords.append(next_coord)
                current_coord = next_coord
            options["Down: "] = down_coords
        if (coordinate[-1]) - (ship_size - 1) >= 1:
            left_coords = [coordinate]
            current_coord = coordinate
            for num in range(ship_size - 1):
                next_coord = self.coord_left(current_coord)
                if self.grid[next_coord] == Battlefield.states[5]:
                    left_coords = None
                    break
                left_coords.append(next_coord)
                current_coord = next_coord
            options["Left: "] = left_coords
        if (coordinate[-1]) + (ship_size - 1) <= len(self.columns):
            right_coords = [coordinate]
            current_coord = coordinate
            for num in range(ship_size - 1):
                next_coord = self.coord_right(current_coord)
                if self.grid[next_coord] == Battlefield.states[5]:
                    right_coords = None
                    break
                right_coords.append(next_coord)
                current_coord = next_coord
            options["Right: "] = right_coords
        return {key: value for (key, value) in options.items() if value != None}
    
    def gen_coords(self, ship_type):
        print("\n")
        self.display()
        print("\n")
        ship_size = Ship.types[ship_type]
        coordinates = []
        input_str = "Please enter {0} coordinate for the position of {1} ({2}): "
        input1 = input(input_str.format("starting", str(ship_type), ship_size*"+"))
        start_coordinate = (input1[0], int(input1[1:]))
        if self.grid[start_coordinate] == Battlefield.states[5]:
            raise BusyCoordinateException
        else:
            coordinates.append(start_coordinate)
            print("\n")
            copy_grid = self.grid.copy()
            self.grid[start_coordinate] = "*"
            input_str_last = input_str.format("ending", str(ship_type), ship_size*"+").replace("enter", "choose").replace(":", ".") + "\n" +\
                "Enter the *NUMBER* corresponding to the coordinates option of your choice : " + "\n" + "\n"
            options = self.coord_opts(start_coordinate, ship_type)
            num = 1
            for key in options.keys():
                last_coord = options[key][-1]
                input_str_last += str(num) + " ({}): ".format(key[:-2]) + Battlefield.coord_to_str(last_coord) +"\n"
                self.grid[last_coord] = num
                num += 1
            self.display()
            print("\n")
            input2 = input(input_str_last)
            for coord in list(options.values())[int(input2) - 1][1:]:
                coordinates.append(coord)
            coordinates.sort()
            self.grid.update(copy_grid)
            return coordinates

    #========================================================================================================================
    #[!] NEEDS REVISION | must return consecutive coortdinates.

    # def get_random_coords(self, ship_type):
    #     ship_size = Ship.types[ship_type]
    #     coords = []
    #     import random
    #     for num in range(ship_size):
    #         coords.append((self.rows[random.randint(0, 10)], str(random.randint(0, 10))))
    #     return coords
    
    #========================================================================================================================

    def generate_ships(self):
        fleet = {}
        for ship_type in Ship.types.keys():
            num = 1
            error_str = "\n" + "\n" + "INCORRECT INPUT! \n{} Please try again!"
            while True:
                try:
                    ship = Ship(self.gen_coords(ship_type), ship_type, self)
                    break
                except ValueError:
                    print(error_str.format(\
                        """Make sure to enter exact coordinates (for starting coordinate)
or exact choice number (for ending coordinate)."""))
                except KeyError:
                    print(error_str.format("Make sure your coordinates are in range!"))
                except BusyCoordinateException:
                    print(error_str.format("There is already a ship in that location!!"))
            ship_var = "ship" + str(num)
            fleet[ship_var] = ship
            num +=1
        return fleet

    def target(self, coordinates):
        if not self.grid[coordinates]:
            self.grid[coordinates] = Battlefield.states[2]
            self.display()
            print("Empty waters hit. No ships at target")
        elif self.grid[coordinates] == Battlefield.states[1]:
            self.grid[coordinates] = Battlefield.states[3]
            self.display()
            print("Ship hit at target!")

class Ship:
    types = {"Carrier": 5, "Battleship": 4, "Destroyer": 3, "Submarine": 3,\
         "Patrol Boat": 2}
    
    def __init__(self, coordinates, type, battlefield):
        self.coordinates = coordinates
        self.type = type
        self.battlefield = battlefield
        self.size = Ship.types[self.type]
        self.ship_sunk = False
        for coordinate in self.coordinates:
            self.battlefield.grid[coordinate] = Battlefield.states[5] 
   
class Player:
    player_count = 0

    def __init__(self):
        Player.player_count += 1
        self.id = Player.player_count
        self.battlefield = Battlefield(10, 10)
        self.fleet = self.battlefield.generate_ships()
        self.list_targetted_coordinates = []

class InputException(Exception):
    """
    For Bad Inputs
    """     

class BusyCoordinateException(InputException):
    """
    For Bad coordinate inputs for placing ships where coordinate already contains ship
    """ 

#=================================================================================================================
#Test_Zone:
test_player = Player()
test_player.battlefield.display()

#=================================================================================================================