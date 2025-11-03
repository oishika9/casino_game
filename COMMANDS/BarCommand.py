from ..imports import *
from ..BALANCE.PlayerBalance import *
from ..COMMANDS.BalanceCommand import *

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from coord import Coord
    from maps.base import Map
    from tiles.base import MapObject
    from tiles.map_objects import *
    from command import MenuCommand
from typing import List

class BarCommand(MenuCommand):
    name = 'bar command'
    def __init__(self, price: float):
        """
        Initialises the BarCommand with the specified prices for drinks

        @Preconditions:
            - price must be a positive float

        @param price (float): The cost of the drink
        """
        assert price >= 0.0, 'Price must be positive' 
        self.price = price


    def execute(self, context, player) :
        """
        Executes the bar command by decrementing the drink price from the player's balance and returning the resulting messages
        and also adding the observers for appropriate observer notifications

        @Preconditions:
            - BalanceManager must be properly initialised
            - The player must be a valid HumanPlayer

        @param context: The current game context
        @param player: The player purchasing the drink
        @return (list): A list of messages showing the result of the transaction
        """
        messages = []
        balance = BalanceManager()


        # Create observers for this interaction
        se_observer = SoundEffectObserver(player)
        be_observer = BalanceEffectObserver(player, player)
        balance.register_observer(se_observer)
        balance.register_observer(be_observer)


        msg = balance.decrease_balance(self.price, BalanceChangeReason.DRINK, player=player)
        messages.append(
            EmoteMessage(sender = player, recipient = player, emote = "yellow_drink", emote_pos = Coord(8, 5))
        )
        messages.extend(msg)


        # Unregister observers after use to avoid duplication on future interactions
        balance.unregister_observer(se_observer)
        balance.unregister_observer(be_observer)


        #return [f"Enjoy your drink! You have {player.balance} left"]
        return messages if messages is not None else []





