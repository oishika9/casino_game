from ..imports import *

from ..Cards.Hand import Hand
from ..Cards.Deck import Deck
from ..Cards.Card import Card, Rank
from ..Cards.OneCardPoker import OneCardPokerGame
from ..Cards.OneCardPokerStrategy import PokerStrategy

from typing import TYPE_CHECKING, Optional
if TYPE_CHECKING:
    from coord import Coord
    from maps.base import Map
    from tiles.base import MapObject
    from tiles.map_objects import *
    from command import MenuCommand
    from ..Cards.OneCardPokerComputer import OneCardPokerComputer

from enum import Enum

import random

from ..BALANCE.PlayerBalance import BalanceManager, BalanceChangeReason, BalanceEffectObserver, SoundEffectObserver

class OneCardDealCommand(MenuCommand):
    """
    menu choice that creates a new round if possible, with a fixed ante
    """
    name = "Deal"

    def __init__(self, poker_computer: "OneCardPokerComputer"):
        self.poker_computer = poker_computer

    def execute(self, context: "Map", player: "HumanPlayer") -> list[Message]:
        """
        @parameters:
            context: current map (unused but required by interface)
            player: HumanPlayer that interacted with the menu option

        @returns:
            list of Messages informing the user if a new round was able to start
        """
        messages = []
        game = self.poker_computer.get_or_create_game(player)

        if game.active_round:
            messages.append(ServerMessage(player, "A round is already active!"))
            messages.append(MenuMessage(
                self.poker_computer, player,
                "One-Card Poker Menu", list(self.poker_computer.get_menu_options())
            ))
            return messages

        game.start_new_round()

        bm = BalanceManager()
        se_observer = SoundEffectObserver(player)
        be_observer = BalanceEffectObserver(self.poker_computer, player)
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

        game.deal_cards()

        # show player's card
        if len(game.player_card) == 0:
            messages.append(ServerMessage(player, "No card was dealt. Something went wrong."))
        else:
            pc = game.player_card[0]
            add_n_before_rank = "n" if pc.rank.starts_with_vowel() else ""

            messages.append(DialogueMessage(
                self.poker_computer,
                player,
                f"You receive a{add_n_before_rank} {pc}.\nThe pot is now ${game.pot:.2f}.",
                image=self.poker_computer.get_image_name()
            ))

        bm.unregister_observer(se_observer)
        bm.unregister_observer(be_observer)

        messages.append(MenuMessage(
            self.poker_computer,
            player,
            "One-Card Poker Menu",
            list(self.poker_computer.get_menu_options())
        ))
        return messages


class OneCardBetCommand(MenuCommand):
    """
    menu choice that allows the player to bet a fixed amount and moving the round to showdown
    """
    name = "Bet"

    def __init__(self, poker_computer: "OneCardPokerComputer"):
        self.poker_computer = poker_computer

    def execute(self, context: "Map", player: "HumanPlayer") -> list[Message]:
        """
        @parameters:
            context: current map (unused but required by interface)
            player: HumanPlayer that interacted with the menu option

        @returns:
            list of Messages summarising the result and updating the balance

        @preconditions:
            - game.ai_card is a Card
        """
        messages = []
        game = self.poker_computer.get_or_create_game(player)

        if not game.active_round:
            messages.append(DialogueMessage(self.poker_computer, player, "No active round. Choose 'Deal' first.", image=self.poker_computer.get_image_name()))
            messages.append(MenuMessage(self.poker_computer, player,
                                        "One-Card Poker Menu",
                                        list(self.poker_computer.get_menu_options())))
            return messages

        assert game.ai_card is not None

        bm = BalanceManager()
        se_observer = SoundEffectObserver(player)
        be_observer = BalanceEffectObserver(self.poker_computer, player)
        bm.register_observer(se_observer)
        bm.register_observer(be_observer)

        current_balance = bm.get_balance(player=player)

        # Check if the player can afford the bet
        if current_balance < game.bet_amount:
            messages.append(ServerMessage(player, f"You need at least ${game.bet_amount:.2f} to bet!"))
            bm.unregister_observer(se_observer)
            bm.unregister_observer(be_observer)
            return messages

        cost_msgs = bm.decrease_balance(game.bet_amount, reason=BalanceChangeReason.BET, player=player)
        messages.extend(cost_msgs)

        game.pot += game.bet_amount

        game.strategy.record_player_bet()

        ai_card_rank = game.ai_card.get_rank()
        add_n_before_rank = "n" if ai_card_rank.starts_with_vowel() else ""

        # AI decides to call or fold based on strategy
        ai_calls = game.ai_decides_call()

        if ai_calls:
            game.pot += game.bet_amount

            messages.append(DialogueMessage(
                self.poker_computer,
                player,
                f"AI calls your bet! Pot is now ${game.pot:.2f}.\nTime for showdown...",
                image=self.poker_computer.get_image_name()
            ))

            winner = game.showdown()
            if winner == "Player":
                messages.append(DialogueMessage(self.poker_computer, player, f"You won the showdown! AI had a{add_n_before_rank} {ai_card_rank.value}", image=self.poker_computer.get_image_name()))
                observer_msgs = bm.increase_balance(game.pot, reason=BalanceChangeReason.WIN, player=player)
                messages.extend(observer_msgs)
            elif winner == "AI":
                messages.append(DialogueMessage(self.poker_computer, player, f"AI wins the showdown with a{add_n_before_rank} {ai_card_rank.value}", image=self.poker_computer.get_image_name()))
            else:
                observer_msgs = bm.increase_balance(game.pot, reason=BalanceChangeReason.TIE, player=player)
                messages.extend(observer_msgs)
                messages.append(DialogueMessage(self.poker_computer, player, "It's a tie. You get your pot back!", image=self.poker_computer.get_image_name()))

            game.active_round = False
        else:
            messages.append(DialogueMessage(
                self.poker_computer,
                player,
                f"AI folds a{add_n_before_rank} {ai_card_rank.value}! You take the pot.",
                image=self.poker_computer.get_image_name()
            ))
            observer_msgs = bm.increase_balance(game.pot, reason=BalanceChangeReason.WIN, player=player)
            messages.extend(observer_msgs)
            game.active_round = False

        bm.unregister_observer(se_observer)
        bm.unregister_observer(be_observer)

        messages.append(MenuMessage(
            self.poker_computer, player,
            "One-Card Poker Menu",
            list(self.poker_computer.get_menu_options())
        ))
        return messages


class OneCardFoldCommand(MenuCommand):
    """
    menu choice that folds the players hand, essentially surrendering their bets up to that point
    """
    name = "Fold"

    def __init__(self, poker_computer: "OneCardPokerComputer"):
        self.poker_computer = poker_computer

    def execute(self, context: "Map", player: "HumanPlayer") -> list[Message]:
        """
        @parameters:
            context: current map (unused but required by interface)
            player: HumanPlayer that interacted with the menu option

        @returns:
            MenuMessage to allow the user to continue with a new round
        """
        messages = []
        game = self.poker_computer.get_or_create_game(player)

        if not game.active_round:
            messages.append(DialogueMessage(self.poker_computer, player, "No active round. Choose 'Deal' first.", image=self.poker_computer.get_image_name()))
            messages.append(MenuMessage(
                self.poker_computer, player,
                "One-Card Poker Menu",
                list(self.poker_computer.get_menu_options())
            ))
            return messages

        game.strategy.record_player_fold()

        messages.append(DialogueMessage(
            self.poker_computer,
            player,
            "You folded. AI wins the pot.",
            image=self.poker_computer.get_image_name()
        ))
        game.active_round = False

        messages.append(MenuMessage(
            self.poker_computer, player,
            "One-Card Poker Menu",
            list(self.poker_computer.get_menu_options())
        ))
        return messages


class OneCardQuitCommand(MenuCommand):
    """
    menu choice that lets the user quit the menu and poker session
    """
    name = "Quit"

    def __init__(self, poker_computer: "OneCardPokerComputer"):
        self.poker_computer = poker_computer

    def execute(self, context: "Map", player: "HumanPlayer") -> list[Message]:
        """
        @parameters:
            context: current map (unused but required by interface)
            player: HumanPlayer that interacted with the menu option
        """
        messages = []
        if player in self.poker_computer.player_games:
            self.poker_computer.remove_game(player)
            messages.append(ServerMessage(player, "You quit the One-Card Poker session."))
        else:
            messages.append(ServerMessage(player, "You're not currently in a One-Card Poker game."))

        return messages
