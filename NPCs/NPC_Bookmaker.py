from ..imports import *

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ..coord import Coord
    from ..maps.base import Map
    from ..tiles.base import MapObject
    from ..tiles.map_objects import SelectionInterface, SenderInterface
    from ..NPC import NPC
    from ..message import Message, DialogueMessage, MenuMessage

from ..COMMANDS.HorseManagerCommands import *


from ..BALANCE.PlayerBalance import *  

class HorseBookmaker(NPC):
    """
    An NPC that asks the player if they want to play a horse betting game
    If the player agrees, the NPC will respond and start a horse betting game through menu options
    If the player declines, the NPC will respond and do nothing
    """
        
    def __init__(self, horse_manager, staring_distance: int = 0, dialogues: list = []) -> None:
        
        super().__init__(
            name = "The Bookmaker",
            image = "player2", # Need to add an image for the bookmaker
            encounter_text = dialogues[0],
            facing_direction = "down",
            staring_distance = staring_distance,
            bg_music = "desert"
        )
        # Keeps track of the NCP's dialogues with the player
        self.dialogues = dialogues
        # Tracks which line of dialogue to send to the player
        self.dialogue_index = 0

        # Flag to keep track of the player's interaction with the NPC
        self.__interaction_done = False
        # Flag to keep track of whether the player's input has been given to the NPC or not
        self.__awaiting_input = False
        self.horse_manager = horse_manager    
    
    def player_interacted(self, player: "HumanPlayer") -> list[Message]:
        messages: list[Message] = []

        # Interaction is finished, do nothing
        if self.__interaction_done:
            # SO THAT YOU CAN INTERACT WITH THE NPC MORE THAN ONCE
            self.__interaction_done = False
            return messages 
        
        # If there are more dialogues to show
        if self.dialogue_index < len(self.dialogues):
            messages.append(
                DialogueMessage(self, player, self.dialogues[self.dialogue_index], self.get_image_name())
            )
            self.dialogue_index += 1
        # If there are no more dialogues than prompt the player to play the game
        else:
            # Create the menu object
            menu_obj = BookmakerMenu(self.horse_manager)
        
            # Attach the menu to the player
            player.set_current_menu(menu_obj)
            msg = menu_obj.player_interacted(player)
            messages.extend(msg)

            self.__interaction_done = True
        return messages

    def npc_process_bet(self, player: "HumanPlayer", bet_amount : int) -> list[Message]:

        messages = []
        scoreboard_observer = SignScoreboardObserver(player)
        HorseBettingManager().register_scoreboard_observer(scoreboard_observer)

        msg = self.horse_manager.set_bet(player, bet_amount)
        messages.extend(msg)
        msg3 = self.horse_manager.process_bet(player, bet_amount)
        messages.extend(msg3)

        self.dialogue_index = 0  #Reset conversation if needed.
        self.__interaction_done = True 
        
        return messages

class BookmakerMenu(Computer):
    """
    A computer object that presents the menu to bet in the horse betting game
    """
    def __init__(self, manager):
        self.manager = manager

        menu_options = {
            'yes': HorseManagerYesCommand(manager),
            'no': HorseManagerNoCommand(manager)
        }
        super().__init__(image_name="empty", menu_name="Horse Bet Menu", menu_options=menu_options)

