from ..imports import *
from abc import ABC, abstractmethod
import random

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from coord import Coord
    from maps.base import Map
    from tiles.base import MapObject
    from tiles.map_objects import *

from typing import List
from ..BALANCE.PlayerBalance import *  
import copy
from typing import TYPE_CHECKING, List, Tuple




# STRATEGY PATTERN FOR SLOT MACHINE
class SlotMachineStrategy(ABC):
    @abstractmethod
    def calculate_payout(self, spin_cost: int, reels: List[str]) -> Tuple[int, str]:
        """
        Calculate the payout for the spin.

        Parameters:
            spin_cost (int): The cost per spin.
            reels (List[str]): List of symbols obtained from spinning.

        Returns:
            Tuple[int, str]: A tuple containing the win amount and an outcome message.
        
        Preconditions:
            - spin_cost must be non-negative.
        Postconditions:
            - The returned win amount is >= 0.
        """
        pass


class StandardStrategyWithWheel(SlotMachineStrategy):
    def calculate_payout(self, spin_cost: int, reels: List[str]) -> Tuple[int, str]:
        base_win = spin_cost * 10
        # Check for standard win (all symbols match).
        if reels[0] == reels[1] == reels[2]:
            # Simulate multiplier wheel narrative.
            multiplier = random.choice([1, 2, 3])
            total_win = base_win * multiplier
            outcome_text = (
                "Spinning the multiplier wheel...\n"
                "Wheel in motion: x1 ... x2 ... x3 ...\n"
                f"It lands on x{multiplier}! YOU WIN!!"
            )
            assert total_win >= 0, "Calculated win amount must be non-negative."
            return (total_win, outcome_text)
        else:
            return (0, "No win, better luck next time.")


class JackpotStrategy(SlotMachineStrategy):
    def calculate_payout(self, spin_cost: int, reels: List[str]) -> Tuple[int, str]:
        # Check for jackpot condition.
        if reels == ['(  7  )', '(  7  )', '(  7  )']:
            total_win = spin_cost * 10 * 7  # 7x win amount for jackpot.
            assert total_win >= 0, "Calculated win amount must be non-negative."
            return (total_win, "JACKPOT HIT!!")
        else:
            return (0, "No win, better luck next time.")


# SLOT MACHINE IMPLEMENTATION USING STRATEGY PATTERN
class SlotMachine():
    """
    Singleton SlotMachine class implementing a slot machine game using strategy pattern.

    Attributes:
        spin_cost (int): The cost per spin.
        symbols (List[str]): List of symbols that can appear on the reels.
        messages (List[Message]): List to accumulate messages during a spin.
        strategy (SlotMachineStrategy): The current payout strategy.
    """
    __instance = None

    def __new__(cls, spin_cost: int = 10) -> "SlotMachine":
        if cls.__instance is None:
            cls.__instance = super(SlotMachine, cls).__new__(cls)
        return cls.__instance

    def __init__(self, spin_cost: int = 10) -> None:
        """
        Initialize the SlotMachine instance.
        
        Preconditions:
            - spin_cost must be >= 0.
        Postconditions:
            - The slot machine is initialized with a list of symbols and a default strategy.
        """
        if not hasattr(self, 'initialized'):
            assert spin_cost >= 0, "Spin cost must be non-negative."
            self.spin_cost: int = spin_cost
            self.symbols: List[str] = ['(  <3  )', '(  :p  )', '( ~*~ )', '(  <>  )', '(  7  )']
            self.messages: List["Message"] = []  # Clear message list.
            self.strategy: SlotMachineStrategy = StandardStrategyWithWheel()
            self.initialized = True

    def set_strategy(self, strategy: SlotMachineStrategy) -> None:
        """
        Set the payout strategy for the slot machine.
        
        Parameters:
            strategy (SlotMachineStrategy): A strategy instance.
        """
        assert isinstance(strategy, SlotMachineStrategy), "Strategy must be a SlotMachineStrategy instance."
        self.strategy = strategy

    def get_image_name(self) -> str:
        """
        Get the image name representing the slot machine.
        
        Returns:
            str: The image name.
        """
        return "slot_machine3"

    def spin_reels(self) -> List[str]:
        """
        Spin the slot machine reels with weighted probabilities.
        
        Returns:
            List[str]: List of 3 symbols representing the spin result.
        
        Postconditions:
            - The returned list has exactly 3 symbols.
        """
        # Define weights to increase the odds of winning.
        weights: List[float] = [0.7, 0.125, 0.125, 0.025, 0.025]
        reels = random.choices(self.symbols, weights=weights, k=3)
        assert len(reels) == 3, "Reels must contain exactly 3 symbols."
        return reels

    def play_spin(self, player: "HumanPlayer", sender: object = None) -> bool:
        """
        Play a single spin of the slot machine.
        
        Parameters:
            player (HumanPlayer): The player who initiates the spin.
            sender (object): The sender of messages (defaults to self if None).
        
        Returns:
            bool: True if the spin was successful; False otherwise.
        
        Preconditions:
            - player must be a valid HumanPlayer.
        Postconditions:
            - Messages list is populated with results.
        """
        if sender is None:
            sender = self

        # Clear previous messages.
        self.messages = []
        bm = BalanceManager()
        current_balance = bm.get_balance(player=player)
        self.messages.append(DialogueMessage(sender, player, f"Starting balance: ${current_balance:.2f}", self.get_image_name()))

        # Check sufficient funds.
        if current_balance < self.spin_cost:
            self.messages.append(ServerMessage(player, "Insufficient funds to spin!"))
            return False

        # Deduct the spin cost.
        observer_msgs = bm.decrease_balance(self.spin_cost, reason=BalanceChangeReason.COST, player=player)
        self.messages.extend(observer_msgs)

        # Display spin initiation messages.
        self.messages.append(SoundMessage(player, 'playing'))
        self.messages.append(DialogueMessage(sender, player, "PLAY: (  X  )   (  X  )   (  X  )", self.get_image_name()))

        # Spin the reels.
        reels = self.spin_reels()
        result_string = "  ".join(reels)
        self.messages.append(DialogueMessage(sender, player, f"Reels: {result_string}", self.get_image_name()))

        # Choose strategy based on reels.
        if reels == ['(  7  )', '(  7  )', '(  7  )']:
            self.set_strategy(JackpotStrategy())
        else:
            self.set_strategy(StandardStrategyWithWheel())

        # Calculate payout.
        win_amount, outcome_text = self.strategy.calculate_payout(self.spin_cost, reels)
        if win_amount > 0:
            # For jackpot, use a different reason.
            if outcome_text == "JACKPOT HIT!!":
                observer_msgs = bm.increase_balance(win_amount, reason=BalanceChangeReason.JACKPOT, player=player)
            else:
                self.messages.append(SoundMessage(player, 'wheel'))
                observer_msgs = bm.increase_balance(win_amount, reason=BalanceChangeReason.WIN, player=player)
            self.messages.append(DialogueMessage(sender, player, outcome_text, self.get_image_name()))
            self.messages.extend(observer_msgs)
        else:
            observer_msgs = bm.decrease_balance(0, reason=BalanceChangeReason.LOSE, player=player)
            self.messages.append(DialogueMessage(sender, player, outcome_text, self.get_image_name()))
            self.messages.extend(observer_msgs)

        current_balance = bm.get_balance(player=player)
        self.messages.append(ServerMessage(player, f"Current balance: ${current_balance:.2f}"))
        self.messages.append(ServerMessage(player, "Game over!"))
        return True

    def play(self, player: "HumanPlayer", sender: object = None) -> List["Message"]:
        """
        Play the slot machine game and return the list of messages.
        
        Parameters:
            player (HumanPlayer): The player who plays.
            sender (object): The sender of messages (defaults to self if None).
        
        Returns:
            List[Message]: The messages resulting from the spin.
        """
        if sender is None:
            sender = self
        self.play_spin(player, sender=sender)
        return self.messages


# SLOT MACHINE UTILITY OBJECT

class SlotMachineUtility(UtilityObject):
    """
    Utility object that integrates the slot machine game into a room.

    When a player interacts with this object, the slot machine game is started and
    relevant messages are returned.
    """
    def __init__(self, image_name: str = 'slot_machine3', spin_cost: float = 10, player: object = None) -> None:
        """
        Initialize the SlotMachineUtility

        Parameters:
            image_name (str): The image identifier for the utility
            spin_cost (float): The cost per spin
            player (object): Optional player reference for observer registration
        """
        super().__init__(image_name, passable=False)
        self.slot_machine: SlotMachine = SlotMachine(spin_cost)

    def player_interacted(self, player: "HumanPlayer") -> List["Message"]:
        """
        Trigger the slot machine game when the player interacts

        @Parameters:
            player (HumanPlayer): The interacting player

        @Returns:
            List[Message]: A list of messages resulting from playing the game
        """
        bm = BalanceManager()
        # Create observers for this interaction.
        se_observer = SoundEffectObserver(player)
        be_observer = BalanceEffectObserver(self, player)
        bm.register_observer(se_observer)
        bm.register_observer(be_observer)

        messages: List["Message"] = []
        messages.append(DialogueMessage(self, player, "Welcome to the Slot Machine!", self.get_image_name()))
        slot_messages = self.slot_machine.play(player, sender=self)
        messages.extend(slot_messages)

        # Unregister observers after use to prevent duplication in subsequent interactions.
        bm.unregister_observer(se_observer)
        bm.unregister_observer(be_observer)
        return messages

    def clone(self) -> "SlotMachineUtility":
        """
        Create a deep copy of this SlotMachineUtility, allows players to interact with multiple SlotMachineUtility Objects without 
        creating a new one from scratch each time.
        """
        return copy.deepcopy(self)