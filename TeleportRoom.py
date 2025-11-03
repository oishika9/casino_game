
from .imports import *

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from coord import Coord
    from maps.base import Map
    from tiles.base import MapObject
    from tiles.map_objects import *


class TeleportRoom(Map):
    """
    The map where the player gets teleported to...
    Inherits from Map.
    """
    def __init__(self) -> None:
        super().__init__(
            name="Teleport Room",
            description="teleported - but look carefully there might be a secret entrance to the casino...",
            size=(15, 15),
            entry_point=Coord(14, 7),
            background_tile_image='grass',
            background_music='park_bg',
            
        )
    
    def get_objects(self) -> list[tuple[MapObject, Coord]]:
        """
        Build and return all MapObjects in this room, with their positions.

        @Returns:
            List of (MapObject, Coord) tuples.
        """
        objects: list[tuple[MapObject, Coord]] = []

        # add a door
        door = Door('empty', linked_room="Casino Royale House")
        objects.append((door, Coord(7, 7)))


        door1 = Door('tube', linked_room="Casino Room")
        door1.connect_to("Casino Room", Coord(14,14))
        objects.append((door1, Coord(14,14)))

        
        #DECOR
        tree1 = ExtDecor('tree_large_1')
        tree2 = ExtDecor('tree_large_1')
        tree3 = ExtDecor('mapletree_small_1')
        tree4 = ExtDecor('tree_large_1')


        tree5 = ExtDecor('mapletree_large_2')
        tree6 = ExtDecor('tree_large_2')
        tree7 = ExtDecor('tree_large_2')
        tree8 = ExtDecor('mapletree_large_2')

        bush1 = ExtDecor('blue_bush')
        bush2 = ExtDecor('blue_bush')
        bush3 = ExtDecor('blue_bush')

        objects.append((tree1, Coord(12, 2)))
        objects.append((tree2, Coord(5, 2)))
        objects.append((tree3, Coord(9, 2)))
        objects.append((tree4, Coord(7, 1)))
        objects.append((tree5, Coord(6, 4)))
        objects.append((tree6, Coord(3, 5)))
        objects.append((tree7, Coord(3, 3)))

        objects.append((tree8, Coord(3, 11)))
        objects.append((bush1, Coord(9, 11)))
        objects.append((bush2, Coord(13, 9)))
        objects.append((bush3, Coord(11, 13)))
        return objects
