from ..imports import *

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from coord import Coord
    from maps.base import Map
    from tiles.base import MapObject
    from tiles.map_objects import *
    from NPC import NPC



class WalkingBartender(NPC):
    """
    A subclass of NPC that represents a  bartender.
    """
    
    def __init__(self, encounter_text: str, staring_distance: int = 0) -> None:
        """
        Initialize a WalkingBartender NPC.

        Parameters:
            encounter_text (str): The text to display when the bartender is encountered.
            staring_distance (int, optional): The distance at which the NPC starts interacting with the player.
                                              Must be >= 0. Defaults to 0.

        Preconditions:
        - encounter_text: must be a non-empty string describing the text displayed when a player interacts
        - staring_distance: should be a non-negative integer
        """
        assert encounter_text, "Encounter text must not be empty."
        assert staring_distance >= 0, "Staring distance must be non-negative."
        
        super().__init__(
            name="Bartender",          
            image='prof',              
            facing_direction='right',  
            encounter_text=encounter_text,
            staring_distance=staring_distance,
        )