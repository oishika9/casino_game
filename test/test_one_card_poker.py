import pytest

from ..imports import *
from ..Cards.Card import Card, Suit, Rank
from ..Cards.Hand import Hand, Deck
from ..Cards.OneCardPoker import OneCardPokerGame
from ..Cards.OneCardPokerStrategy import EasyPokerStrategy, MediumPokerStrategy, HardPokerStrategy

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from coord import Coord
    from Player import HumanPlayer


class TestPoker:
    def test_one_card_poker_setup(self):
        game = OneCardPokerGame(strategy=MediumPokerStrategy())
        game.start_new_round()
        # Each player should have 1 card if we have enough cards (3 total).
        assert len(game.deck) == 3
