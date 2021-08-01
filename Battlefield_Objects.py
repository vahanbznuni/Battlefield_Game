import string
from Battlefield_Strings import line_str1, line_str2, NL, continue_str, line_wrap3, object_strings as obj_str, \
    battlefield_str, ready_str, target_str, incoming_str
import random

class Battlefield:
    states = [None, 1, 2, 3, 4, "healthy", "targetted", "hit", "*", "#"]

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
                    elif self.grid[key]==Battlefield.states[9]:
                        row.append("[#]")                      
            print(row_name + " " + "".join(row))
   
    def display_wrapped(self, string):
        print(line_str1)
        print(NL)
        print(battlefield_str.format(string))
        print(NL)
        self.display()
        print(NL)
    
    @staticmethod
    def coord_to_str(coordinate):
        return str(coordinate[0]) + str(coordinate[-1])
    
    def row_index(self, coordinate):
            return self.rows.index(coordinate[0])

    def get_row(self, coordinate):
        row = []
        for column in self.columns:
            row.append((coordinate[0], column))
        return row

    def get_column(self, coordinate):
        column = []
        for row in self.rows:
            column.append((row, coordinate[-1]))
        return column

    def coord_up(self, coordinate):
        if self.row_index(coordinate) - 1 >= 0:
            return (self.rows[self.row_index(coordinate) - 1], coordinate[-1])

    def coord_down(self, coordinate):
        if self.row_index(coordinate) + 1 < len(self.rows):
            return (self.rows[self.row_index(coordinate) + 1], coordinate[-1])

    def coord_left(self, coordinate):
        if (coordinate[-1]) - 1 >= 1:
            return (coordinate[0], coordinate[-1] - 1)

    def coord_right(self, coordinate):
        if (coordinate[-1]) + 1 <= len(self.columns):
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
        self.display_wrapped("Your")
        ship_size = Ship.types[ship_type]
        coordinates = []
        input_str = obj_str.gen_coords_input1_str
        input1 = input(input_str.format("starting", str(ship_type), ship_size*"+"))
        start_coordinate = (input1[0], int(input1[1:]))
        if self.grid[start_coordinate] == Battlefield.states[5]:
            raise BusyCoordinateException
        else:
            coordinates.append(start_coordinate)
            print(NL)
            copy_grid = self.grid.copy()
            self.grid[start_coordinate] = "*"
            input2_str_addon = obj_str.gen_coords_input2_str_addon
            input2_str = input_str.format("ending", str(ship_type), ship_size*"+").replace("enter", "choose").replace(":", ".") + "\n" +\
                input2_str_addon + NL*2
            options = self.coord_opts(start_coordinate, ship_type)
            if not options:
                self.grid.update(copy_grid)
                raise NotEnoughRoomException
            else:
                num = 1
                for key in options.keys():
                    last_coord = options[key][-1]
                    input2_str += str(num) + " ({}): ".format(key[:-2]) + Battlefield.coord_to_str(last_coord) +"\n"
                    self.grid[last_coord] = num
                    num += 1
                self.display()
                print(NL)
                input2 = input(input2_str)
                self.grid.update(copy_grid)
                for coord in list(options.values())[int(input2) - 1][1:]:
                    coordinates.append(coord)
                coordinates.sort()
                return coordinates

    # def input_coords(self, coordinate):
    #     error_str = obj_str.error_str
    #     while True:
    #         try:
    #             input_coord = coordinate
    #             break
    #         except ValueError:
    #             print(error_str.format(obj_str.value_error_str))
    #         except KeyError:
    #             print(error_str.format(obj_str.key_error_str))
    #         except BusyCoordinateException:
    #             print(error_str.format(obj_str.busy_coord_error_str))
    #         except NotEnoughRoomException:
    #             print(error_str.format(obj_str.not_enough_room_error_str))
    #         except TargettedCoordinateException:
    #             print(error_str.format(obj_str.targetted_coord_error_str))
    #     return input_coord
       
    def generate_ships(self):
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
    def gen_coords(self, ship_type):
        coordinates = []
        start_coordinate = (self.rows[random.randint(0, len(self.rows)-1)], random.randint(0, 10))
        coordinates.append(start_coordinate)
        options = list(self.coord_opts(start_coordinate, ship_type).values())
        for coord in options[random.randint(0, len(options)-1)][1:]:
            coordinates.append(coord)
        coordinates.sort()
        return coordinates

    def display(self):
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

class Ship:
    types = {"Carrier": 5, "Battleship": 4, "Destroyer": 3, "Submarine": 3,\
         "Patrol Boat": 2}
    
    def __init__(self, coordinates, type, battlefield):
        self.coordinates = coordinates
        self.type = type
        self.battlefield = battlefield
        self.size = Ship.types[self.type]
        self.sunk = False
        for coordinate in self.coordinates:
            self.battlefield.grid[coordinate] = Battlefield.states[5]

    def __repr__(self):
        return "Type " + str(self.type) + ". Coordinates: " + str(self.coordinates)

    def check_sunk(self):
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
            from Battlefiled_main import check_winner
            if check_winner():
                break
            battlefiled = player.battlefield
            grid = player.battlefield.grid
            while True:
                player.display_ships()
                input(continue_str)
                battlefiled.display_wrapped("Enemy")
                error_str = obj_str.error_str
                try:
                    input1 = (input(obj_str.target_cords_str))
                    coordinate = (input1[0], int(input1[1:]))
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
                battlefiled.display()
                print(NL*2 + obj_str.empty_waters_str.format(str(coordinate)) + NL*2)
                shot += 1
                last_shot_hit = False
            elif grid[coordinate] == Battlefield.states[5]:
                grid[coordinate] = Battlefield.states[7]
                print(NL*2 + obj_str.target_complete + NL)
                battlefiled.display()
                print(NL*2 + line_wrap3(obj_str.ship_hit_str.format(str(coordinate))) + NL*2)
                last_shot_hit = True
                shot += 1
                for ship in player.fleet.values():
                    ship.check_sunk()
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
    
    def target_options(self, player):
        battlefiled = player.battlefield
        target_options = []
        if self.active_targets:
            options = []
            for coordinate in self.active_targets:
                row = battlefiled.get_row(coordinate)
                column = battlefiled.get_column(coordinate)
                targets_in_row = [target for target in self.active_targets if target in row]
                targets_in_column = [target for target in self.active_targets if target in column]
                if len(targets_in_row) > 1:
                    target_columns = [target[-1] for target in targets_in_row]
                    target_columns.sort()
                    if target_columns.index(coordinate[-1]) < len(target_columns) - 1:
                        row_options = []
                        current_coord = coordinate
                        index_difference = target_columns[target_columns.index(coordinate[-1]) + 1] - \
                            target_columns[target_columns.index(coordinate[-1])]
                        seperation = index_difference - 1
                        if seperation >= 1:
                            for num in range(seperation):
                                next_coord = battlefiled.coord_right(current_coord)
                                if next_coord in self.targetted_coordinates and next_coord not in self.hit_coordinates:
                                    row_options = None
                                    break
                                elif next_coord not in self.targetted_coordinates:
                                    row_options.append(next_coord)
                                current_coord = next_coord
                            options.extend([option for option in row_options if option not in options])    
                if len(targets_in_column) > 1:
                    target_row_indices = [battlefiled.row_index(target) for target in targets_in_column]
                    target_row_indices.sort()
                    if target_row_indices.index(battlefiled.row_index(coordinate[0])) < len(target_row_indices) - 1:
                        column_options = []
                        current_coord = coordinate
                        index_difference = target_row_indices[target_row_indices.index(battlefiled.row_index(coordinate[0])) + 1] - \
                            target_row_indices[target_row_indices.index(battlefiled.row_index(coordinate[0]))]
                        seperation = index_difference - 1
                        if seperation >= 1:
                            for num in range(seperation):
                                next_coord = battlefiled.coord_down(current_coord)
                                if next_coord in self.targetted_coordinates and next_coord not in self.hit_coordinates:
                                    column_options = None
                                    break
                                elif next_coord not in self.targetted_coordinates:
                                    column_options.append(next_coord)
                                current_coord = next_coord
                            options.extend([option for option in column_options if option not in options])
            if options:
                target_options.extend([option for option in options if option not in target_options])
                return target_options
            else: 
                for coordinate in self.active_targets:
                    if battlefiled.coord_up(coordinate):
                        coord_up = battlefiled.coord_up(coordinate)
                    else:
                        coord_up = None
                    if battlefiled.coord_down(coordinate):
                        coord_down = battlefiled.coord_down(coordinate)
                    else:
                        coord_down = None
                    if battlefiled.coord_left(coordinate):
                        coord_left = battlefiled.coord_left(coordinate)
                    else:
                        coord_left = None
                    if battlefiled.coord_right(coordinate):
                        coord_right = battlefiled.coord_right(coordinate)
                    else:
                        coord_right = None
                    if coord_up:
                        current_coord = coordinate
                        if coord_up in self.hit_coordinates:
                            for num in range(battlefiled.rows.index(coordinate[0])):
                                next_coord = battlefiled.coord_up(current_coord)
                                if next_coord in self.targetted_coordinates and next_coord not in self.hit_coordinates:
                                    break
                                elif next_coord not in self.targetted_coordinates and next_coord not in options:
                                    options.append(next_coord)
                                    break
                                else:
                                    pass
                                current_coord = next_coord
                    if coord_down:
                        current_coord = coordinate
                        if coord_down in self.hit_coordinates:
                            for num in range(len(battlefiled.rows) - battlefiled.rows.index(coordinate[0])):
                                next_coord = battlefiled.coord_down(current_coord)
                                if next_coord in self.targetted_coordinates and next_coord not in self.hit_coordinates:
                                    break
                                elif next_coord not in self.targetted_coordinates and next_coord not in options:
                                    options.append(next_coord)
                                    break
                                else:
                                    pass
                                current_coord = next_coord
                    if coord_left:
                        current_coord = coordinate
                        if coord_left in self.hit_coordinates:
                            for num in range(coordinate[-1]):
                                next_coord = battlefiled.coord_left(current_coord)
                                if next_coord in self.targetted_coordinates and next_coord not in self.hit_coordinates:
                                    break
                                elif next_coord not in self.targetted_coordinates and next_coord not in options:
                                    options.append(next_coord)
                                    break
                                else:
                                    pass
                                current_coord = next_coord
                    if coord_right:
                        current_coord = coordinate
                        if coord_right in self.hit_coordinates:
                            for num in range(len(battlefiled.columns) - coordinate[-1]):
                                next_coord = battlefiled.coord_right(current_coord)
                                if next_coord in self.targetted_coordinates and next_coord not in self.hit_coordinates:
                                    break
                                elif next_coord not in self.targetted_coordinates and next_coord not in options:
                                    options.append(next_coord)
                                    break
                                else:
                                    pass
                                current_coord = next_coord
                if options:
                    target_options.extend([option for option in options if option not in target_options])
                    print("RESULT 2")
                    return target_options
                else:    
                    for coordinate in self.active_targets:
                        if coord_up:
                            if coord_up not in self.targetted_coordinates and coord_up not in target_options:
                                options.append(coord_up)
                        if coord_down:
                            if coord_down not in self.targetted_coordinates and coord_down not in target_options:
                                options.append(coord_down)
                        if coord_left:
                            if coord_left not in self.targetted_coordinates and coord_left not in target_options:
                                options.append(coord_left)
                        if coord_right:
                            if coord_right not in self.targetted_coordinates and coord_right not in target_options:
                                options.append(coord_right)
                    target_options.extend([option for option in options if option not in target_options])
                    return target_options

    def target(self, player):
        shot = 0
        last_shot_hit = False
        while shot < 1 or last_shot_hit:
            from Battlefiled_main import check_winner
            if check_winner():
                break
            battlefiled = player.battlefield
            grid = player.battlefield.grid
            rows = battlefiled.rows
            player.display_ships()
            input(continue_str)
            battlefiled.display_wrapped("Your")
            input(continue_str)
            while True:
                try:
                    if not self.active_targets:
                        coordinate = (rows[random.randint(0, len(rows)-1)], random.randint(0, 10))
                    else:
                        options = self.target_options(player)
                        coordinate = options[random.randint(0, len(options))]
                    if grid[coordinate] == Battlefield.states[6] or grid[coordinate] == Battlefield.states[7]:
                        raise BusyCoordinateException
                    break
                except Exception:
                    pass
            self.targetted_coordinates.append(coordinate)
            if not grid[coordinate]:
                grid[coordinate] = Battlefield.states[6]
                print(NL*2 + obj_str.incoming_complete + NL)
                battlefiled.display()
                print(NL*2 + obj_str.empty_waters_str.format(str(coordinate)) + NL*2)
                shot += 1
                last_shot_hit = False
            elif grid[coordinate] == Battlefield.states[5]:
                grid[coordinate] = Battlefield.states[7]
                print(NL*2 + obj_str.incoming_complete + NL)
                battlefiled.display()
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
#=================================================================================================================
#Test_Zone:
# test_player = Player()
# test_computer = Computer()
# test_player.battlefield.display_wrapped()
# test_coordinates1 = []
# for ship in test_player.fleet.values():
#     for coordinate in ship.coordinates:
#         test_coordinates1.append(coordinate)
# hit_coords = [coord for coord in test_coordinates1 if test_coordinates1.index(coord)%2 == 0]
# hit_coords.extend([list(test_player.fleet.values())[0].coordinates[1], list(test_player.fleet.values())[1].coordinates[1]])
# for coord in hit_coords:
#     test_player.battlefield.grid[coord] = test_player.battlefield.states[7]
# test_computer.hit_coordinates = hit_coords
# test_computer.targetted_coordinates = hit_coords
# test_computer.active_targets = hit_coords
# test_player.battlefield.display_wrapped()

# print(NL + "targetted_coordinates: " + NL)
# print(test_computer.targetted_coordinates)
# print(NL + "active_targets: " + NL)
# print(test_computer.active_targets)
# print(NL + "hit_coordinates: " + NL)
# print(test_computer.hit_coordinates)
# print(NL + "target_options: " + NL)
# print(test_computer.target_options(test_player))

# for coord in test_computer.target_options(test_player):
#     test_player.battlefield.grid[coord] = test_player.battlefield.states[8]
# test_player.battlefield.display_wrapped()

#=================================================================================================================