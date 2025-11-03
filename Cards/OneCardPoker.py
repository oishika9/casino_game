from ..imports import *

from .Hand import Hand
from .Deck import Deck
from .Card import Card, Rank, Suit
from .OneCardPokerStrategy import PokerStrategy

from typing import TYPE_CHECKING, Optional
if TYPE_CHECKING:
    from coord import Coord
    from maps.base import Map
    from tiles.base import MapObject
    from tiles.map_objects import *

from enum import Enum

import random


class OneCardPokerGame:
    """
    One-Card Poker with a single AI rival.
    The pot is formed by the player's and AI's ante.
    Then the player can bet or fold, and the AI decides
    whether to call or fold (via its PokerStrategy).
    """

    def __init__(self, strategy: PokerStrategy, ante: float = 10.0, bet_amount: float = 10.0):
        """
        @parameters:
            strategy: the AI's strategy object.
            ante: the amount each side pays to form the pot.
            bet_amount: the fixed bet the player will place if they choose to bet.

        @preconditions:
            - ante >= 0
        """
        assert ante >= 0

        self.strategy = strategy
        self.ante = ante
        self.bet_amount = bet_amount

        self.deck = Deck(custom_cards=[
            Card(Suit.SPADES, Rank.QUEEN),
            Card(Suit.SPADES, Rank.KING),
            Card(Suit.SPADES, Rank.ACE)
        ])

        self.player_card: list[Card] = []
        self.ai_card: Optional[Card] = None
        self.pot: float = 0.0
        self.active_round: bool = False

    def start_new_round(self) -> None:
        """
        reset deck, then shuffle, ante up from both sides, deal 1 card each

        @postcoditions:
            - active_round is True
            - pot is 0
            - both hands are empty, and 3-card deck is shuffled
        """
        self.deck = Deck(custom_cards=[
            Card(Suit.SPADES, Rank.QUEEN),
            Card(Suit.SPADES, Rank.KING),
            Card(Suit.SPADES, Rank.ACE)
        ])

        self.deck.shuffle()

        self.player_card.clear()
        self.ai_card = None
        self.pot = 0.0
        self.active_round = True

    def deal_cards(self) -> None:
        """
        deal 1 card to player, 1 card to AI
        """
        self.player_card.clear()
        pcard = self.deck.deal_card()
        if pcard:
            self.player_card.append(pcard)
        self.ai_card = self.deck.deal_card()

    def ai_decides_call(self) -> bool:
        """
        use our strategy to see if the AI calls or folds

        @returns:
            Boolean: AIStrategy decision (True if call, False if fold)
        """
        return self.strategy.decide_call_or_fold(self)

    def showdown(self) -> str:
        """
        compare the player's card vs AI's card
        resolve the round and declare winner

        @returns:
            'Player' or 'AI' or 'Tie'

        @precoditions:
            - player_card and ai_card must be present
        """
        if not self.ai_card or len(self.player_card) == 0:
            return "Tie"

        ai_val = self.ai_card.rank.numeric_value()
        player_val = self.player_card[0].rank.numeric_value()

        if player_val > ai_val:
            return "Player"
        elif ai_val > player_val:
            return "AI"
        else:
            return "Tie"
