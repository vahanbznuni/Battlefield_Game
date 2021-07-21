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
        size = Ship.types[self.type]
        self.ship_sunk = False
        for coordinate in self.coordinates:
            battlefield.grid[coordinate] = Battlefield.states[1]

    def get_coordinate_row(coordinate, battlefield):
        return battlefield.rows[battlefield.rows.index(coordinate[0])
    
    def gen_coordinates(self):
        coordinates = []
        input_str = "Please choose {} coordinate for {}"
        coord1 = input(input_str.format("starting", str(self.type)))
        coordinates.append(coord1)
        if self.size <=2:

        # list[list.index(item + x)] <movinf up and down rows or columns
        # coord2 = input(input_str.format("ending", str(self.type)))
        # coordinates.append(coord2)

        
        
    
    #def check_health(self)
    #may be overlapping with class Player check health
    #try PLayer met5hod first

class Carrier(Ship):
    def __init__(self, coordinates, type="Carrier"):
        super().__init__(coordinates, type)


# class Player:
# player_count = 0

    # def __init__(self, id):
    #     Player.player_count += 1
    #     self.id = Player.player_count
    #     self.carrier = Ship("Carrier", [a, b, c, d, e])
    #     self.ships = {}
    #     self.list_targetted_coordinates = []


