import pytest

from ..imports import *
from ..example_map import ExampleHouse

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from coord import Coord
    from Player import HumanPlayer
from ..BALANCE.PlayerBalance import BalanceManager, BalanceObserver, BalanceChangeReason
from typing import List, Optional




class DummyObserver(BalanceObserver):
    """Capture notifications for assertions."""
    def __init__(self):
        self.notifications: List[tuple[float, float, BalanceChangeReason]] = []

    def update_balance(
        self,
        new_balance: float,
        change: float,
        reason: BalanceChangeReason = None) -> List[str]:
        # Record the notification
        self.notifications.append((new_balance, change, reason))
        # Return a dummy message
        return [f"Notified: {new_balance}, {change}, {reason}"]


class DummyPlayer:
    """ HumanPlayer (just needs get_name())."""
    def __init__(self, name: str):
        self._name = name

    def get_name(self) -> str:
        return self._name


@pytest.fixture(autouse=True)
def reset_balance_manager():
    """
    Before each test, clear out the singleton’s state so tests don't
    leak into one another.
    """
    bm = BalanceManager()
    bm.balances.clear()
    bm.observers.clear()


def test_get_balance_initializes_and_returns_default():
    """
    tests that if player is not already in dictionary then it is added 
    with a default amount of 1000
    """
    bm = BalanceManager()
    p = DummyPlayer("Alice")

    # First call should create and return 1000.0
    assert bm.get_balance(player=p) == 1000.0
    # Second call returns the same stored value
    assert bm.get_balance(player=p) == 1000.0

    # The 'default' key (None) also works
    assert bm.get_balance() == 1000.0


def test_increase_balance_updates_and_notifies():
    """
    Tests that after increase_balance() is called, the player's balance increases by that the given amount and it notifies the observers
    """
    bm = BalanceManager()
    p = DummyPlayer("Bob")
    obs = DummyObserver()
    bm.register_observer(obs)

    initial = bm.get_balance(player=p)
    msgs = bm.increase_balance(amount=200, reason=BalanceChangeReason.WIN, player=p)

    # Balance updated
    assert bm.get_balance(player=p) == initial + 200
    # Observer got correct tuple
    assert obs.notifications[-1] == (initial + 200, 200, BalanceChangeReason.WIN)
    # And our dummy return message is in the list
    assert any("Notified:" in m for m in msgs)

    bm.unregister_observer(obs)


def test_decrease_balance_updates_and_notifies():
    """
    Tests that after increase_balance() is called, the player's balance decreases by that the given amount and it notifies the observers
    """
    bm = BalanceManager()
    p = DummyPlayer("Charlie")
    obs = DummyObserver()
    bm.register_observer(obs)

    initial = bm.get_balance(player=p)
    msgs = bm.decrease_balance(amount=150, reason=BalanceChangeReason.COST, player=p)

    # Balance decreased
    assert bm.get_balance(player=p) == initial - 150
    # Observer got correct tuple (new_balance, negative change)
    assert obs.notifications[-1] == (initial - 150, -150, BalanceChangeReason.COST)
    assert any("Notified:" in m for m in msgs)

    bm.unregister_observer(obs)


def test_notify_observers_without_changing_balance():
    "Tests notify_oberservers"
    bm = BalanceManager()
    p = DummyPlayer("Dana")
    obs = DummyObserver()
    bm.register_observer(obs)

    msgs = bm.notify_observers(
        change=50,
        reason=BalanceChangeReason.DRINK,
        player=p
    )

    # Balance stays the same
    assert bm.get_balance(player=p) == 1000.0
    # Observer saw the notification
    assert obs.notifications[-1] == (1000.0, 50, BalanceChangeReason.DRINK)
    assert any("Notified:" in m for m in msgs)

    bm.unregister_observer(obs)
