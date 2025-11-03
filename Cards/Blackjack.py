from ..imports import *

from .Hand import Hand
from .Deck import Deck

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from coord import Coord
    from maps.base import Map
    from tiles.base import MapObject
    from tiles.map_objects import *

from enum import Enum


class BlackjackGame:
    """
    blackjack logic for a single player versus house game

    the pot is formed by the player's and AI's ante.
    then the player can bet or fold, and the AI decides
    whether to call or fold (via its PokerStrategy)
    """

    def __init__(self, ante: float = 10.0, bet_amount: float = 10.0):
        """
        @parameters:
            ante: the amount each side pays to form the pot.
            bet_amount: the fixed bet the player will place if they choose to bet.

        @preconditions:
            - ante >= 0
        """

        self.deck = Deck()
        self.player_hand = Hand()
        self.dealer_hand = Hand()

        self.ante = ante
        self.bet_amount = bet_amount

        self.active_round: bool = False

    def start_new_round(self):
        """
        reset deck, then shuffle, and deal 2 cards to player and dealer

        @postcoditions:
            - active_round is True
            - pot is 0
            - both hands (player and dealer) contain 2 cards
        """
        self.deck = Deck()
        self.deck.shuffle()

        self.player_hand.clear_hand()
        self.dealer_hand.clear_hand()

        self.player_hand.add_card(self.deck.deal_card())
        self.player_hand.add_card(self.deck.deal_card())

        self.dealer_hand.add_card(self.deck.deal_card())
        self.dealer_hand.add_card(self.deck.deal_card())

        self.pot = 0.0

        self.active_round = True

    def player_hit(self):
        """
        deals one card to player and returns a copy

        @returns:
            copy of Card dealt

        @preconditions:
            - Deck must contain at least one card
        """
        card = self.deck.deal_card()
        self.player_hand.add_card(card)
        return card.copy(card)

    def is_busted(self):
        """
        @returns:
            Bool representing if player hand total > 21
        """
        return self.player_hand.is_busted_blackjack()

    def dealer_turn(self):
        """
        follow the dealer rules:
            dealer hits until total >= 17

        @returns:
            Bool, true if dealer busts, false dealer stands
        """
        # return True if dealer bust, else False.
        while self.dealer_hand.total_blackjack() < 17:
            self.dealer_hand.add_card(self.deck.deal_card())
        return self.dealer_hand.is_busted_blackjack()

    def determine_winner(self):
        """
        decide outcome of round

        @returns:
            'Player', 'Dealer', or 'Push'
        """
        p_total = self.player_hand.total_blackjack()
        d_total = self.dealer_hand.total_blackjack()

        if p_total > 21:
            return "Dealer"
        if d_total > 21:
            return "Player"
        if p_total > d_total:
            return "Player"
        if d_total > p_total:
            return "Dealer"
        return "Push"

    def get_player_cards(self):
        """
        @returns:
            str of readable player card names
        """
        return [str(c) for c in self.player_hand.cards]

    def get_dealer_cards(self, reveal_all=False):
        """
        @parameters:
            reveal_all: if false, hide dealer's first card

        @returns:
            str of readable dealer card names
        """
        if reveal_all or not self.dealer_hand.cards:
            return [str(c) for c in self.dealer_hand.cards]
        return ["<Hidden Card>"] + [str(c) for c in self.dealer_hand.cards[1:]]

    def get_player_total(self):
        """
        @returns:
            int of blackjack total of player hand
        """
        return self.player_hand.total_blackjack()

    def get_dealer_total(self):
        """
        @returns:
            int of blackjack total of dealers hand
        """
        return self.dealer_hand.total_blackjack()
