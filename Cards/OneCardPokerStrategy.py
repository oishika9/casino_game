from ..imports import *
from abc import ABC, abstractmethod

from .Hand import Hand
from .Deck import Deck
from .Card import Card, Rank

from typing import TYPE_CHECKING, Optional
if TYPE_CHECKING:
    from coord import Coord
    from maps.base import Map
    from tiles.base import MapObject
    from tiles.map_objects import *
    from .OneCardPoker import OneCardPokerGame

from enum import Enum

import random


class PokerStrategy():
    """
    strategy interface (strategy pattern) used by one-card poker ai
    strategies decide whether the ai calls or folds
    """
    def __init__(self):
        self.num_bets = 0
        self.num_folds = 0

    def record_player_bet(self) -> None:
        self.num_bets += 1

    def record_player_fold(self) -> None:
        self.num_folds += 1

    @abstractmethod
    def decide_call_or_fold(self, game: 'OneCardPokerGame') -> bool: # type: ignore
        """
        return

        @parameters:
            game: the current one-card poker game instance

        @returns:
            Bool: True if the AI decides to call, or False if the AI decides to fold

        @preconditions:
            - game must be valid and active
        """
        pass


class EasyPokerStrategy(PokerStrategy):
    """
    easy AI: 90% of the time it tends to fold unless it has an ace
    """
    def decide_call_or_fold(self, game: 'OneCardPokerGame') -> bool:
        ai_card = game.ai_card
        if ai_card is None:
            return False

        card_val = ai_card.rank.numeric_value() # Q=12, K=13, A=14
        if card_val == 14:
            # always call aces
            return True
        else:
            # 10% chance to call
            return (random.random() < 0.1)


class MediumPokerStrategy(PokerStrategy):
    """
    medium AI: bets 100% of the time with ace, 70% of the time with a king, 25% of the time with a queen
    """
    def decide_call_or_fold(self, game: 'OneCardPokerGame') -> bool:
        ai_card = game.ai_card
        if ai_card is None:
            return False

        card_val = ai_card.rank.numeric_value()
        if card_val == 14:
            # always call aces
            return True
        elif card_val == 13: # king
            return (random.random() < 0.7)
        else:                # queen => 12
            return (random.random() < 0.25)


class HardPokerStrategy(PokerStrategy):
    """
    hard AI: builds profile of how often player bets/folds and plays off of that
    internal counters are updated via record_player_bet / record_player_fold which are called from the command
    """
    def decide_call_or_fold(self, game: 'OneCardPokerGame') -> bool:
        ai_card = game.ai_card
        if ai_card is None:
            return False

        card_val = ai_card.rank.numeric_value()

        total_actions = self.num_bets + self.num_folds
        if total_actions == 0:
            # if we have no data on the player, treat bet frequency as 50%
            player_bet_freq = 0.5
        else:
            player_bet_freq = self.num_bets / float(total_actions)

        # if highly agressive
        if player_bet_freq > 0.4:
            # only call with Ace
            return (card_val == 14)
        else:
            # call with King or Ace
            return (card_val >= 13)

