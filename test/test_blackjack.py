import pytest

from ..imports import *
from ..Cards.Card import Card, Suit, Rank
from ..Cards.Hand import Hand, Deck
from ..Cards.Blackjack import BlackjackGame

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from coord import Coord
    from Player import HumanPlayer

class TestBlackjack:
    def test_hand_total_blackjack_ace_logic(self):
        h = Hand()
        h.add_card(Card(Suit.HEARTS, Rank.ACE))
        h.add_card(Card(Suit.HEARTS, Rank.NINE))
        assert h.total_blackjack() == 20

    def test_hand_is_busted(self):
        h = Hand()
        h.add_card(Card(Suit.HEARTS, Rank.TEN))
        h.add_card(Card(Suit.CLUBS, Rank.KING))
        h.add_card(Card(Suit.DIAMONDS, Rank.TWO))
        assert h.is_busted_blackjack()

    def test_blackjack_start_new_round(self):
        game = BlackjackGame()
        game.start_new_round()
        assert len(game.player_hand.cards) == 2
        assert len(game.dealer_hand.cards) == 2
        # 52 - 4 => 48
        assert len(game.deck.cards) == 48

    def test_blackjack_determine_winner_player(self):
        game = BlackjackGame()
        # force player's total > dealer
        game.player_hand.clear_hand()
        game.dealer_hand.clear_hand()

        # player = 20
        game.player_hand.add_card(Card(Suit.HEARTS, Rank.TEN))
        game.player_hand.add_card(Card(Suit.HEARTS, Rank.QUEEN))

        # dealer = 18
        game.dealer_hand.add_card(Card(Suit.DIAMONDS, Rank.NINE))
        game.dealer_hand.add_card(Card(Suit.CLUBS, Rank.NINE))

        winner = game.determine_winner()
        assert winner == "Player"

