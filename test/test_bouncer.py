import pytest

from ..COMMANDS.AgeChatCommand import AgeChatCommand
from ..NPCs.NPCBouncer1 import NPCBouncer1

from typing import List

from ..imports import *
from ..example_map import ExampleHouse

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from coord import Coord
    from Player import HumanPlayer

# Dummy implementations to support the tests:
class DummyRoom:
    """A minimal dummy room with a bouncer and a teleport object."""
    def __init__(self, bouncer: object = None, teleport: object = None):
        self.bouncer = bouncer
        self.teleport = teleport

class DummyTeleport:
    """A dummy teleport object with a player_entered method that returns a ServerMessage."""
    def player_entered(self, player: "DummyPlayer") -> List:
        return [ServerMessage(player, "Teleported to Trottier Town!")]

class DummyPlayer:
    """
     dummy for HumanPlayer.
    It needs to provide:
        - get_name()
        - get_image_name()
        - get_state()/set_state() for waiting_for_age_npc, etc.
        - get_current_room() to return a dummy room.
    """
    def __init__(self, name: str):
        self._name = name
        self._state = {}
        # Initially set current_room to a dummy room.
        self._room = DummyRoom()

    def get_name(self) -> str:
        return self._name

    def get_image_name(self) -> str:
        return "dummy_player_img"

    def get_state(self, key: str):
        return self._state.get(key)

    def set_state(self, key: str, value):
        self._state[key] = value

    def get_current_room(self):
        return self._room

    def set_current_room(self, room: object):
        self._room = room


# AgeChatCommand Tests
def test_agechat_matches():
    # Should match if the text is "age/" followed by digits.
    assert AgeChatCommand.matches("age/21")
    # Should not match if non-digits follow.
    assert not AgeChatCommand.matches("age/twenty")
    # Should not match if the prefix is wrong.
    assert not AgeChatCommand.matches("foo/21")
    # Should not match if nothing follows.
    assert not AgeChatCommand.matches("age/")


def test_agechat_execute_no_npc():
    """
    If the player's state does not include 'waiting_for_age_npc',
    then AgeChatCommand.execute should return a ServerMessage indicating no one is asking.
    """
    cmd = AgeChatCommand()
    player = DummyPlayer("TestPlayer")
    # Ensure state is not set.
    player.set_state("waiting_for_age_npc", None)
    msgs = cmd.execute("age/30", context=None, player=player)
    # Expect a single ServerMessage.
    assert len(msgs) == 1
    assert isinstance(msgs[0], ServerMessage)
    assert "No one is asking" in msgs[0]._get_data().get("text", "")


def test_agechat_execute_with_bouncer(monkeypatch):
    """
    When the player's state has a waiting_for_age_npc value and the room has a bouncer,
    AgeChatCommand.execute should delegate processing to the bouncer.
    """
    cmd = AgeChatCommand()
    player = DummyPlayer("TestPlayer")
    # Set the waiting_for_age_npc flag.
    player.set_state("waiting_for_age_npc", "bouncer_id")

    # Create a dummy bouncer with a process_player_input method.
    class DummyBouncer:
        def __init__(self):
            self.called_with = None

        def process_player_input(self, player, age_str: str) -> List:
            self.called_with = age_str
            return [DialogueMessage(self, player, f"Processed age: {age_str}", "bouncer_img")]

        def get_image_name(self) -> str:
            return "bouncer_img"

    dummy_bouncer = DummyBouncer()
    # Create a dummy teleport so that room.teleport exists 
    dummy_teleport = DummyTeleport()
    room = DummyRoom(bouncer=dummy_bouncer, teleport=dummy_teleport)
    player.set_current_room(room)

    msgs = cmd.execute("age/17", context=None, player=player)
    # The dummy bouncer should have been called with "17"
    assert dummy_bouncer.called_with == "17"
    # And the returned message should be a DialogueMessage reflecting that.
    assert any(isinstance(m, DialogueMessage) and "Processed age: 17" in m._get_data().get("dialogue_text", "")
               for m in msgs)


# --------------------- NPCBouncer1 Tests --------------------- #


def test_npcbouncer1_process_player_input_underage(monkeypatch):
    """
    When the player enters an age under 18, NPCBouncer1 should return messages
    that include teleportation.
    """
    dialogues = ["Welcome!", "Please tell me your age:"]
    bouncer = NPCBouncer1(dialogues, staring_distance=1)
    player = DummyPlayer("Underage")
    # Set the bouncer in the player's current room.
    dummy_teleport = DummyTeleport()
    room = DummyRoom(bouncer=bouncer, teleport=dummy_teleport)
    player.set_current_room(room)
    # Simulate that bouncer is waiting for input.
    bouncer.waiting_for_input = True

    msgs = bouncer.process_player_input(player, "16")
    # Expect a ServerMessage about teleportation and a DialogueMessage indicating "too young".
    server_msgs = [m for m in msgs if isinstance(m, ServerMessage)]
    assert any("Teleporting" in m._get_data().get("text", "") for m in server_msgs)
    # After processing, waiting_for_input should be False and conversation finished.
    assert bouncer.waiting_for_input is False
    assert bouncer.conversation_finished is True


def test_npcbouncer1_process_player_input_valid_age(monkeypatch):
    """
    When the player enters an age of 18 or above, NPCBouncer1 should welcome the player.
    """
    dialogues = ["Welcome!", "Please tell me your age:"]
    bouncer = NPCBouncer1(dialogues, staring_distance=1)
    player = DummyPlayer("Adult")
    dummy_teleport = DummyTeleport()
    room = DummyRoom(bouncer=bouncer, teleport=dummy_teleport)
    player.set_current_room(room)
    bouncer.waiting_for_input = True

    msgs = bouncer.process_player_input(player, "25")
    dialogue_msgs = [m for m in msgs if isinstance(m, DialogueMessage)]
    assert any("Welcome! You may continue" in m._get_data().get("dialogue_text", "")
               for m in dialogue_msgs)
    # After processing, conversation should be marked finished.
    assert bouncer.conversation_finished is True
