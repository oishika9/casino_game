from ..imports import *
import pytest
import random
from ..example_map import ExampleHouse
from ..DJbooth.DJ import DJ
#from CasinoRoyale.CasinoRoom import CasinoRoom
from ..BALANCE.PlayerBalance import BalanceManager, BalanceChangeReason
from ..GAME.SlotMachine import *
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from coord import Coord
    from Player import HumanPlayer


class DummyPlayer:
    """ HumanPlayer (just needs get_name()) """
    def __init__(self, name: str):
        self._name = name

    def get_name(self) -> str:
        return self._name


@pytest.fixture(autouse=True)
def reset_singletons():
    # Reset SlotMachine singleton
    SlotMachine._SlotMachine__instance = None
    # Reset BalanceManager state
    bm = BalanceManager()
    bm.balances.clear()
    bm.observers.clear()
    yield


def test_standard_strategy_no_win():
    strat = StandardStrategyWithWheel()
    win, text = strat.calculate_payout(10, ['A','B','C'])
    assert win == 0
    assert "No win" in text


def test_standard_strategy_win(monkeypatch):
    strat = StandardStrategyWithWheel()
    # force multiplier wheel to land on x3
    monkeypatch.setattr(random, "choice", lambda seq: 3)
    win, text = strat.calculate_payout(5, ['X','X','X'])
    assert win == 5 * 10 * 3
    assert "YOU WIN" in text
    assert "x3" in text


def test_jackpot_strategy_no_jackpot():
    strat = JackpotStrategy()
    win, text = strat.calculate_payout(10, ['(  <3  )']*3)
    assert win == 0
    assert "No win" in text


def test_jackpot_strategy_jackpot():
    strat = JackpotStrategy()
    reels = ['(  7  )','(  7  )','(  7  )']
    win, text = strat.calculate_payout(2, reels)
    assert win == 2 * 10 * 7
    assert text == "JACKPOT HIT!!"


def test_spin_reels_length_and_symbols():
    sm = SlotMachine(spin_cost=10)
    reels = sm.spin_reels()
    assert isinstance(reels, list)
    assert len(reels) == 3
    for symbol in reels:
        assert symbol in sm.symbols


def test_play_insufficient_funds():
    # spin_cost is default 10
    sm = SlotMachine(spin_cost=10)
    p = DummyPlayer("P1")
    # set player balance to 5
    bm = BalanceManager()
    bm.balances[p.get_name()] = 5.0

    msgs = sm.play(p)
    # should get a ServerMessage about insufficient funds
    assert any(
        isinstance(m, ServerMessage) and "Insufficient funds" in m._get_data().get("text","")
        for m in msgs
    )


def test_play_jackpot(monkeypatch):
    sm = SlotMachine(spin_cost=10)
    p = DummyPlayer("P2")
    # force reels to be jackpot
    monkeypatch.setattr(sm, "spin_reels", lambda: ['(  7  )']*3)

    msgs = sm.play(p)
    # must include a DialogueMessage with "JACKPOT"
    assert any(
        isinstance(m, DialogueMessage) and "JACKPOT" in m._get_data().get("dialogue_text","")
        for m in msgs
    )
    # balance should have increased
    bm = BalanceManager()
    assert bm.get_balance(player=p) > 1000.0


def test_play_standard_win(monkeypatch):
    '''
    Tests the strategy for standard win that has a payout multiplier
    '''
    sm = SlotMachine(spin_cost=10)
    p = DummyPlayer("P3")
    # force a standard match
    monkeypatch.setattr(sm, "spin_reels", lambda: ['(  <3  )']*3)
    # force multiplier wheel
    monkeypatch.setattr(random, "choice", lambda seq: 2)

    msgs = sm.play(p)
    # must include a DialogueMessage with "YOU WIN"
    assert any(
        isinstance(m, DialogueMessage) and "YOU WIN" in m._get_data().get("dialogue_text","")
        for m in msgs
    )
    # net change
    bm = BalanceManager()
    assert bm.get_balance(player=p) == 1000 - 10 + 200


def test_slotmachine_utility_clone():
    util = SlotMachineUtility(spin_cost=7)
    clone = util.clone()
    # should be distinct objects
    assert clone is not util
    # but same spin_cost on their slot_machine
    assert clone.slot_machine.spin_cost == util.slot_machine.spin_cost
