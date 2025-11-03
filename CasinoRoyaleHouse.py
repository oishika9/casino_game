from .NPCs.NPCBouncer1 import NPCBouncer1
from .COMMANDS.AgeChatCommand import AgeChatCommand
from .COMMANDS.BalanceCommand import BalanceCommand

from .imports import *

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from coord import Coord
    from maps.base import Map
    from tiles.base import MapObject
    from tiles.map_objects import *
from typing import List, Tuple

class Unwalkable(MapObject):
    """
    Represents an object that cannot be walked on
    
    @Precondition:
        - image_name: The image file name (without path prefix) must be a non-empty string.
        - passable is always False.
    """
    def __init__(self, image_name: str, passable: bool = False) -> None:
        assert image_name, "image_name must not be empty."
        super().__init__(f'tile/{image_name}', passable=False, z_index=-1)


class CasinoRoyaleHouse(Map):
    """
    Represents the Casino Royale House - a main entrance map
    """
    MAIN_ENTRANCE = True

    def __init__(self) -> None:
        """
        Initialize the CasinoRoyaleHouse with a name, description, size, entry point,
        background image, chat commands, and background music.
        """
        super().__init__(
            name="Casino Royale House",
            description="Welcome to the BEST casino in town!! Interact with the NPC to show your ID and get in ;)",
            size=(15, 15),
            entry_point=Coord(14, 7),
            background_tile_image='cobblestone',
            chat_commands=[AgeChatCommand, BalanceCommand],
            background_music='blue_val',
        )

    def get_objects(self) -> List[Tuple['MapObject', 'Coord']]:
        """
        Constructs and returns a list of tuples (object, coordinate) that belong to this map.
        
        @Preconditions:
            - The NPC bouncer and teleport door are only created if they do not exist yet.
        
        @Returns:
            A list of map objects paired with their coordinates.
        """
        objects: List[Tuple['MapObject', 'Coord']] = []

        # Create and add the main door to Trottier Town.
        door = Door('int_entrance', linked_room="Trottier Town", is_main_entrance=True)
        # Assert that door's position is valid (here we assume Coord(14, 7) is correct).
        assert isinstance(Coord(14, 7), Coord), "Entry point must be a Coord instance."
        objects.append((door, Coord(14, 7)))

        # Instantiate the bouncer if not already present.
        if not hasattr(self, 'bouncer'):
            self.bouncer = NPCBouncer1(
                dialogues=[
                    "HEY YOU RIGHT THERE", "YOU LOOK SUS", "I NEED TO SEE YOUR ID"
                ],
                staring_distance=1,
            )
        objects.append((self.bouncer, Coord(8, 8)))

        # Create and add a door to the Bar Room.
        bardoor = Door('back_entrance', linked_room="Bar Room")
        # Connect the door with the corresponding room entry point.
        bardoor.connect_to("Bar Room", Coord(0, 7))
        objects.append((bardoor, Coord(0, 7)))
        
        # Add unwalkable areas to shrink the room.
        unwalkable = Unwalkable('background/water')
        for x in range(1, 14):
            for y in range(1, 5):
                coord = Coord(x, y)
                objects.append((unwalkable, coord))
        for x in range(1, 14):
            for y in range(10, 14):
                coord = Coord(x, y)
                objects.append((unwalkable, coord))

        # Add decorative plants along the borders.
        plant = IntDecor('plant')
        for y in range(0, 13):
            coord1 = Coord(y, 0)
            coord2 = Coord(y, 14)
            objects.append((plant, coord1))
            objects.append((plant, coord2))
      
        # Create an invisible door for a teleportation trick if not already created.
        if not hasattr(self, 'teleport'):
            self.teleport = Door('empty', linked_room="Teleport Room")
            self.teleport.connect_to("Teleport room", Coord(0, 0))
        objects.append((self.teleport, Coord(0, 0)))

        return objects

