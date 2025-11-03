from ..imports import *

from .Hand import Hand
from .Deck import Deck
from .Blackjack import BlackjackGame
from ..COMMANDS.BlackjackCommands import *

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from coord import Coord
    from maps.base import Map
    from tiles.base import MapObject
    from tiles.map_objects import *
    from command import MenuCommand

from enum import Enum
import copy

from ..BALANCE.PlayerBalance import BalanceManager, BalanceChangeReason, BalanceEffectObserver, SoundEffectObserver


class BlackjackComputer(Computer):
    """
    offers Blackjack via menu commands
    players can see options like [Deal, Hit, Stand, Quit]
    """
    def __init__(self, image_name: str = 'casino_table4'):
        # We'll build a dictionary of menu commands
        # and pass them to the parent Computer constructor.
        self.player_games: dict["HumanPlayer", BlackjackGame] = {}

        self.menu_options = {
            "Deal": BlackjackDealCommand(self),
            "Hit": BlackjackHitCommand(self),
            "Stand": BlackjackStandCommand(self),
            "Quit": BlackjackQuitCommand(self),
        }

        super().__init__(
            image_name=image_name,
            menu_name="Blackjack Menu",
            menu_options=self.menu_options
        )

    def get_menu_options(self):
        """
        @returns:
            a dictionary containing the current menu option commands
        """
        return self.menu_options

    def get_or_create_game(self, player: "HumanPlayer") -> BlackjackGame:
        """
        each player can have a separate game instance

        @returns:
            The BlackjackGame instance for the given player
        """
        if player not in self.player_games:
            self.player_games[player] = BlackjackGame()
        return self.player_games[player]

    def remove_game(self, player: "HumanPlayer") -> None:
        # remove the player's blackjackGame (e.g. after round ends or they quit)
        if player in self.player_games:
            del self.player_games[player]

    #PROTOTYPE --------
    def clone(self):
        return copy.deepcopy(self)


