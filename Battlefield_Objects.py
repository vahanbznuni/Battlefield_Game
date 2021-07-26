import string
import random

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

    def generate_ships(self):
        fleet = {}
        for ship_type in Ship.types.keys():
            error_str = "\n" + "\n" + "INCORRECT INPUT! \n{} Please try again!"
            while True:
                try:
                    ship = Ship(self.gen_coords(ship_type), ship_type, self)
                    break
                except ValueError:
                    print(error_str.format(\
                        """Make sure to enter exact coordinates (for starting coordinate) \nor exact choice number (for ending coordinate)."""))
                except KeyError:
                    print(error_str.format("Make sure your coordinates are in range!"))
                except BusyCoordinateException:
                    print(error_str.format("There is already a ship in that location!!"))
            fleet[ship_type] = ship
        return fleet

    def target(self, coordinate):
        if self.grid[coordinate] == Battlefield.states[6] or self.grid[coordinate] == Battlefield.states[7]:
            raise BusyCoordinateException
        else:
            if not self.grid[coordinate]:
                self.grid[coordinate] = Battlefield.states[6]
                self.display()
                print("\n\nEmpty waters hit. No ships at target.\n\n")
            elif self.grid[coordinate] == Battlefield.states[5]:
                self.grid[coordinate] = Battlefield.states[7]
                self.display()
                print("\n\nShip hit at target!")

class ComputerBattlefield(Battlefield):
    def gen_coords(self, ship_type):
        coordinates = []
        start_coordinate = (self.rows[random.randint(0, len(self.rows)-1)], random.randint(0, 10))
        coordinates.append(start_coordinate)
        options = list(self.coord_opts(start_coordinate, ship_type).values())
        for coord in options[random.randint(0, len(options)-1)][1:]:
            coordinates.append(coord)
        coordinates.sort()
        return coordinates

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

    def __repr__(self):
        return "Type " + str(self.type) + ". Coordinates: " + str(self.coordinates)

    def check_sunk(self):
        hit_coordinates = 0
        battlefield = self.battlefield
        for coordinate in self.coordinates:
            if battlefield[coordinate] == battlefield.states[8]:
                hit_coordinates += 1
        if hit_coordinates == self.size:
            self.ship_sunk = True
            print(self.type + " has been sunk!")
   
class Player:
    player_count = 0

    def __init__(self):
        Player.player_count += 1
        self.id = Player.player_count
        self.battlefield = Battlefield(10, 10)
        self.fleet = self.battlefield.generate_ships()
        self.fleet_sunk = False
        self.list_targetted_coordinates = []

    def check_fleet_sunk(self):
        sunk_ships = 0
        for ship in self.fleet.values():
            if ship.check_sunk():
                sunk_ships += 1
        if sunk_ships == len(self.fleet):
            self.fleet_sunk = True

class Computer(Player):
    def __init__(self):
        Player.player_count += 1
        self.id = Player.player_count
        self.battlefield = ComputerBattlefield(10, 10)
        self.fleet = self.battlefield.generate_ships()
        self.list_targetted_coordinates = []

class InputException(Exception):
    """
    For Bad Inputs
    """     

class BusyCoordinateException(InputException):
    """
    For Bad coordinate inputs when input coordinate already contains Ship; or was already targetted
    """ 

#=================================================================================================================
#Test_Zone:
# test_player_Computer = Computer()
# test_player_Computer.battlefield.display()
# print("\n")
# test_player_Computer.battlefield.target(("G",7))

# test_battlefield = Battlefield(10, 10)
# print((test_battlefield.rows[random.randint(0, 10)], random.randint(0, 10)))

#=================================================================================================================