       ship_size = Ship.types[ship_type]
        
        def get_coord_row_index(coordinate):
            return self.battlefield.rows.index(coordinate[0])
        
        def get_last_coords(coordinate):
            last_left = coordinate[0] + str(int(coordinate[1]) - ship_size)
            last_right = coordinate[0] + str(int(coordinate[1]) + ship_size)
            last_up = self.battlefield.rows[get_coord_row_index(coordinate) + ship_size] + coordinate[1]
            last_down = self.battlefield.rows[get_coord_row_index(coordinate) - ship_size] + coordinate[1]
            list_options = [last_left, last_right, last_up, last_down]
            return [item for item in list_options if item[0] in self.battlefield.rows and int(item[1:] in self.battlefield.columns]
        
        def gen_coords():
            coordinates = []
            input_str = "Please enter {} coordinate for {}: "
            start_coordinate = input(input_str.format("starting", str(ship_type)))
            coordinates.append(start_coordinate)
            input_str_last = input_str.format("ending", str(ship_type)) + "from the following options: \n"
            for num in len(get_last_coords(start_coordinate)):
                input_str_last += "Option " + str(num) + ": " + get_last_coords(start_coordinate)[num-1] + "\n"
            last_coordinate = input(input_str_last)
            coordinates.append(last_coordinate)
            if ship_size <= 2:
                return coordinates
            else:
                count = 0
                while count <= ship_size - 2:
                    pass