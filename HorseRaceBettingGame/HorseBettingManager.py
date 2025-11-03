from .BandOfHorses import BandOfHorses
from ..imports import *
from typing import TYPE_CHECKING
from ..BALANCE.PlayerBalance import *

if TYPE_CHECKING:
    from coord import Coord
    from maps.base import Map
    from tiles.base import MapObject
    from tiles.map_objects import *
    from resources import get_resource_path
    from message import Message, DialogueMessage, EmoteMessage, SoundMessage


class HorseBettingObserver(ABC):
    @abstractmethod
    def update_scoreboard(self, winning_horse: int) -> list:
        """
        This method is called when a race is finished and the winning horse is determined

        Preconditions:
            - winning_horse must be an integer corresponding to a valid horse number

        @param winning_horse (int): The winning horse's number.
        @return (list): A list of messages to be displayed (typically DialogueMessage instances)
        """
        pass


class SignScoreboardObserver(HorseBettingObserver):
    __instance = None


    def __new__(cls, player):
        if cls.__instance is None:
            cls.__instance = super(SignScoreboardObserver, cls).__new__(cls)
        return cls.__instance


    def __init__(self, player):
        # Only initialize once
        if not hasattr(self, 'initialized'):
            self.horse_wins = {i: 0 for i in range(1, 6)}
            self.player = player
            self.initialized = True
            self.scoreboard = None


    def update_scoreboard(self, winning_horse: int) -> list:
        """
        Updates the scoreboard with the result of the race by incrementing the win count for the winning horse.
        Constructs a scoreboard string and returns it as a DialogueMessage

        Preconditions:
            - winning_horse must be an integer corresponding to a valid horse number (1-5)
            - self.horse_wins must have been initialized properly

        @param winning_horse (int): The winning horse's number.

        @return (list): A list containing a DialogueMessage with the updated scoreboard
        """
        if winning_horse in self.horse_wins:
            self.horse_wins[winning_horse] += 1

        header = "Horse Scoreboard:"
        items = [f"Horse {horse}: {wins} wins" for horse, wins in self.horse_wins.items()]
        lines = []
        i = 0
        while i < len(items):
            line = " ".join(items[i:i+2])
            lines.append(line)
            i += 2
        self.scoreboard = header + "\n" + "\n".join(lines)

        message = DialogueMessage(
            self.player,
            self.player,
            text=self.scoreboard,
            image='sign'
        )
        return [message]


    def show_result_sign(self, player) -> list:
        """
        This method returns a message displaying the current scoreboard

        Preconditions:
            - The scoreboard has been initialized by a previous call to update_scoreboard

        @param player: The player to whom the scoreboard message will be sent
        @return (list): A list containing a DialogueMessage with the scoreboard, or None if no scoreboard exists
        """
        if self.scoreboard is None:
            return None 
        else: 
            return [DialogueMessage(self.player, self.player, self.scoreboard, 'sign')]


class HorseBettingManager:
    __instance = None


    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super(HorseBettingManager, cls).__new__(cls)
        return cls.__instance


    def __init__(self):
        if not hasattr(self, 'initialized'):
            self.band = BandOfHorses()
            self.player_choices = {}
            self.singular_player_choice = 0
            self.bet = 50 
            # List for scoreboard observers
            self.scoreboard_observers = []  # List[HorseBettingObserver]
            self.initialized = True


    def register_scoreboard_observer(self, observer: HorseBettingObserver) -> None:
        """
        Registers a scoreboard observer to receive updates after a race

        Preconditions:
            - observer must be an instance of HorseBettingObserver

        @param observer (HorseBettingObserver): The observer to register
        @return None
        """
        if observer not in self.scoreboard_observers:
            self.scoreboard_observers.append(observer)


    def unregister_scoreboard_observer(self, observer: HorseBettingObserver) -> None:
        """
        Unregisters a scoreboard observer so it no longer receives race updates

        Preconditions:
            - observer must be currently registered

        @param observer (HorseBettingObserver): The observer to unregister
        @return: None
        """
        if observer in self.scoreboard_observers:
            self.scoreboard_observers.remove(observer)


    def notify_scoreboard_observers(self, winning_horse: int) -> list:
        """
        Notifies all registered scoreboard observers with the winning horse number and collects their messages

        Preconditions:
            - winning_horse must be an integer corresponding to a valid horse number

        @param winning_horse (int): The winning horse's number
        @return (list): A combined list of messages from all observers
        """
        messages = []
        for observer in self.scoreboard_observers:
            msgs = observer.update_scoreboard(winning_horse)
            if msgs:
                messages.extend(msgs)
        return messages


    ## SAVE THE PLAYER'S HORSE CHOICE
    def set_player_choice(self, player, horse_number: int) -> None:
        """
        This methods sets the player's chosen horse

        Preconditions:
            - player must have a method get_name() that returns a unique identifier
            - horse_number should be a valid integer corresponding to a horse

        @param player: The player who made the choice
        @param horse_number (int): The number of the horse chosen by the player
        @return: None
        """
        self.player_choices[player.get_name()] = horse_number
        

    def get_player_choice(self, player) -> int:
        """
        This method is used to retrieve the player's horse choice

        Preconditions:
            - player must have a method get_name() that returns a unique identifier

        @param player: The player whose choice is to be retrieved
        @return: The number of the horse chosen by the player
        """
        return self.player_choices.get(player.get_name(), -1)


    def set_bet(self, player, bet_amount: int) -> list[DialogueMessage]:
        """
        This method is used to set the bet amount for the player

        Preconditions:
            - bet_amount should be a positive number

        @param player: The player who is placing the bet
        @param bet_amount: The amount to be bet
        @return: A list of messages to be displayed
        """
        messages = []
        self.bet = bet_amount
        return messages


    def get_bet(self):
        """
        This method is used to retrieve the bet amount for the player

        @return: The amount bet by the player
        """
        return self.bet


    def option_horse(self, player, horse_number: int) -> list[DialogueMessage]:
        """
        This method is used for the player to choose a horse to bet on

        Preconditions:
            - horse_number should be an integer corresponding to a valid horse in the band

        @param player: The player who is choosing the horse
        @param horse_number: The number of the horse chosen by the player
        @return: A list of messages to be displayed
        """
        self.horse_number = horse_number

        return [
            DialogueMessage(
                sender=player,
                recipient=player,
                text=f"Let the race begin!",
                image="player2"
            )]


    def process_bet(self, player, bet : int) -> list[Message]:
        """
        This method is used to process the bet placed by the player and display the results

        Preconditions:
            - The player must have already selected a horse
            - bet should be a valid positive number

        @param player: The player who placed the bet
        @param bet: The amount bet by the player
        @return: A list of messages to be displayed
        """
        messages = []
        if bet == None:
            bet_amount = self.bet
        else:
            bet_amount = bet


        # Countdown
        messages.append(DialogueMessage(sender=player, recipient=player, text="3", image="player2"))
        messages.append(DialogueMessage(sender=player, recipient=player, text="2", image="player2"))
        messages.append(DialogueMessage(sender=player, recipient=player, text="1", image="player2"))
        messages.append(SoundMessage(player, 'gunshot'))
        messages.append(DialogueMessage(sender=player, recipient=player, text="GO!", image="player2"))
        

        # horse_number is not used anymore
        horse_number = self.horse_number

        bm = BalanceManager()
        # Create observers for this interaction.
        se_observer = SoundEffectObserver(player)
        be_observer = BalanceEffectObserver(player, player)
        bm.register_observer(se_observer)
        bm.register_observer(be_observer)


        # Display the horse emote and the sound before the race results are shown
        messages.append(
            EmoteMessage(sender = player, recipient = player, emote = "smaller_horse.png", emote_pos = Coord(9, 5))
        )
        messages.append(
            SoundMessage(recipient = player, sound_path = "horse_race", volume = 0.8)
        )


        # Run the race and determine the winner
        result_band = self.band.figure_out_winner()
        horses = result_band._get_horses()  # get the list of horses after the race
        winning_horse = horses[0]


        # If the player's horse is the winner, they win money; otherwise they've lost their bet
        # Incrementing or decrementing the player's balance depending on the outcome of their bet
        if winning_horse.get_number() == self.get_player_choice(player):
            win_amount = bet_amount * 3
            messages.append(
                DialogueMessage(
                    sender = player,
                    recipient = player,
                    text = f"Well done! You've won {win_amount} credits!",
                    image = "player2"
                )
            )
            obs = BalanceManager().increase_balance(win_amount, reason=BalanceChangeReason.WIN, player=player)
            #messages.extend(obs)
        else:
            messages.append(
                DialogueMessage(
                    sender = player,
                    recipient = player,
                    text = f"You've lost {bet_amount} credits... better luck next time!",
                    image = "player2"
                )
            )
            
            obs = BalanceManager().decrease_balance(bet_amount, reason=BalanceChangeReason.LOSE, player=player)
            #messages.extend(obs)

        
        scoreboard_msgs = self.notify_scoreboard_observers(winning_horse.get_number())
        messages.extend(obs)
        messages.append(
            SoundMessage(recipient = player, sound_path = "horse", volume = 0.8)
        )
        messages.extend(scoreboard_msgs)
        bm.unregister_observer(se_observer)
        bm.unregister_observer(be_observer)
        self.set_bet(player, bet_amount=50)
        
        return messages
