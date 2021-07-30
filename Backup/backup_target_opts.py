    def target_options(self, player):
        battlefiled = player.battlefield
        target_options = []
        if self.active_targets:
            for coordinate in self.active_targets: 
                options = []
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
                    if coord_up in self.hit_coordinates:
                        if coord_down:
                            if coord_down not in self.targetted_coordinates and coord_down not in target_options:
                                options.append(coord_down)
                            elif coord_down in self.hit_coordinates:
                                pass
                if coord_down:
                    if coord_down in self.hit_coordinates:
                        if coord_up:
                            if coord_up not in self.targetted_coordinates and coord_up not in target_options:
                                target_options.append(coord_up)
                if coord_left:
                    if coord_left in self.hit_coordinates:
                        if coord_right:
                            if coord_right not in self.targetted_coordinates and coord_right not in target_options:
                                target_options.append(coord_right)
                if coord_right:
                    if coord_right in self.hit_coordinates:
                        if coord_left:
                            if coord_left not in self.targetted_coordinates and coord_left not in target_options:
                                target_options.append(coord_left)
                if not options:
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
                target_options.extend(option for option in options if option not in target_options)
        return target_options