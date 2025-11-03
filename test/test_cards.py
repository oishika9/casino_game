import pytest

from ..imports import *
from ..Cards.Card import Card, Suit, Rank
from ..Cards.Hand import Hand, Deck

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from coord import Coord
    from Player import HumanPlayer

class TestCards:
    def test_imports(self):
        assert str(Suit.CLUBS) == "Clubs"

        assert Rank.ACE.numeric_value() == 14
        assert Rank.TWO.numeric_value() == 2

        assert str(Card(Suit.HEARTS, Rank.ACE)) == "Ace of Hearts"

class TestDeck:
    def test_deck_standard(self):
        d = Deck()
        assert len(d) == 52

    def test_deck_custom(self):
        custom = [Card(Suit.SPADES, Rank.QUEEN), Card(Suit.CLUBS, Rank.KING), Card(Suit.HEARTS, Rank.ACE)]
        d = Deck(custom_cards=custom)
        assert len(d) == 3

        one_card_poker_deck = Deck(custom_cards=[
            Card(Suit.SPADES, Rank.QUEEN),
            Card(Suit.SPADES, Rank.KING),
            Card(Suit.SPADES, Rank.ACE)
        ])

        c = one_card_poker_deck.deal_card()
        assert c.get_suit() == Suit.SPADES
        assert c.get_rank() == Rank.ACE

class TestHand:
    def test_hand_add_card(self):
        h = Hand()
        h.add_card(Card(Suit.HEARTS, Rank.TEN))
        assert len(h.cards) == 1

    def test_hand_short_names(self):
        assert Suit.CLUBS.short_str() == "C"
        assert Suit.DIAMONDS.short_str() == "D"
        assert Suit.HEARTS.short_str() == "H"
        assert Suit.SPADES.short_str() == "S"

        assert Rank.ACE.short_str() == "A"
        assert Rank.KING.short_str() == "K"
        assert Rank.QUEEN.short_str() == "Q"
        assert Rank.JACK.short_str() == "J"

        assert Rank.TWO.short_str() == "2"
        assert Rank.TEN.short_str() == "10"
