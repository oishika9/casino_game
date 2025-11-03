import pytest
from BarCommand import BarCommand
from PlayerBalance import BalanceManager, BalanceChangeReason
from PlayerBalance import SoundEffectObserver, BalanceEffectObserver

class DummyPlayer:
    def __init__(self,name):
        self._name = name
    def get_name(self):
        return self._name

def test_execute_emote_and_balance(monkeypatch):
    player = DummyPlayer("X")
    bar = BarCommand(10.0)
    bm = BalanceManager()
    bm.balances.clear()
    bm.observers.clear()

    msgs = bar.execute(None, player)
    # first message should be the emote
    from message import EmoteMessage
    assert isinstance(msgs[0], EmoteMessage)
    # should also have at least one DialogueMessage from BalanceEffectObserver
    from message import DialogueMessage
    assert any(isinstance(m, DialogueMessage) for m in msgs)