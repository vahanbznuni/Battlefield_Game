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
    
    def get_coord_row_index(self, coordinate):
        return self.rows.index(coordinate[0])

    def get_last_coords(self, coordinate, ship_type):
        ship_size = Ship.types[ship_type]
        list_options = []
        if (coordinate[-1]) - ship_size >= 1:
            last_left = (coordinate[0], coordinate[-1] - ship_size)
            list_options.append(last_left)
        if (coordinate[-1]) + ship_size <= len(self.columns):
            last_right = (coordinate[0], coordinate[-1] + ship_size)
            list_options.append(last_right)
        if self.get_coord_row_index(coordinate) - ship_size >= 0:
            last_up = (self.rows[self.get_coord_row_index(coordinate) - ship_size], coordinate[-1])
            list_options.append(last_up)
        if self.get_coord_row_index(coordinate) + ship_size < len(self.rows):
            last_down = (self.rows[self.get_coord_row_index(coordinate) + ship_size], coordinate[-1])
            list_options.append(last_down)
        return list_options

    def gen_coords(self, ship_type):
        print("\n")
        self.display()
        print("\n")
        ship_size = Ship.types[ship_type]
        coordinates = []
        input_str = "Please enter {} coordinate for {}: "
        input1 = input(input_str.format("STARTING", str(ship_type)))
        start_coordinate = (input1[0], int(input1[1:]))
        coordinates.append(start_coordinate)
        print("\n")
        copy_grid = self.grid.copy()
        self.grid[start_coordinate] = "*"
        input_str_last = input_str.format("ending", str(ship_type)).replace("enter", "choose") + "\n" + "\n" +\
             "Enter the option *NUMBER* for your choice from the following options listed below - as shown on the grid: "+ "\n"
        for num in range(len(self.get_last_coords(start_coordinate, ship_type))):
            input_str_last += "Option " + str(num+1) + ": " + Battlefield.coord_to_str(self.get_last_coords(start_coordinate, ship_type)[num]) +"\n"
            self.grid[self.get_last_coords(start_coordinate, ship_type)[num]] = num+1
        self.display()
        print("\n")
        input2 = input(input_str_last)
        last_coordinate = self.get_last_coords(start_coordinate, ship_type)[int(input2) - 1]
        coordinates.append(last_coordinate)
        if ship_size <= 2:
            coordinates.sort()
            self.grid.update(copy_grid)
            return coordinates
        else:
            count = 0
            coordinate = start_coordinate
            while count <= ship_size - 2:
                if start_coordinate[0] == last_coordinate[0]:
                    if start_coordinate[-1] > last_coordinate[-1]:
                        next_coordinate = (coordinate[0], coordinate[-1] - 1)
                        coordinates.append(next_coordinate)
                        count += 1
                        coordinate = next_coordinate
                    elif start_coordinate[-1] < last_coordinate[-1]:
                        next_coordinate = (coordinate[0], coordinate[-1] + 1)
                        coordinates.append(next_coordinate)
                        count += 1
                        coordinate = next_coordinate
                elif  start_coordinate[-1] == last_coordinate[-1]:
                    if self.get_coord_row_index(start_coordinate) > self.get_coord_row_index(last_coordinate):
                        next_coordinate = (self.rows[self.get_coord_row_index(coordinate) - 1], coordinate[-1])
                        coordinates.append(next_coordinate)
                        count += 1
                        coordinate = next_coordinate
                    elif self.get_coord_row_index(start_coordinate) < self.get_coord_row_index(last_coordinate):
                        next_coordinate = (self.rows[self.get_coord_row_index(coordinate) + 1], coordinate[-1])
                        coordinates.append(next_coordinate)
                        count += 1
                        coordinate = next_coordinate
            coordinates.sort()
            self.grid.update(copy_grid)
            return coordinates

    def get_random_coords(self, ship_type):
        ship_size = Ship.types[ship_type]
        coords = []
        import random
        for num in range(ship_size):
            coords.append((self.rows[random.randint(0, 10)], str(random.randint(0, 10))))
        return coords
    
    def generate_ships(self):
        fleet = {}
        for ship_type in Ship.types.keys():
            num = 1
            ship = Ship(self.gen_coords(ship_type), ship_type, self)
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
      

#=================================================================================================================
player1 = Player()
player1.battlefield.display()

# test_battlefield = Battlefield(10, 10)


# for key in Ship.types.keys():
#     print(test_battlefield.gen_coords(key))
#     print("\n")
#     print("Final Battlefield: ")
#     print("\n")
#     test_battlefield.display()



#=================================================================================================================