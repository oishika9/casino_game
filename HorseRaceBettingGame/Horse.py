
from ..imports import *

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from coord import Coord
    from maps.base import Map
    from tiles.base import MapObject
    from tiles.map_objects import *

# Horse Class which will define a single instance of a horse to be used in Horse Race Betting Game

class Horse:


    def __init__(self, number: int, victory: bool):
        assert isinstance(number, int), "number must be an int"
        assert isinstance(victory, bool), "victory must be a bool"
        self.__number = number
        self.__victory = victory


    @classmethod
    def copy(cls, horse : 'Horse') -> 'Horse':
        """
        This method is used to deepcopy an instance of an existing horse

        Preconditions:
            - horse is an instance of Horse

        @param horse: The horse to be copied
        @return (Horse): A new instance of the given horse with same fields
        """
        return cls(horse.get_number(), horse.was_victorious())


    def get_number(self) -> int:
        """
        This method is used to get the number (field) of the horse

        @return (int): The number of the horse
        """
        return self.__number


    def was_victorious(self) -> bool:
        """
        This method is used to know whether a horse has won the previous race

        @return (bool): True if the horse won the previous race, False otherwise
        """
        return self.__victory


    def set_victory(self, victory: bool) -> None:
        """
        This method is used to set the horse as victorious (edits the field)
        """
        self.__victory = victory