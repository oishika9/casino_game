from ..imports import *

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from coord import Coord
    from maps.base import Map
    from tiles.base import MapObject
    from tiles.map_objects import *

from enum import Enum


class Rank(Enum):
    """
    enum of card ranks from 2 to Ace, with some helper utilities
    """
    TWO = "2"
    THREE = "3"
    FOUR = "4"
    FIVE = "5"
    SIX = "6"
    SEVEN = "7"
    EIGHT = "8"
    NINE = "9"
    TEN = "10"
    JACK = "Jack"
    QUEEN = "Queen"
    KING = "King"
    ACE = "Ace"

    def numeric_value(self):
        """
        converst the rank to a numeric value, so that it can be used in comparisons
        these values dont necessarily correlate with a value in most games, just useful to prove a sorting or pecking order amongst cards

        @returns:
            int (from 2-14, where Ace is 14)
        """
        order = {
            Rank.TWO: 2,
            Rank.THREE: 3,
            Rank.FOUR: 4,
            Rank.FIVE: 5,
            Rank.SIX: 6,
            Rank.SEVEN: 7,
            Rank.EIGHT: 8,
            Rank.NINE: 9,
            Rank.TEN: 10,
            Rank.JACK: 11,
            Rank.QUEEN: 12,
            Rank.KING: 13,
            Rank.ACE: 14
        }
        return order[self]

    def short_str(self):
        """
        an abbreviation of the rank

        @returns:
            digits for 2-10, or the first letter for face / ace cards
        """
        if self.value.isdigit():
            return self.value
        return self.value[0]

    def starts_with_vowel(self):
        """
        determine if the ranks string begins with a vowel
        useful for formatting phrases like "a four" vs "an eight"

        @returns:
            Bool for if first character of self.value is a vowel (A E I O U)
        """
        return self.name[0].lower() in {'a', 'e', 'i', 'o', 'u'}
