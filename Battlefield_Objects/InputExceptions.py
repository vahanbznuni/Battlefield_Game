
"""
InputException. Contains all custom exceptions defined for the game.

The InputException subclass of the built-in Exception class - as well as 
  subclasses of InputException - assist with the game's exception handling.
"""

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
    For Bad coordinate inputs when input coordinate does not allow enough\
         room for given ship
    """ 