import pytest
from HorseManagerCommands import (
    HorseManagerYesCommand,
    HorseManagerNoCommand,
    HorseChoiceCommand,
)
from HorseBettingManager import HorseBettingManager

class DummyPlayer:
    def __init__(self):
        self._img = "hero"
    def get_image_name(self):
        return self._img
    def get_current_room(self):
        class R: bookmaker1 = None
        return R()

def test_yes_command_prompts_for_bet():
    mgr = HorseBettingManager()
    cmd = HorseManagerYesCommand(mgr)
    res = cmd.execute(None, DummyPlayer())
    texts = [m.text for m in res]
    assert any("place your bet" in t for t in texts)

def test_no_command_exits():
    mgr = HorseBettingManager()
    cmd = HorseManagerNoCommand(mgr)
    res = cmd.execute(None, DummyPlayer())
    assert len(res) == 1

def test_choice_command_invalid_selection():
    mgr = HorseBettingManager()
    cmd = HorseChoiceCommand(mgr, "not_a_number")
    res = cmd.execute(None, DummyPlayer())
    from message import DialogueMessage
    assert isinstance(res[0], DialogueMessage)
    assert "Invalid selection" in res[0].text
