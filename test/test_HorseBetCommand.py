import pytest
from HorseBetCommand import HorseBetCommand

class DummyPlayer:
    def __init__(self):
        self._state = {}
    def get_state(self, key):
        return self._state.get(key)
    def get_current_room(self):
        return self
    bookmaker1 = None

def test_matches():
    assert HorseBetCommand.matches("bet_horse/100")
    assert not HorseBetCommand.matches("bet_hors/10")

def test_execute_without_bet_context():
    cmd = HorseBetCommand()
    player = DummyPlayer()
    res = cmd.execute("bet_horse/50", None, player)
    # should get a ServerMessage telling there's no NPC
    from command import ServerMessage
    assert isinstance(res[0], ServerMessage)
    assert "No one is for you to bet" in res[0].text
