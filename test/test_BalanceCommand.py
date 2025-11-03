import pytest
from BalanceCommand import BalanceCommand
from PlayerBalance import BalanceManager

class DummyPlayer:
    def __init__(self, name):
        self._name = name
    def get_name(self):
        return self._name

class FakeServerMessage:
    def __init__(self, recipient, text):
        self.recipient = recipient
        self.text = text

@pytest.fixture(autouse=True)
def patch_server_message(monkeypatch):
    from BalanceCommand import ServerMessage
    monkeypatch.setattr("BalanceCommand.ServerMessage", FakeServerMessage)

def test_matches():
    assert BalanceCommand.matches("balance")
    assert BalanceCommand.matches("  BALANCE ")
    assert not BalanceCommand.matches("bal")

def test_execute_shows_correct_balance(monkeypatch):
    player = DummyPlayer("Bob")
    # stub get_balance
    monkeypatch.setattr(BalanceManager, "get_balance", lambda self, player=None: 1234.56)
    cmd = BalanceCommand()
    msgs = cmd.execute("balance", None, player)
    assert len(msgs) == 1
    msg = msgs[0]
    assert isinstance(msg, FakeServerMessage)
    assert "1234.56" in msg.text
