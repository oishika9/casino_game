from ..imports import *

from .Deck import Deck, Card, Rank

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from coord import Coord
    from maps.base import Map
    from tiles.base import MapObject
    from tiles.map_objects import *

from enum import Enum
import random


class Hand:
    """
    represents a collection of Card objects a player holds
    used in:
        - blackjack (multiple cards)
        - one-card poker (singe card)
    """
    def __init__(self):
        """
        initializes an empty hand
        """
        self.cards: list[Card] = []

    def add_card(self, card: Card):
        """
        appends a card to the hand

        @preconditions:
            - card is not None
        """
        if card:
            self.cards.append(card)

    def clear_hand(self):
        """
        removes all cards from hand
        """
        self.cards = []

    def total_blackjack(self):
        """
        calculates optimal blackjack total (ace = 1 or 11)

        for blackjack:
         - each card's base_value() (with aces = 1, face cards = 10)
         - upgrade Aces from 1 to 11 if it keeps total <= 21.

         @returns:
            int representing the total value of hand
        """
        base_sum = 0
        for card in self.cards:
            card_value = card.base_value()

            if card.rank == Rank.ACE:
                card_value = 1

            card_value = min(10, card_value)
            base_sum += card_value

        ace_count = sum(1 for card in self.cards if card.rank == Rank.ACE)

        for _ in range(ace_count):
            if base_sum + 10 <= 21:
                base_sum += 10
        return base_sum

    def is_busted_blackjack(self):
        """
        @returns:
            Bool representing whether the current value of hand is more than 21
        """
        return self.total_blackjack() > 21

    def __str__(self):
        """
        @returns:
            str of comma sepparated list of card names
        """
        return ", ".join(str(card) for card in self.cards)
