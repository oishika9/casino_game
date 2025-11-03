from typing import TYPE_CHECKING
from ..BALANCE.PlayerBalance import *
from ..imports import *
from ..NPCs.NPC_Bartender import WalkingBartender

if TYPE_CHECKING:
    from coord import Coord
    from maps.base import Map
    from ..tiles.base import MapObject
    from ..tiles.map_objects import *
    from message import ServerMessage
    from command import ChatCommand


class BalanceCommand(ChatCommand):
    name = 'balance'
    desc = 'Returns the current balance of the player; the command is /balance'

    @classmethod
    def matches(cls, command_text: str) -> bool:
        """
        This method checks if the command text matches the expected format for the balance command

       
        @param command_text (str): The full text of the command entered by the player
        @return (bool): True if command_text is exactly '/balance' and False otherwise
        """
        return command_text.strip().lower() == "balance"


    # METHOD RETRIEVES THE PLAYER'S BALANCE AND RETURNS A SERVER MESSAGE WITH CURRENT BALANCE
    def execute(self, command_text: str, context: "Map", player: "HumanPlayer") -> list:
        """
        Executes the balance command by retrieving the player's current balance and returning a server message

        Preconditions:
            - The player must be a valid HumanPlayer instance
            - BalanceManager must be properly initialised

        @param command_text (str): The command text entered by the player (expected to be '/balance')
        @param context (Map): The current game map
        @param player (HumanPlayer): The player issuing the command
        @return (list): A list containing a single ServerMessage with the current balance formatted as a currency value
        """
        balance = BalanceManager().get_balance(player=player)
        return [ServerMessage(player, f"Your current balance is ${balance:.2f}")]
