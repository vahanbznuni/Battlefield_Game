import string

class Battlefield:
    states = [None, "healthy", "targetted", "hit"]

    def __init__(self, num_rows, num_columns):
        self.rows = [row for row in string.ascii_uppercase[:num_rows]]
        self.columns = [column for column in range(1, num_columns+1)]
        self.coordinates = []
        for row in self.rows:
            for column in self.columns:
                self.coordinates.append(row + str(column))
        self.grid = {coordinate: None for coordinate in self.coordinates}

    def display(self):
        print("   " + "  ".join([str(column) for column in self.columns]))
        for row_name in self.rows:
            row = []
            for key in self.grid.keys():
                if key[0] == row_name:
                    if not self.grid[key]:
                        row.append("[ ]")
                    elif self.grid[key]==Battlefield.states[2]:
                        row.append("[o]")
                    elif self.grid[key]==Battlefield.states[1]:
                        row.append("[+]")
                    elif self.grid[key]==Battlefield.states[3]:
                        row.append("[X]")
            print(row_name + " " + "".join(row))

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
            self.battlefield.grid[coordinate] = Battlefield.states[1] 
    
    #def check_health(self)
    #may be overlapping with class Player check health
    #try PLayer met5hod first

class Player:
    player_count = 0

    def __init__(self):
        Player.player_count += 1
        self.id = Player.player_count
        self.battlefield = Battlefield(10, 10)
        self.fleet = {}
        self.list_targetted_coordinates = []

    
        ship_size = Ship.types[ship_type]
        
        def get_coordinate_row(coordinate):
            return self.battlefield.rows[self.battlefield.rows.index(coordinate[0])]
        
        def get_last_coordinate_options(coordinate):
            last_left = coordinate[0] + str(int(coordinate[1]) - ship_size)
            last_right = coordinate[0] + str(int(coordinate[1]) + ship_size)
            last_up = str(get_coordinate_row(coordinate) + ship_size) + coordinate[1]
            last_down = str(get_coordinate_row(coordinate) - ship_size) + coordinate[1]
            list_options = [last_left, last_right, last_up, last_down]
            return [item for item in list_options if item[0] in self.battlefield.rows and item[1] in self.battlefield.columns]
        

        def gen_coordinates():
            coordinates = []
            input_str = "Please enter {} coordinate for {}: "
            start_coordinate = input(input_str.format("starting", str(ship_type)))
            coordinates.append(start_coordinate)
            input_str_last = input_str.format("ending", str(ship_type)) + "from the following options: \n"
            for num in len(get_last_coordinate_options(start_coordinate)):
                input_str_last += "Option " + str(num) + ": " + get_last_coordinate_options(start_coordinate)[num-1] + "\n"
            last_coordinate = input(input_str_last)
            coordinates.append(last_coordinate)
            if ship_size <= 2:
                return coordinates
            else:
                count = 0
                while count <= ship_size - 2:
                    pass

        

#>>>>>>>>>>>>>>Not working as intended. Analyze elements and reassemble.^^^^^^^^^^^^^^^^^^^^^^^^^

#========================================
#Testing:
# player1 = Player()
# player1_boat = player1.add_ship("Patrol Boat")
# print(player1_boat.coordinates