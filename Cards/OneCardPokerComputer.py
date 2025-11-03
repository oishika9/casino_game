from ..imports import *

from .Hand import Hand
from .Deck import Deck
from .Card import Card, Rank
from .OneCardPoker import OneCardPokerGame
from .OneCardPokerStrategy import PokerStrategy
from ..COMMANDS.OneCardPokerCommands import OneCardDealCommand, OneCardBetCommand, OneCardFoldCommand, OneCardQuitCommand

from typing import TYPE_CHECKING, Optional
if TYPE_CHECKING:
    from coord import Coord
    from maps.base import Map
    from tiles.base import MapObject
    from tiles.map_objects import *
    from command import MenuCommand

from enum import Enum

import random

from ..BALANCE.PlayerBalance import BalanceManager, BalanceChangeReason, BalanceEffectObserver, SoundEffectObserver


class OneCardPokerComputer(Computer):
    """
    map-object (inherits Computer), that lets a player sit at a One-Card poker table and play against an AI defined by PokerStrategy

    displays a menu with commands: (Deal, Bet, Stand, Fold, Quit)
    """
    def __init__(self, strategy: PokerStrategy, image_name: str = 'casino_table7'):
        self.player_games: dict["HumanPlayer", OneCardPokerGame] = {}

        self.menu_options = {
            "Deal": OneCardDealCommand(self),
            "Bet": OneCardBetCommand(self),
            "Fold": OneCardFoldCommand(self),
            "Quit": OneCardQuitCommand(self),
        }

        self.strategy = strategy

        super().__init__(
            image_name=image_name,
            menu_name="One-Card Poker Menu",
            menu_options=self.menu_options
        )

    def get_or_create_game(self, player: "HumanPlayer") -> OneCardPokerGame:
        """
        each player can have a separate game instance

        @returns:
            The OneCardPokerGame instance for the given player
        """
        if player not in self.player_games:
            self.player_games[player] = OneCardPokerGame(strategy=self.strategy, ante=10.0, bet_amount=10.0)
        return self.player_games[player]

    def remove_game(self, player: "HumanPlayer") -> None:
        if player in self.player_games:
            del self.player_games[player]

    def get_menu_options(self):
        """
        @returns:
            a dictionary containing the current menu option commands
        """
        return self.menu_options
