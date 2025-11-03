from ..imports import *

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from coord import Coord
    from maps.base import Map
    from tiles.base import MapObject
    from tiles.map_objects import *
    from NPC import NPC

import copy 

from typing import List

class NPCClone(NPC):
    """
    A prototype‐based NPC that can be cloned

    Implements the Prototype design pattern: call clone() to produce
    an independent deep copy of this instance with the same attributes without having to create 
    a new NPC from scratch. 
    """
    def __init__(self, encounter_text: str, staring_distance: int = 0) -> None:
        super().__init__(
            name = "NPC Clone",
            image="player2",
            encounter_text=encounter_text,
            staring_distance=staring_distance,
        )

    def clone(self) -> 'NPCClone':
        """
        Produce a deep copy of this NPCClone.

        @return: A new NPCClone instance with identical state.
        """
        return copy.deepcopy(self)

    def set_encounter_text(self, new_text: str) -> None:
        """
        Update the encounter text of this NPC.

        @param new_text: The new text to display on interaction.
        
        @Postconditions:
            - Future calls to player_interacted will use new_text.
        """
        setattr(self, "_NPC__encounter_text", new_text)

