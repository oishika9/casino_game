from ..imports import *

from .Hand import Hand
from .Deck import Deck
from .Blackjack import BlackjackGame

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from coord import Coord
    from maps.base import Map
    from tiles.base import MapObject
    from tiles.map_objects import *

from enum import Enum

from ..BALANCE.PlayerBalance import BalanceManager, BalanceChangeReason, BalanceEffectObserver, SoundEffectObserver

import copy














# NOT USED ANYMORE, PLEASE IGNORE














class BlackjackUtility(UtilityObject):
    def __init__(self, image_name: str = 'casino_table3', cost_to_play: float = 10.0):
        super().__init__(image_name, passable=False)
        self.cost_to_play = cost_to_play
        self.game = BlackjackGame()

    def player_interacted(self, player: "HumanPlayer") -> list:
        messages = []

        bm = BalanceManager()

        se_observer = SoundEffectObserver(player)
        be_observer = BalanceEffectObserver(self, player)
        bm.register_observer(se_observer)
        bm.register_observer(be_observer)

        current_balance = bm.get_balance(player=player)
        if current_balance < self.cost_to_play:
            # if not enough money, show message and exit
            messages.append(ServerMessage(player,
                f"You need at least ${self.cost_to_play:.2f} to play Blackjack!"))
            bm.unregister_observer(se_observer)
            bm.unregister_observer(be_observer)
            return messages

        # deduct the entry cost
        cost_msgs = bm.decrease_balance(self.cost_to_play, reason=BalanceChangeReason.COST, player=player)
        messages.extend(cost_msgs)

        # start a new Blackjack round
        self.game.start_new_round()

        # show the player’s initial cards in a dialogue
        player_cards = self.game.get_player_cards()
        messages.append(DialogueMessage(
            self,
            player,
            f"Your hand: {', '.join(player_cards)} (Total: {self.game.get_player_total()})",
            image="card_table"
        ))

        # autoplay for player (just to test)
        # will keep hitting if tota < 17
        while self.game.get_player_total() < 17:
            self.game.player_hit()
            busted = self.game.is_busted()
            if busted:
                break

        # dealer turn
        dealer_bust = self.game.dealer_turn()

        # show final results
        dealer_cards = self.game.get_dealer_cards(reveal_all=True)
        dealer_total = self.game.get_dealer_total()
        messages.append(DialogueMessage(
            self,
            player,
            f"Dealer's hand: {', '.join(dealer_cards)} (Total: {dealer_total})",
            image="card_table"
        ))

        # determine winner
        winner = self.game.determine_winner()
        if winner == "Player":
            # 2:1 payout:
            payout = self.cost_to_play * 2.0
            win_msgs = bm.increase_balance(payout, reason=BalanceChangeReason.WIN, player=player)
            messages.extend(win_msgs)
            messages.append(DialogueMessage(
                self,
                player,
                "You WIN!",
                image="card_table"
            ))
            messages.append(SoundMessage(player, 'win_sound'))
        elif winner == "Dealer":
            messages.append(DialogueMessage(
                self,
                player,
                "Dealer wins, better luck next time!",
                image="card_table"
            ))
            messages.append(SoundMessage(player, 'lose_sound'))
        else:
            # "push" i.e. tie, give money back
            push_msgs = bm.increase_balance(self.cost_to_play, reason=BalanceChangeReason.TIE, player=player)
            messages.extend(push_msgs)
            messages.append(DialogueMessage(
                self,
                player,
                "It's a tie! Your bet is returned.",
                image="card_table"
            ))


        # unregister observers to avoid duplication next time
        bm.unregister_observer(se_observer)
        bm.unregister_observer(be_observer)

        return messages

    #PROTOTYPE --------
    def clone(self):
        return copy.deepcopy(self)

