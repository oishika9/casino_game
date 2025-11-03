from ..imports import *

from .Suit import Suit
from .Rank import Rank

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from coord import Coord
    from maps.base import Map
    from tiles.base import MapObject
    from tiles.map_objects import *

from enum import Enum


class Card:
    """
    immutable data object representing a single card with a suit and a rank
    """
    def __init__(self, suit: Suit, rank: Rank):
        """
        constructs a card from a given suit and rank

        @parameters:
            suit: one of the four Suit enum values
            rank: one of the valid Rank enum values
        """
        self.suit = suit
        self.rank = rank

    def __str__(self):
        """
        @returns:
            str: long human-readable name for a card (e.g. Ace of Hearts)
        """
        return f"{self.rank.value} of {self.suit}"

    def short_str(self):
        """
        @returns:
            str: short representation for a card (e.g. 7H for Seven of Hearts)
        """
        return f"{self.rank.short_str()}{self.suit.short_str()}"

    def base_value(self) -> int:
        """
        returns the numeric value of the card, based on the sorting from 2 - Ace (14)
        @returns:
            int from 2-14
        """
        return self.rank.numeric_value()

    def get_suit(self) -> 'Suit':
        return self.suit

    def get_rank(self) -> 'Rank':
        return self.rank

    @classmethod
    def copy(cls, card : 'Card') -> 'Card':
        """
        class method that copies an instance of a card

        @parameters:
            card: Card ojbect to copy

        @returns:
            Card, a new card object with identical values
        """
        return cls(card.get_suit(), card.get_rank())

