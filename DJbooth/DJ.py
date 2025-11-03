
from ..imports import *


from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from coord import Coord
    from maps.base import Map
    from tiles.base import MapObject
    from tiles.map_objects import *
    from resources import get_resource_path
    from message import *

import random 
import os
from pathlib import Path
from typing import List


class DJ:
    """
    Singleton DJ class for managing music system in the DJ booth.

    This class uses the Singleton design pattern to ensure that only one instance exists.
    It also provides methods to play, go to the next song, return to the previous song, and shuffle the playlist.

    @Attributes:
        songs (List[str]): A list of song names
        current_index (int): The index of the currently playing song
    """
    __instance = None

    def __new__(cls) -> "DJ":
        if cls.__instance is None:
            cls.__instance = super(DJ, cls).__new__(cls)
        return cls.__instance

    def __init__(self) -> None:
        """
        Initializes the DJ instance. This initialization is run only once.

        @Postconditions:
            - The instance is initialized with a pre-defined list of songs and the current index is set to 0
        """
        if not hasattr(self, 'initialized'):
            self.songs: List[str] = ['baby', '365', 'party4u', 'limitless', 'audacity']
            self.current_index: int = 0
            self.initialized = True

    def play(self, player: "HumanPlayer") -> List["Message"]:
        """
        Plays the current song and returns a list of messages representing the DJ booth effects.

        @Parameters:
            player (HumanPlayer): The player who triggered the command

        @Returns:
            List[Message]: A list of messages including sound and emote messages to display effects

        @Preconditions:
            - There must be at least one song in the playlist
        @Postconditions:
            - Returns a list of messages; if no songs exist, an empty list is returned
        """
        assert self.songs, "No songs in the playlist"
        if self.songs:
            current_song = self.songs[self.current_index]
            print("song playing")
            # Create a sound message for the current song.
            sound_msg: "SoundMessage" = SoundMessage(player, f'{current_song}')
            # Create several emote messages to simulate light effects.
            emote_msg1: "EmoteMessage" = EmoteMessage(player, player, "disco", Coord(1, 4))
            emote_msg2: "EmoteMessage" = EmoteMessage(player, player, "small_light", Coord(5, 1))
            emote_msg3: "EmoteMessage" = EmoteMessage(player, player, "light_blue", Coord(0, 0))
            emote_msg4: "EmoteMessage" = EmoteMessage(player, player, "light_red", Coord(5, 0))
            server_msg: "ServerMessage" = ServerMessage(player, "Playing Music in DJ Booth")
            msg2: "EmoteMessage" = EmoteMessage(player, player, "light_red", Coord(5, 1))
            msg3: "EmoteMessage" = EmoteMessage(player, player, "small_light", Coord(0, 0))
            msg4: "EmoteMessage" = EmoteMessage(player, player, "light_blue", Coord(7, 0))
            # Return all messages.
            return [sound_msg, emote_msg1, emote_msg2, emote_msg3, emote_msg4, server_msg, msg2, msg3, msg4]
        else:
            return []

    def next_song(self, player: "HumanPlayer") -> List["Message"]:
        """
        Goes to the next song in the playlist and plays it.

        @Parameters:
            player (HumanPlayer): The player who triggered the command

        @Returns:
            List[Message]: A list of messages from playing the next song
        """
        if self.songs:
            self.current_index = (self.current_index + 1) % len(self.songs)
            return self.play(player)
        else:
            return []

    def previous_song(self, player: "HumanPlayer") -> List["Message"]:
        """
        Goes back to the previous song in the playlist and plays it

        @Parameters:
            player (HumanPlayer): The player who triggered the command

        @Returns:
            List[Message]: A list of messages from playing the previous song
        """
        if self.songs:
            self.current_index = (self.current_index - 1) % len(self.songs)
            return self.play(player)
        else:
            return []

    def shuffle(self, player: "HumanPlayer") -> List["Message"]:
        """
        Shuffles the playlist and resets the current song to the first song, then plays it

        @Parameters:
            player (HumanPlayer): The player who triggered the command

        @Returns:
            List[Message]: A list of messages from playing the first song after shuffling
        """
        if self.songs:
            random.shuffle(self.songs)
            self.current_index = 0
            return self.play(player)
        else:
            return []