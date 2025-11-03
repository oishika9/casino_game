from ..imports import *
from ..NPCs.NPC_Bartender import WalkingBartender

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from coord import Coord
    from maps.base import Map
    from tiles.base import MapObject
    from tiles.map_objects import *
    from command import ChatCommand

from typing import List

class AgeChatCommand(ChatCommand):
    """
    ChatCommand that handles an '/age/<n>' input when an NPC is waiting for the player's age.
    """
    name = 'age'
    desc = 'Process numeric age input for an NPC waiting for age, in the format /age/<your_age>'

    @classmethod
    def matches(cls, command_text: str) -> bool:
        """
        Check if the input matches the age pattern.

        @return: True if it starts with "age/" and the remainder is all digits.
        """
        # This command matches if the command_text starts with "age/" and what follows is numeric.
        if command_text.startswith("age/"):
            age_part = command_text[4:]
            return age_part.isdigit()
        return False
    
    def execute(self, command_text: str, context: "Map", player: "HumanPlayer") -> List["Message"]:
        """
        Execute the age command by forwarding the numeric age to the awaiting NPC

        @Preconditions:
            - command_text must satisfy matches().

        @Postconditions:
            - If no NPC is awaiting age, returns a ServerMessage indicating so
            - Otherwise delegates to bouncer.process_player_input and returns its messages

        @return: List of Message
        """
        assert self.matches(command_text), f"Invalid age command"

        # Extract the numeric part after "age/"
        age_str = command_text[4:]
        npc_id = player.get_state('waiting_for_age_npc')
        if npc_id is None:
            return [ServerMessage(player, "No one is asking for your age right now.")]
        else:
            bouncer = player.get_current_room().bouncer
            if bouncer is None:
                return [ServerMessage(player, "No one is asking for your age right now.")]


        # Process the input using the NPC's method.
        return bouncer.process_player_input(player, age_str)

        


