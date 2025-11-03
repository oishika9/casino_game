
from ..imports import *
from .Horse import *
import random

from typing import TYPE_CHECKING, Optional, List
if TYPE_CHECKING:
    from coord import Coord
    from maps.base import Map
    from tiles.base import MapObject
    from tiles.map_objects import *

# The class BandOfHorses is a class that will define a group of horses to be used and calculates the odds
# of the horses which are competing in the same race

class BandOfHorses:


    def __init__(self, horses: Optional[List[Horse]] = None) -> None:
        if horses is None:
            horses = [
                Horse(1, False),
                Horse(2, False),
                Horse(3, False),
                Horse(4, False),
                Horse(5, False)
            ]
        else:
            # Check if all items in the list are instances of Horse
            assert all(isinstance(h, Horse) for h in horses), "All items must be instances of Horse"
        self.__horses = horses


    def _get_horses(self) -> list:
        """
        This method is used to return the horses in the band

        @return (list): The list of horses in the band
        """
        return self.__horses


    def deep_copy_horses(self) -> 'BandOfHorses':
        """
        This method is used to deepcopy a band of horses

        @return (BandOfHorses): A new instance of the band of horses with same fields
        """
        new_horses : list = []
        for horse in self.__horses:
            new_horses.append(Horse.copy(horse))
        return BandOfHorses(new_horses)


    def is_first(self, horse : Horse) -> bool:
        """
        This method is used to check if a horse is first in the ranking

        Preconditions:
            - horse should be a member of the band (i.e. one of the horses in the list)

        @param horse: The horse to be checked
        @return (bool): True if the horse is first in the ranking, False otherwise
        """
        return self.__horses[0] == horse


    def figure_out_winner(self) -> 'BandOfHorses':
        """
        This method outputs a ranking of the horses after a race

        @return (BandOfHorses): A new instance of the band of horses with the horses in order of their ranking
        """
        # Creating a deep copy of the horses
        horses = self.deep_copy_horses()
        # Extracting the list for easier manipulation
        ranking = horses._get_horses()
        # Shuffle the list randomly
        random.shuffle(ranking)

        # Finding the previous winner and moving it up a slot
        for horse in ranking:
            if horse.was_victorious() and not horses.is_first(horse):
                # Getting the index of the horse
                index = ranking.index(horse)
                # Moving the horse up a slot
                ranking[index], ranking[index - 1] = ranking[index - 1], ranking[index]
                # Removing the victory from the horse
                horse.set_victory(False)
                break

        # Adding the victory to the new first horse
        ranking[0].set_victory(True)

        # Returning the new ranking
        return BandOfHorses(ranking)



