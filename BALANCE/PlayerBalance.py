
from ..imports import *
from abc import ABC, abstractmethod

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from coord import Coord
    from maps.base import Map
    from tiles.base import MapObject
    from tiles.map_objects import *

from enum import Enum
from typing import Optional, List, Dict


#DETERMINES THE CAUSE OF BALANCE CHANGES
class BalanceChangeReason(Enum):
    """Reasons for why a balance change occurred."""

    WIN = "win"
    LOSE = "lose"
    JACKPOT = "jackpot"
    DRINK = "drink"
    COST = "cost"
    BET = "bet"
    TIE = "tie"


#OBSERVER - EVERY OBSERVER WILL HAVE TO HAVE AN update_balance METHOD
class BalanceObserver(ABC):
    """Observer interface for receiving balance change notifications."""

    @abstractmethod
    def update_balance(self, new_balance: float, change: float, reason: BalanceChangeReason = None) -> List:
        """
        Called when the player's balance changes
        @param new_balance: The updated balance
        @param change: The change in balance (>=0 for win, <=0 for loss/cost)
        @param reason: The reason for the balance change
        """
        pass


class BalanceManager:
    """
    Singleton manager for per-player balances and observer notifications.
    """
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super(BalanceManager, cls).__new__(cls)
        return cls.__instance

    def __init__(self):
        if not hasattr(self, 'initialized'):
            #self.balance = 1000.0
            self.balances: Dict[str, float] = {}
            self.observers: List[BalanceObserver] = []  # List of BalanceObserver objects
            self.initialized = True


    def register_observer(self, observer: BalanceObserver) -> None:
        """
        Register an observer to be notified on balance changes

        :param observer: The observer to register

        @Preconditions:
            - observer must implement BalanceObserver
        """
        assert isinstance(observer, BalanceObserver), "observer must be BalanceObserver"
        if observer not in self.observers:
            self.observers.append(observer)

    def unregister_observer(self, observer: BalanceObserver) -> None:
        """Removes Observer from the list observers"""
        if observer in self.observers:
            self.observers.remove(observer)

    #USED TO NOTIFY THE OBSERVERS OF A CHANGE IN BALANCE
    def notify_observers(self, change: float, reason: BalanceChangeReason = None, player: Optional["HumanPlayer"] = None) -> List:
        """
        Notify all registered observers of a balance change

        @param change (float): The change in balance.
        @param reason (BalanceChangeReason, optional): The reason for the change
        @param player (Optional[HumanPlayer]): the player's whose balance has been changed

        @Returns:
            List: A list of messages returned by the observers
        """

        messages = []
        new_balance = self.get_balance(player=player)
        for observer in self.observers:
            msgs = observer.update_balance(new_balance, change, reason)
            if msgs:
                messages.extend(msgs)
        return messages



    def _get_key(self, player: Optional["HumanPlayer"]) -> str:
        """
        Determine the key for the given player
        If no player is provided, use 'default'

        @Preconditions:
            - player is either None or has a get_name() method
        @Returns:
            str: The unique key for the player
        """
        if player is None:
            return "default"
        return player.get_name()


    def get_balance(self, player: Optional["HumanPlayer"] = None) -> float:
        """
        Get the balance for the given player
        If the player is not in the dictionary, initialize their balance to 1000.0

        @Parameters:
            player (Optional[HumanPlayer]): The player whose balance is requested

        @Returns:
            float: The current balance for the player
        """
        key = self._get_key(player)
        if key not in self.balances:
            self.balances[key] = 1000.0
        return self.balances[key]

    def increase_balance(self, amount: float, reason: BalanceChangeReason = None, player: Optional["HumanPlayer"] = None) -> List:
        """
        Increase the balance for the given player by the specified amount and notify observers

        @Parameters:
            amount (float): The amount to increase the balance
            reason (BalanceChangeReason, optional): The reason for the change
            player (Optional[HumanPlayer]): The player whose balance is to be increased

        @Returns:
            List: A list of messages from notifying observers

        @Preconditions:
            - amount must be non-negative.
            - If player is provided, it must have a get_name() method
        """
        assert amount >= 0, "Amount to increase must be non-negative."
        key = self._get_key(player)
        if key not in self.balances:
            self.balances[key] = 1000.0
        self.balances[key] += amount
        return self.notify_observers(amount, reason, player=player)

    def decrease_balance(self, amount: float, reason: BalanceChangeReason = None, player: Optional["HumanPlayer"] = None) -> List:
        """
        Decrease the balance for the given player by the specified amount and notify observers

        @Parameters:
            amount (float): The amount to decrease the balance
            reason (BalanceChangeReason, optional): The reason for the change
            player (Optional[HumanPlayer]): The player whose balance is to be decreased

        @Returns:
            List: A list of messages from notifying observers

        @Preconditions:
            - amount must be non-negative.
            - If player is provided, it must have a get_name() method
        """
        assert amount >= 0, "Amount to decrease must be non-negative"
        key = self._get_key(player)
        if key not in self.balances:
            self.balances[key] = 1000.0
        self.balances[key] -= amount
        return self.notify_observers(-amount, reason, player=player)


#BALANCE NOTIFIER
class BalanceEffectObserver(BalanceObserver):
    """Observer that sends DialogueMessages reflecting balance changes"""
    def __init__(self, sender, player) -> None:
        self.player = player
        if sender is None:
            self.sender = self
        else:
            self.sender = sender

    def update_balance(self, new_balance: float, change: float, reason: BalanceChangeReason = None) -> List:

        messages = []
        if change > 0:
                message = DialogueMessage(self.sender, self.player, f"After winning ${change:.2f}, your new balance is ${new_balance:.2f} ", self.sender.get_image_name())

        elif change <= 0:
            # SO THAT IT DOESN'T SHOW A NEGATIVE CHANGE BUT SIMPLY TELLS YOU HOW MUCH YOU LOST OR SPENT
            change = abs(change)
            if reason == BalanceChangeReason.DRINK:
                message = DialogueMessage(self.sender, self.player, f"Enjoy your drink! It will cost you ${change:.2f}, your new balance is ${new_balance:.2f} ", self.sender.get_image_name())
            elif reason == BalanceChangeReason.COST:
                message = DialogueMessage(self.sender, self.player, f"This game cost ${change:.2f}, your new balance is ${new_balance:.2f} ", self.sender.get_image_name())
            elif reason == BalanceChangeReason.BET:
                message = DialogueMessage(self.sender, self.player, f"You bet ${change:.2f} ", self.sender.get_image_name())
            elif reason == BalanceChangeReason.LOSE:
                message = DialogueMessage(self.sender, self.player, f"After losing ${change:.2f}, your new balance is ${new_balance:.2f} ", self.sender.get_image_name())
        else:
            message = None

        #IMPORTANT TO RETURN MESSAGES
        return [message] if message is not None else []


#OUR SOUND OBSERVER SO EVERYTIME BALANCE IS CHANGED THIS GETS NOTIFIED AND PLAYS A SOUND
class SoundEffectObserver(BalanceObserver):
    """Observer that plays sound effects on balance changes"""
    def __init__(self, player):
        self.player = player

    def update_balance(self, new_balance: float, change: float, reason: BalanceChangeReason = None) -> list:
        # Here, we'll return a list of SoundMessage objects.
        messages = []
        if change > 0:
            if reason == BalanceChangeReason.JACKPOT:
                message = SoundMessage(self.player, 'jackpot', repeat=False)
            else:
                message = SoundMessage(self.player, 'win', repeat=False)
        elif change <= 0:
            if reason == BalanceChangeReason.DRINK:
                message = SoundMessage(self.player, 'slurp', repeat=False)
            elif reason == BalanceChangeReason.COST or reason == BalanceChangeReason.BET:
                message = SoundMessage(self.player, 'cost', repeat=False)
            elif reason == BalanceChangeReason.LOSE:
                message = SoundMessage(self.player, 'lose', repeat=False)
            elif reason == BalanceChangeReason.TIE:
                message = SoundMessage(self.player, 'tie', repeat=False)
        else:
            message = None

        return [message] if message is not None else []
