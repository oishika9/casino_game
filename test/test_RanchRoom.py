import pytest
from RanchRoom import RanchRoom, ScoreboardSign
from imports import Coord
from ..RanchRoom import RanchRoom, ScoreboardSign
from ..

def test_scoreboard_sign_displays_default():
    sign = ScoreboardSign(text="No races yet")
    msgs = sign.player_interacted(DummyPlayer())
    from message import DialogueMessage
    assert isinstance(msgs[0], DialogueMessage)
    assert msgs[0].text == "No races yet"