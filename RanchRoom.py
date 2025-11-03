from .HorseRaceBettingGame.HorseBettingManager import *
from .COMMANDS.HorseManagerCommands import *
from .COMMANDS.BalanceCommand import BalanceCommand
from .COMMANDS.HorseBetCommand import HorseBetCommand

from .NPCs.NPC_Bookmaker import HorseBookmaker
from .imports import *

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from coord import Coord
    from maps.base import Map
    from tiles.base import MapObject
    from tiles.map_objects import *


class RanchRoom(Map):
    def __init__(self) -> None:

        # Instantiate your HorseBettingManager
        self.horse_betting_manager = HorseBettingManager()


        super().__init__(
            name = "Ranch Room",
            description = "YEEHAW, Interact with the NPC to start horsebetting and check the sign for scoreboard!",
            size = (15, 15),
            entry_point = Coord(7, 14),
            background_tile_image = 'sand',
            ## HOPEFULLY THE CORRECT ONE
            # chat_commands =  [BalanceCommand],
            ## CHECK THIS ONE
            chat_commands = [HorseBetCommand, BalanceCommand]
        )
    
    def get_objects(self) -> list[tuple[MapObject, Coord]]:
        objects: list[tuple[MapObject, Coord]] = []

        # add a door
        door = Door('side1_entrance', linked_room="Casino Room")
        objects.append((door, Coord(10, 14)))

        # add houses
        house1 = IntDecor('house1')
        objects.append((house1,Coord(0,1)))

        #carry 13, 2
        carry = IntDecor('carry')
        objects.append((carry,Coord(11, 1)))

        # add rocks
        rocks = IntDecor('rocks')
        objects.append((rocks,Coord(9,0)))


        if not hasattr(self, 'bookmaker1'): 
            self.bookmaker1 = HorseBookmaker(self.horse_betting_manager, staring_distance = 2, dialogues = ["YEEHAW COWBOY! It's your lucky day!","Want to bet on a horse race?",])
        objects.append((self.bookmaker1, Coord(10,9)))

        # add a sign for the scoreboard 
        scoreboard = ScoreboardSign('signpost', 'There has been no races')
        objects.append((scoreboard, Coord(13,9)))
        

        return objects

class ScoreboardSign(Sign):
    """
    A signpost that, when interacted with, displays the current horse-race scoreboard.
    @param _text (str): The default text to display if the scoreboard is empty.
    """
    def __init__(self, image_name: str = 'signpost', text: str = '') -> None:
        super().__init__(image_name)
        self._text: str = text

    def player_interacted(self, player: "HumanPlayer") -> list[Message]:
        """
        Handle player interaction by showing the scoreboard or the default message.

        @param player: The HumanPlayer who interacted
        @returns: A list of DialogueMessage objects representing the scoreboard or the fallback text
        """
        scoreboard_observer = SignScoreboardObserver(player)
        msg = scoreboard_observer.show_result_sign(player)
        if msg is None:
            return [DialogueMessage(self, player, self._text, 'sign')]
        else:
            return msg 

