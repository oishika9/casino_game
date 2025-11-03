from ..imports import *

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from coord import Coord
    from maps.base import Map
    from tiles.base import MapObject
    from tiles.map_objects import *
    from ..Cards.BlackjackComputer import BlackjackComputer

from enum import Enum

from ..BALANCE.PlayerBalance import BalanceManager, BalanceChangeReason, BalanceEffectObserver, SoundEffectObserver


class BlackjackDealCommand(MenuCommand):
    """
    menu choice that creates a new round if possible
    """
    name = "Deal"

    def __init__(self, blackjack_computer: "BlackjackComputer"):
        self.blackjack_computer = blackjack_computer

    def execute(self, context: "Map", player: "HumanPlayer") -> list[Message]:
        messages: list[Message] = []

        # start (or restart) a game for the player
        game = self.blackjack_computer.get_or_create_game(player)

        if game.active_round:
            # There's already a round in progress.
            # Let the user Fold or Bet or Quit first.
            messages.append(ServerMessage(player, "A round is already active!"))
            messages.append(MenuMessage(
                sender=self.blackjack_computer,
                recipient=player,
                menu_name="Blackjack Menu",
                menu_options=list(self.blackjack_computer.get_menu_options())
            ))
            return messages

        game.start_new_round()

        bm = BalanceManager()
        se_observer = SoundEffectObserver(player)
        be_observer = BalanceEffectObserver(self.blackjack_computer, player)
        bm.register_observer(se_observer)
        bm.register_observer(be_observer)

        current_balance = bm.get_balance(player=player)

        # check if the player can afford the ante
        if current_balance < game.ante:
            messages.append(ServerMessage(player, f"You need at least ${game.ante:.2f} to ante up!"))
            bm.unregister_observer(se_observer)
            bm.unregister_observer(be_observer)
            return messages

        cost_msgs = bm.decrease_balance(game.ante, reason=BalanceChangeReason.COST, player=player)
        messages.extend(cost_msgs)

        game.pot = game.ante * 2.0

        # show player's initial hand
        cards = game.get_player_cards()
        total = game.get_player_total()
        text = f"New round started!\nYour hand: {', '.join(cards)} (Total: {total})"
        messages.append(DialogueMessage(self.blackjack_computer, player, text, image=self.blackjack_computer.get_image_name()))

        bm.unregister_observer(se_observer)
        bm.unregister_observer(be_observer)

        # re-show the menu so they can choose hit, stand, or quit
        messages.append(MenuMessage(
            sender=self.blackjack_computer,
            recipient=player,
            menu_name="Blackjack Menu",
            menu_options=list(self.blackjack_computer.get_menu_options())
        ))
        return messages


class BlackjackHitCommand(MenuCommand):
    """
    menu choice that allows the player to hit (get a new card in blackjack game)
    """
    name = "Hit"

    def __init__(self, blackjack_computer: "BlackjackComputer"):
        self.blackjack_computer = blackjack_computer

    def execute(self, context: "Map", player: "HumanPlayer") -> list[Message]:
        messages: list[Message] = []
        game = self.blackjack_computer.get_or_create_game(player)

        # if no active round, prompt them to deal first
        if len(game.player_hand.cards) == 0:
            messages.append(DialogueMessage(self.blackjack_computer, player, "No active round. Choose 'Deal' first.", image=self.blackjack_computer.get_image_name()))
            messages.append(MenuMessage(
                self.blackjack_computer, player,
                "Blackjack Menu", list(self.blackjack_computer.get_menu_options())
            ))
            return messages

        # deal a card to the player
        new_card = game.player_hit()
        busted = game.is_busted()
        cards = game.get_player_cards()
        total = game.get_player_total()

        if busted:
            # player busts, immediately end round
            text = (
                f"You drew a {new_card} and busted!\n"
                f"Final hand: {', '.join(cards)} (Total: {total})"
            )
            messages.append(DialogueMessage(self.blackjack_computer, player, text, image=self.blackjack_computer.get_image_name()))
            winner = game.determine_winner()
            messages.append(DialogueMessage(self.blackjack_computer, player, f"Result: {winner} wins!", image=self.blackjack_computer.get_image_name()))
            self.blackjack_computer.remove_game(player)
        else:
            text = f"You drew a {new_card}.\nYour hand: {', '.join(cards)} (Total: {total})"
            messages.append(DialogueMessage(self.blackjack_computer, player, text, image=self.blackjack_computer.get_image_name()))

        # either way, show menu again
        messages.append(MenuMessage(
            self.blackjack_computer,
            player,
            "Blackjack Menu",
            list(self.blackjack_computer.get_menu_options())
        ))
        return messages


class BlackjackStandCommand(MenuCommand):
    """
    menu choice that allows the player to stand with their current hand
    """
    name = "Stand"

    def __init__(self, blackjack_computer: "BlackjackComputer"):
        self.blackjack_computer = blackjack_computer

    def execute(self, context: "Map", player: "HumanPlayer") -> list[Message]:
        messages: list[Message] = []
        game = self.blackjack_computer.get_or_create_game(player)

        if len(game.player_hand.cards) == 0:
            messages.append(DialogueMessage(self.blackjack_computer, player, "No active round. Choose 'Deal' first.", image=self.blackjack_computer.get_image_name()))
            messages.append(MenuMessage(
                self.blackjack_computer, player,
                "Blackjack Menu", list(self.blackjack_computer.get_menu_options())
            ))
            return messages

        bm = BalanceManager()
        se_observer = SoundEffectObserver(player)
        be_observer = BalanceEffectObserver(self.blackjack_computer, player)
        bm.register_observer(se_observer)
        bm.register_observer(be_observer)

        current_balance = bm.get_balance(player=player)

        # dealer turn
        dealer_busted = game.dealer_turn()
        dealer_cards = game.get_dealer_cards(reveal_all=True)
        dealer_total = game.get_dealer_total()

        # show final dealer hand
        text = f"Dealer's hand: {', '.join(dealer_cards)} (Total: {dealer_total})"
        messages.append(DialogueMessage(self.blackjack_computer, player, text, image=self.blackjack_computer.get_image_name()))

        # determine winner
        winner = game.determine_winner()
        messages.append(DialogueMessage(self.blackjack_computer, player, f"Result: {winner} wins!", image=self.blackjack_computer.get_image_name()))

        if winner == "Player":
            observer_msgs = bm.increase_balance(game.pot, reason=BalanceChangeReason.WIN, player=player)
            messages.extend(observer_msgs)

        bm.unregister_observer(se_observer)
        bm.unregister_observer(be_observer)

        self.blackjack_computer.remove_game(player)

        # show menu again (they can choose to 'deal' for a new round, or quit)
        messages.append(MenuMessage(
            self.blackjack_computer,
            player,
            "Blackjack Menu",
            list(self.blackjack_computer.get_menu_options())
        ))
        return messages


class BlackjackQuitCommand(MenuCommand):
    """
    menu choice that lets the user quit the menu and poker session
    """
    name = "Quit"

    def __init__(self, blackjack_computer: 'BlackjackComputer'):
        self.blackjack_computer = blackjack_computer

    def execute(self, context: "Map", player: "HumanPlayer") -> list[Message]:
        messages: list[Message] = []

        if player in self.blackjack_computer.player_games:
            self.blackjack_computer.remove_game(player)
            messages.append(ServerMessage(player, "You quit the Blackjack session."))
        else:
            messages.append(ServerMessage(player, "You're not currently in a Blackjack game."))

        return messages
