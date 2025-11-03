from ..imports import *
from ..HorseRaceBettingGame.HorseBettingManager import *
#from ..NPCs.NPC_Bookmaker import *


from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from coord import Coord
    from maps.base import Map
    from tiles.base import MapObject
    from tiles.map_objects import *
    from ..command import MenuCommand, ChatCommand
    from ..message import MenuMessage, DialogueMessage
    
    
# As per the DJ Commands, all the commands are implemented as separate classes that inherit from either MenuCommand or ChatCommand


class HorseManagerYesCommand(MenuCommand):
    name = "yes"
    
    def __init__(self, horse_manager):
        """
        Initialise the command with a reference to the HorseBettingManager

        @param horse_manager: An instance of HorseBettingManager handling bet logic
        """
        self.horse_manager = horse_manager


    def execute(self, context, player) -> list:
        """
        Execute the 'yes' command to initiate the betting process

        Preconditions:
            - The player is in an interactive state that allows betting

        @param context: The current execution context
        @param player: The player initiating the command
        @return (list): A list of messages including prompts and menu displays for horse selection
        """
        messages = []

        messages.append(DialogueMessage(
                sender=player,
                recipient=player,
                text=f"Please place your bet using /bet_horse/<amount>. (Default is $50)",
                image="player2"
            ))

        messages.append(DialogueMessage(player, player, f"Choose which Horse to bet on:", player.get_image_name()))

        menu_obj = ChooseHorseMenu(self.horse_manager)  
        msg = menu_obj.player_interacted(player)
        messages.extend(msg)
        
        return messages


class HorseManagerNoCommand(MenuCommand):
    name = "no"
    
    def __init__(self, horse_manager):
        """
        Initialise the command with a reference to the HorseBettingManager

        @param horse_manager: An instance of HorseBettingManager handling bet logic
        """
        self.horse_manager = horse_manager


    def execute(self, context, player) -> list:
        """
        Execute the 'no' command, ending the betting interaction and exiting

        @param context: The current execution context
        @param player: The player who chose not to bet
        @return (list): A list of messages that exit the betting process
        """
        return [DialogueMessage(player, player, 'Not brave enough to take a risk aye?', player.get_image_name())]


class HorseChoiceCommand(MenuCommand):
    name = "horse_choice"
    
    def __init__(self, horse_manager, choice):
        """
        Initialise the command with the chosen horse option

        @param horse_manager: An instance of HorseBettingManager
        @param choice (str): The chosen horse number as a string
        """
        self.horse_manager = horse_manager
        self.chosen_option = choice


    def execute(self, context, player) -> list:
        """
        Execute the command to process the horse choice

        Preconditions:
            - The chosen option must be convertible to an integer

        @param context: The current execution context
        @param player: The player making the choice
        @return (list): A list of messages, including a prompt for a bet and further bet processing; if option is invalid, return an error message
        """
        messages = []

        try:
            horse_number = int(self.chosen_option)
        except (AttributeError, ValueError):
            return [DialogueMessage(player, player, "Invalid selection. Please try again.", "player2")]
        
        # Save the player's choice in the manager
        self.horse_manager.set_player_choice(player, horse_number)

        msg = self.horse_manager.option_horse(player, horse_number = horse_number)
        messages.extend(msg)

        bookmaker = player.get_current_room().bookmaker1
        if bookmaker is None:
            return [ServerMessage(player, "No one is asking for you to bet")]
            
        

        msg2 = bookmaker.npc_process_bet(player, HorseBettingManager().get_bet())
        messages.extend(msg2)

        return messages 


# MOVED HorseBetCommand() CLASS TO A DIFFERENT FILE


class ChooseHorseMenu(Computer):
    """
    Menu interface for selecting a horse to bet on; presents options for horses 1 through 5

    @param manager: An instance of HorseBettingManager that manages the betting logic
    """
    def __init__(self, manager):
        self.manager = manager

        menu_options = {
            "Horse 1": HorseChoiceCommand(manager, "1"), 
            "Horse 2": HorseChoiceCommand(manager, "2") , 
            "Horse 3": HorseChoiceCommand(manager, "3") , 
            "Horse 4": HorseChoiceCommand(manager, "4") , 
            "Horse 5": HorseChoiceCommand(manager, "5")
        }
        super().__init__(image_name="empty", menu_name="Horse Choose Menu", menu_options=menu_options)

