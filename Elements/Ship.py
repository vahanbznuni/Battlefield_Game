"""
Ship Module.

The Ship class contains data relating to each ship, including its coordinates, 
  its name/type, and its health status.
"""

if __name__ == "__main__":
    import sys
    import os
    sys.path.append(os.path.join( os.path.dirname( __file__ ), '..' ))

from Elements.Battlefield import Battlefield
from Elements.Battlefield_Strings.Battlefield_Strings import NL, Formatting

class Ship:
    """contains data structure(s) relating to each ship, including its\
         coordinates, it's name/type, and it's health status.

    Class variables:
      types (dict): contains names of ship types as keys, and sizes for each
        ship as values.
    Instance Variables:
      coordinates (list): the coordinates of the ship.
      type (str): the name of the ship type, from the list of ship types.
      battlefield (object): a Battlefiled class bject - the Battlefiled to
        which the ship has been added.
      size (int): the number of coordinates that a ship occupipes on the
        Battlefiled grid.
      sunk (bool): True if all of the ship's coordinates have been hit.
    Methods:
      __init__, __repr__, check_sunk
    """

    types = {"Carrier": 5, "Battleship": 4, "Destroyer": 3, "Submarine": 3,\
         "Patrol Boat": 2}
    
    def __init__(self, coordinates, type, battlefield):
        """initialize an instance of a Ship.
        
        Args:
          coordinates (list): the coordinates of the ship (where the ship will
            be placed on a Battlefield)
          type (str): the name of the ship type, from the list of ship types.
          battlefield (object): a Battlefiled class bject - the Battlefiled
            to which the ship will be added.
        """
        self.coordinates = coordinates
        self.type = type
        self.battlefield = battlefield
        self.size = Ship.types[self.type]
        self.sunk = False
        for coordinate in self.coordinates:
            self.battlefield.grid[coordinate] = Battlefield.states[5]

    def __repr__(self):
        """String representation of Ship containing it's type and coordinates"""
        return "Type " + str(self.type) + \
          ". Coordinates: " + str(self.coordinates)

    def check_sunk(self):
        """Check if the ship has sunk (all ship coordinates hit). \
            If so, update the sunk attribute to True, and \
                print a stetement identifyuing the sunk ship"""
        hit_coordinates = 0
        battlefield = self.battlefield
        for coordinate in self.coordinates:
            if battlefield.grid[coordinate] == battlefield.states[7]:
                hit_coordinates += 1
        if hit_coordinates == self.size:
            self.sunk = True
            for coordinate in self.coordinates:
                battlefield.grid[coordinate] = Battlefield.states[9]
            print(NL*2 + Formatting.line_wrap3(
              self.type + " HAS BEEN SUNK!!!!") + NL*2)
