from ..imports import *

from .Card import Card, Suit, Rank

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from coord import Coord
    from maps.base import Map
    from tiles.base import MapObject
    from tiles.map_objects import *

from enum import Enum
import random


class Deck:
    """
    a pile of Cards that can be shuffled and dealt

    by default, builds a 52 card deck (4 suits 13 ranks)
    or you can supply a custom list of Cards
    """

    def __init__(self, custom_cards=None):
        """
        @parameters:
            custom_cards: Optional iterable of pre-built Cards

        @postconditions:
            - self.cards is initialised and may be shuffled / dealt
        """
        if custom_cards is None:
            # standard ordered 52 card deck
            self.cards = [Card(suit, rank) for suit in Suit for rank in Rank]
        else:
            self.cards = []
            for item in custom_cards:
                if isinstance(item, Card):
                    self.cards.append(item)

    def shuffle(self):
        """
        shuffle the deck in place
        """
        random.shuffle(self.cards)

    def deal_card(self):
        """
        draw the top card and return it

        @returns:
            Card from the deck

        @preconditions:
            - Deck must not be empty
        """
        return self.cards.pop()

    def __len__(self):
        """
        @returns:
            int representing the number of cards currently in the deck
        """
        return len(self.cards)
