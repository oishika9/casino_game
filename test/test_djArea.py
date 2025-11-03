# tests/test_plate_and_dj.py
import pytest
import random


from ..BarRoom import LightPressurePlate, DJBoothComputer
from ..DJbooth.DJ import DJ
from ..COMMANDS.DJ_commands import (
    DJPlayCommand,
    DJNextCommand,
    DJPreviousCommand,
    DJShuffleCommand,
)
from ..imports import *
from ..example_map import ExampleHouse

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from coord import Coord
    from Player import HumanPlayer


class DummyPlayer:
    """ HumanPlayer (needs get_name and get_image_name)."""
    def __init__(self, name: str):
        self._name = name

    def get_name(self) -> str:
        return self._name

    def get_image_name(self) -> str:
        return "dummy_image"


@pytest.fixture(autouse=True)
def reset_dj_singleton():
    # Clear DJ singleton between tests
    DJ._DJ__instance = None
    yield
    DJ._DJ__instance = None


def test_light_pressure_plate_behavior():
    p = DummyPlayer("Alice")
    plate = LightPressurePlate(emote_path="sparkle", emote_pos=Coord(2, 3))

    # Stepping on it returns exactly one EmoteMessage
    msgs = plate.player_entered(p)
    assert len(msgs) == 1
    em = msgs[0]
    #check that it is an EmoteMessage 
    assert isinstance(em, EmoteMessage)
    data = em._get_data()
    assert data["emote"] == "sparkle"
    # emote_pos is positioned to (x, y)
    assert data["emote_pos"] == (2, 3)

    # Setting an empty path should assert
    with pytest.raises(AssertionError):
        plate.set_emote_path("")

    # Valid change of path and position
    plate.set_emote_path("boom")
    plate.set_emote_position(Coord(5, 6))
    msgs2 = plate.player_entered(p)
    em2 = msgs2[0]
    d2 = em2._get_data()
    assert d2["emote"] == "boom"
    assert d2["emote_pos"] == (5, 6)

    # Invalid position type should assert
    with pytest.raises(AssertionError):
        plate.set_emote_position("not a coord")


