
from ..imports import *
from typing import TYPE_CHECKING
from ..NPCs.NPC_Bookmaker import *
if TYPE_CHECKING:
    from coord import Coord
    from maps.base import Map
    from tiles.base import MapObject
    from tiles.map_objects import *
    from ..command import MenuCommand, ChatCommand
    from ..message import MenuMessage, DialogueMessage



class HorseBetCommand(ChatCommand):
    name = "bet_horse"
    desc = "Place a bet on the horse race. Usage: /bet_horse/<amount>. You can also check your balance with /balance."


    @classmethod
    def matches(cls, command_text: str) -> bool:
        """
        Determine whether the provided command text matches the expected format

        Preconditions:
            - command_text is a non-empty string

        @param command_text (str): The full text of the command entered by the player
        @return (bool): True if command_text starts with 'bet_horse/', False otherwise
        """
        return command_text.startswith("bet_horse/")


    def execute(self, command_text: str, context, player) -> list:
        """
        Execute the horse bet command by parsing the bet amount and updating the bet

        Preconditions:
            - The player must be in a state where a bet is expected (e.g. waiting for a bet NPC)
            - command_text must follow the format '/bet_horse/<amount>'

        @param command_text (str): The command text entered by the player
        @param context: The execution context (game state, etc.)
        @param player: The player object issuing the command
        @return (list): A list of messages (e.g., DialogueMessage or ServerMessage) to be sent to the player
        """
        messages = []

        ## NEED SOME ERROR HANDLING HERE AND/OR TYPE CHECKING
        bet_amount = float(command_text[10:].strip())

        # BET LOGIC
        npc_id = player.get_state('waiting_for_bet_npc')
        if npc_id is None:
            return [ServerMessage(player, "No one is for you to bet")]
        else:
            bookmaker = player.get_current_room().bookmaker1
            if bookmaker is None:
                return [ServerMessage(player, "No one is asking for you to bet")]

        return HorseBettingManager().set_bet(player, bet_amount)