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
        start_coordinate = (input1[0].upper(), int(input1[1:]))
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
        start_coordinate = (self.rows[random.randint(0, len(self.rows)-1)], random.randint(1, len(self.columns)))
        if self.grid[start_coordinate] == Battlefield.states[5]:
            raise BusyCoordinateException
        coordinates.append(start_coordinate)
        options = list(self.coord_opts(start_coordinate, ship_type).values())
        if not options:
            raise NotEnoughRoomException
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

    def generate_ships(self):
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
    
    def target_options(self, player):
        battlefield = player.battlefield
        row_index = battlefield.row_index
        target_options = []
        coord_up = battlefield.coord_up                    
        coord_down = battlefield.coord_down                   
        coord_left = battlefield.coord_left                   
        coord_right = battlefield.coord_right
        if self.active_targets:
            options = []
            for coordinate in self.active_targets:
                row = battlefield.get_row(coordinate)
                column = battlefield.get_column(coordinate)
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
                        if seperation >= 1:
                            for num in range(seperation):
                                next_coord = coord_down(current_coord)
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
                def adjascent_targets(direction_func, coord):
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
                for coordinate in self.active_targets:   
                    if coord_up(coordinate):
                        adjascent_targets(coord_up, coordinate)
                    if coord_down(coordinate):
                        adjascent_targets(coord_down, coordinate)
                    if coord_left(coordinate):
                        adjascent_targets(coord_left, coordinate)
                    if coord_right(coordinate):
                        adjascent_targets(coord_right, coordinate)
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
            def next_targetted_coord(direction_func, coord):
                if direction_func == coord_up:
                    range_value = row_index(coord)
                elif direction_func == coord_down:
                    range_value = len(battlefield.rows) - row_index(coord)
                elif direction_func == coord_left:
                    range_value = coord[-1]
                elif direction_func == coord_right:
                    range_value = len(battlefield.columns) - coord[-1]
                current_coord = coord
                if direction_func(coord) and direction_func(coord) not in self.targetted_coordinates:
                    for num in range(range_value):
                        next_coord = direction_func(current_coord)
                        if next_coord in self.targetted_coordinates:
                            return next_coord
                        elif next_coord:
                            current_coord = next_coord
            def horizontal_target_size(coord):
                left_border = next_targetted_coord(coord_left, coord)
                right_border = next_targetted_coord(coord_right, coord)
                if left_border and right_border:
                    difference = right_border[-1] - left_border[-1]
                    target_size = difference - 1
                elif left_border and not right_border:
                    difference = len(battlefield.rows) - left_border[-1]
                    target_size = difference
                elif not left_border and right_border:
                    difference = right_border[-1]
                    target_size = difference - 1
                elif not left_border and not right_border:
                    target_size = len(battlefield.rows)
                return target_size
            def vertical_target_size(coord):
                top_border = next_targetted_coord(coord_up, coord)
                bottom_border = next_targetted_coord(coord_down, coord)
                if top_border and bottom_border:
                    difference = row_index(bottom_border) - row_index(top_border) 
                    target_size = difference - 1
                if top_border and not bottom_border:
                    difference = len(battlefield.rows) - 1 - row_index(top_border)
                    target_size = difference
                if not top_border and bottom_border:
                    difference = row_index(bottom_border)
                    target_size = difference
                if not top_border and not bottom_border:
                    target_size = len(battlefield.rows)
                return target_size
            for coordinate in available_targets:
                for ship in player.fleet.values():
                    if not ship.sunk:
                        if ship.size <= horizontal_target_size(coordinate) or ship.size <= vertical_target_size(coordinate):
                            if coordinate not in options:
                                options.append(coordinate)
            for option in options:
                #guyguygu
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


# a = test_computer.battlefield
# print("   " + "  ".join([str(column) for column in a.columns]))
# for row_name in a.rows:
#     row = []
#     for key in a.grid.keys():
#         if key[0] == row_name:
#             if not a.grid[key]:
#                 row.append("[ ]")
#             elif a.grid[key]==Battlefield.states[1]:
#                 row.append("[1]")
#             elif a.grid[key]==Battlefield.states[2]:
#                 row.append("[2]")
#             elif a.grid[key]==Battlefield.states[3]:
#                 row.append("[3]")
#             elif a.grid[key]==Battlefield.states[4]:
#                 row.append("[4]")
#             elif a.grid[key]==Battlefield.states[5]:
#                 row.append("[+]")
#             elif a.grid[key]==Battlefield.states[6]:
#                 row.append("[o]")
#             elif a.grid[key]==Battlefield.states[7]:
#                 row.append("[X]")
#             elif a.grid[key]==Battlefield.states[8]:
#                 row.append("[*]")
#             elif a.grid[key]==Battlefield.states[9]:
#                 row.append("[#]")                      
#     print(row_name + " " + "".join(row))

# print("/n")
# for ship in test_computer.fleet.values():
#     print(ship.type, ship.coordinates)
# input("continue")
#=================================================================================================================
