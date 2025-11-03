from ..imports import *

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from coord import Coord
    from maps.base import Map
    from tiles.base import MapObject
    from tiles.map_objects import *

from enum import Enum


class Suit(Enum):
    """
    enum of the four standart playing card suits
    """
    HEARTS = "Hearts"
    DIAMONDS = "Diamonds"
    CLUBS = "Clubs"
    SPADES = "Spades"

    def __str__(self):
        """
        string representation used in long card names

        @returns:
            the full suit name (Hearts, Diamonds, Clubs, or Spades)
        """
        return self.value

    def short_str(self):
        """
        a single-character abbreviation of the suit name

        @returns:
            the first letter of the suit (H, D, C, or S)
        """
        return self.value[0]
