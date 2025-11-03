import pytest
import random


from ..imports import *
from ..DJbooth.DJ import DJ
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from coord import Coord
    from maps.base import Map
    from tiles.base import MapObject
    from tiles.map_objects import *
    from coord import Coord
    from Player import HumanPlayer
    from message import SoundMessage, DialogueMessage, ServerMessage

from ..BALANCE.PlayerBalance import *  

# Dummy HumanPlayer class for testing.
class DummyPlayer:
    def __init__(self, name: str = "TestPlayer"):
        self._name = name

    def get_image_name(self) -> str:
        return "dummy_image"

    def get_name(self) -> str:
        return self._name

@pytest.fixture(autouse=True)
def reset_dj_singleton():
    """
    Fixture to reset the DJ singleton instance between tests.
    """
    DJ._DJ__instance = None
    yield
    DJ._DJ__instance = None

def test_singleton_property():
    """Test that multiple instantiations of DJ return the same instance."""
    dj1 = DJ()
    dj2 = DJ()
    assert dj1 is dj2, "DJ should be a singleton, both instances must be identical."

def test_play_returns_messages():
    """Test that the play method returns a list of messages and that the list is non-empty."""
    dj = DJ()
    player = DummyPlayer()
    messages = dj.play(player)
    assert isinstance(messages, list), "The result of play() should be a list."
    # We expect at least one message
    assert len(messages) >= 1, "Expected non-empty list of messages when play() is called."

def test_next_song_updates_index():
    """Test that next_song advances the current index correctly."""
    dj = DJ()
    player = DummyPlayer()
    original_index = dj.current_index
    dj.next_song(player)
    expected_index = (original_index + 1) % len(dj.songs)
    assert dj.current_index == expected_index, "next_song() should increment the current_index properly."

def test_previous_song_updates_index():
    """Test that previous_song updates the current index correctly."""
    dj = DJ()
    player = DummyPlayer()
    original_index = dj.current_index
    dj.previous_song(player)
    expected_index = (original_index - 1) % len(dj.songs)
    assert dj.current_index == expected_index, "previous_song() should decrement the current_index properly."

def test_shuffle_resets_index_and_changes_order():
    """
    Test that shuffle resets the current index to 0 and changes the order of songs.
    Note: Since shuffling is random, this test checks that the index resets.
    """
    dj = DJ()
    player = DummyPlayer()
    original_order = dj.songs.copy()
    dj.shuffle(player)
    assert dj.current_index == 0, "After shuffling, the current_index should be reset to 0."
    