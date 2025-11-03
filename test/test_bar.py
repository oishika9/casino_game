import pytest
from ..imports import *

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from coord import Coord
    from Player import HumanPlayer


from ..COMMANDS.BarCommand import BarCommand 
from ..BarRoom import BarMenuComputer
from ..BALANCE.PlayerBalance import *
#from CasinoRoyale.message import EmoteMessage, SoundMessage, DialogueMessage
from typing import List, Optional


class DummyPlayer:
    """HumanPlayer (needs get_name and get_image_name)."""
    def __init__(self, name: str):
        self._name = name

    def get_name(self) -> str:
        return self._name

    def get_image_name(self) -> str:
        return "dummy_image"


@pytest.fixture(autouse=True)
def reset_balance_manager():
    """
    Clear out the BalanceManager state before each test
    """
    bm = BalanceManager()
    bm.balances.clear()
    bm.observers.clear()


def test_bar_menu_computer_options():
    menu = BarMenuComputer()
    opts = getattr(menu, "_Computer__menu_options")

    expected = {
        'coke - $5.00': 5.00,
        'vodka coke - $17.00': 17.00,
        'vodka - $12.00': 12.00,
    }
    assert set(opts.keys()) == set(expected.keys())


@pytest.mark.parametrize("price,label", [
    (5.00, "Enjoy your drink! It will cost you $5.00, your new balance is $995.00 "),
    (17.00, "Enjoy your drink! It will cost you $17.00, your new balance is $983.00 "),
    (12.00, "Enjoy your drink! It will cost you $12.00, your new balance is $988.00 "),
])
def test_bar_command_execute_decrements_and_returns_messages(price: float, label: str):
    """
    BarCommand.execute should:
      - Deduct price from the player's balance
      - Return [EmoteMessage, SoundMessage, DialogueMessage]
      - The DialogueMessage text should match our expected label
    """
    p = DummyPlayer("Drinker")
    # ensure default balance is 1000
    bm = BalanceManager()
    assert bm.get_balance(player=p) == 1000.0

    cmd = BarCommand(price)
    msgs = cmd.execute(context=None, player=p)

    # must return at least three messages
    assert len(msgs) >= 3

    # first message is the emote
    assert isinstance(msgs[0], EmoteMessage)

    # next should be the SoundMessage from SoundEffectObserver
    assert any(isinstance(m, SoundMessage) for m in msgs[1:])

    # then the DialogueMessage with our expected text
    dialogues = [m for m in msgs if isinstance(m, DialogueMessage)]
    assert dialogues, "Expected at least one DialogueMessage"
    texts = [m._get_data().get('dialogue_text', '') for m in dialogues]
    assert label in texts

    # balance should have been reduced
    assert pytest.approx(bm.get_balance(player=p), rel=1e-6) == 1000.0 - price

