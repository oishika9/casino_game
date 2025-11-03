import pytest
from HorseBettingManager import HorseBettingManager

class DummyObserver:
    def __init__(self):
        self.called = False
    def update_scoreboard(self, winning_horse):
        self.called = True
        return ["ok"]

class DummyPlayer:
    def __init__(self, name):
        self._name = name
    def get_name(self):
        return self._name

def test_scoreboard_observers():
    mgr = HorseBettingManager()
    mgr.scoreboard_observers.clear()
    obs = DummyObserver()
    mgr.register_scoreboard_observer(obs)
    msgs = mgr.notify_scoreboard_observers(2)
    assert obs.called
    assert msgs == ["ok"]

def test_player_choice_and_bet_defaults():
    mgr = HorseBettingManager()
    player = DummyPlayer("A")
    assert mgr.get_player_choice(player) == -1

    mgr.set_player_choice(player, 5)
    assert mgr.get_player_choice(player) == 5

    # test bet setter/getter
    assert mgr.get_bet() == 50
    ret = mgr.set_bet(player, 99)
    assert mgr.get_bet() == 99
    assert ret == []
