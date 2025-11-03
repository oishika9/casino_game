#from tkinter import image_names

from .COMMANDS.BalanceCommand import BalanceCommand
from .NPCs.NPC_Bartender import WalkingBartender
from .DJbooth.DJ import DJ 
from .COMMANDS.DJ_commands import *
from .imports import *
from .COMMANDS.BarCommand import BarCommand

from typing import List
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from coord import Coord
    from maps.base import Map
    from tiles.base import MapObject
    from tiles.map_objects import *
    from resources import get_resource_path

from typing import List


# Walkable Tile-----------------------------------------------------------------------------------
class Walkable(MapObject):
    """Tiles om which the player cannot walk on"""
    def __init__(self, image_name: str, passable: bool = True) -> None:
        super().__init__(f'tile/{image_name}', passable=True, z_index=-1.5)


# Creating Bar Room -------------------------------------------------------------------------------
class BarRoom(Map):
    """
    Represents the Bar Room map.
    """
    def __init__(self) -> None:
        super().__init__(
            name="Bar Room",
            description="Its time to party yeppieee!! Order drinks at the bar, play music at the DJ booth and dance on the dance floor!",
            size=(20, 18),
            entry_point=Coord(24, 3),
            background_tile_image='wood_diagonal',
            chat_commands = [BalanceCommand],
            background_music='bar_bg',
        )
    
    def get_objects(self) -> list[tuple[MapObject, Coord]]:
        """
        @Returns a list of map objects along with their coordinates.
        @Preconditions: All objects created here must be valid MapObjects.
        """
        objects: list[tuple[MapObject, Coord]] = []

        # Add a door to the Casino Royale House.
        door = Door('int_entrance', linked_room="Casino Royale House")
        #door = Door('int_entrance', linked_room="Casino Royale House", is_main_entrance=False)
        objects.append((door, Coord(19, 5)))

        #create bar tables 
        table1 = IntDecor('bar_table')
        objects.append((table1, Coord(15,8)))
        table2 = IntDecor('bar_table')
        objects.append((table2, Coord(12,12)))
        table3 = IntDecor('bar_table')
        objects.append((table3, Coord(15,13)))
        table4 = IntDecor('bar_table')
        objects.append((table4, Coord(8,10)))
        

        #Bar Area
        chair = IntDecor('stool2')
        objects.append((chair, Coord(8,3)))
        chair = IntDecor('stool2')
        objects.append((chair, Coord(8,3)))
        chair1 = IntDecor('stool2')
        objects.append((chair1, Coord(8,1)))
        chair3 = IntDecor('stool2')
        objects.append((chair3, Coord(14,3)))
        chair3 = IntDecor('stool2')
        objects.append((chair3, Coord(14,1)))
        chair2 = IntDecor('chair2')
        objects.append((chair2, Coord(11,6)))

        #Dance floor 
        walkable = Walkable('background/red_tile')
        for x in range(0, 9):
            for y in range(0, 18):
                coord = Coord(x, y)
                objects.append((walkable, coord))

        
        # add door to Casino Room
        casinodoor = Door('side1_entrance',  linked_room="Casino Room")
        casinodoor.connect_to("Casino Room" , Coord(6, 0))  
        objects.append((casinodoor, Coord(6, 0)))


        # add an NPC - bartender
        bartender = WalkingBartender(
            encounter_text = "Welcome to the bar! What can I get you?",
            # this has to be checked because the NPC is not interacting with me; object potentially colliding with me
            staring_distance = 5,
        )
        objects.append((bartender, Coord(13, 4)))


        #create DJ booth -------------------------------
        dj_instance = DJ()
        dj_set = DJBoothComputer(dj_instance)
        objects.append((dj_set, Coord(4,6)))

        
        #create dance floor - flashing lights 
        pp_bluelight = LightPressurePlate('light_blue', Coord(2,0))
        objects.append((pp_bluelight, Coord(6,3)))
        pp_redlight1 = LightPressurePlate('light_red', Coord(3,1))
        objects.append((pp_redlight1, Coord(7,3)))
        pp_bluelight2 = LightPressurePlate('light_blue', Coord(2,3))
        objects.append((pp_bluelight2, Coord(6,1)))
        pp_bluelight3 = LightPressurePlate('light_blue', Coord(3,1))
        objects.append((pp_bluelight3, Coord(5,3)))
        pp_redlight =  LightPressurePlate('light_red', Coord(5,0))
        objects.append((pp_redlight, Coord(7,4)))
        pp_bluelight4 = LightPressurePlate('light_blue', Coord(3,1))
        objects.append((pp_bluelight4, Coord(7,5)))
        pp_redlight2 = LightPressurePlate('light_red', Coord(3,1))
        objects.append((pp_redlight2, Coord(7,6)))
        pp_light = LightPressurePlate('small_light', Coord(6,1))
        objects.append((pp_light, Coord(8,3)))
        pp_light1 = LightPressurePlate('small_light', Coord(6,1))
        objects.append((pp_light1, Coord(8,7)))
        pp_light2 = LightPressurePlate('small_light', Coord(6,2))
        objects.append((pp_light2, Coord(7,7)))
        pp_bluelight5 = LightPressurePlate('light_blue', Coord(5,6))
        objects.append((pp_bluelight5, Coord(7,8)))
        pp_light2 = LightPressurePlate('small_light', Coord(4,2))
        objects.append((pp_light2, Coord(7,9)))
        pp_redlight3 = LightPressurePlate('light_red', Coord(4,2))
        objects.append((pp_redlight3, Coord(8,6)))
        pp_bluelight6 = LightPressurePlate('light_blue', Coord(4,4))
        objects.append((pp_bluelight6, Coord(8,8)))
        pp_light3 = LightPressurePlate('small_light', Coord(4,1))
        objects.append((pp_light3, Coord(6,8)))
        pp_redlight4 = LightPressurePlate('light_red', Coord(4,2))
        objects.append((pp_redlight4, Coord(6,6)))
        pp_light4 = LightPressurePlate('small_light', Coord(4,1))
        objects.append((pp_light4, Coord(6,7)))
        pp_bluelight7 = LightPressurePlate('light_blue', Coord(4,4))
        objects.append((pp_bluelight7, Coord(6,4)))

        #Bar object -> order drinks
        bar_menu = BarMenuComputer()
        objects.append((bar_menu, Coord(10,2)))
    
        return objects


#PRESSURE PLATE THE SENDS AN EMOTE MESSAGE WHEN YOU STEP ON IT 
class LightPressurePlate(PressurePlate):
    """
    A pressure plate that sends an emote message when a player steps on it.
    
    @Precondition: emote_path must be a non-empty string.
    @Postcondition: Returns a list containing one EmoteMessage.
    """
    def __init__(self, emote_path: str = '', emote_pos: "Coord" = None) -> None:
        super().__init__(image_name="empty")
        self.__emote_path = emote_path
        self.__emote_pos = emote_pos if emote_pos is not None else Coord(0, 0)
    
    def set_emote_path(self, emote_path: str) -> None:
        assert isinstance(emote_path, str) and emote_path != "", "emote_path must be a non-empty string"
        self.__emote_path = emote_path
    
    def set_emote_position(self, emote_pos: "Coord") -> None:
        assert hasattr(emote_pos, 'to_tuple'), "emote_pos must be a Coord object"
        self.__emote_pos = emote_pos
    
    def player_entered(self, player) -> List[Message]:
        """
        Called when a player steps on the pressure plate.
        
        @Returns:
            A list containing an EmoteMessage.
        """
        return [EmoteMessage(player, player, self.__emote_path, self.__emote_pos)]



# DJ BOOTH MENU OPTIONS
class DJBoothComputer(Computer):
    """
    A computer object representing a DJ booth with DJ controls.
    
    Provides menu options for playing, advancing, reversing, and shuffling the music.
    """
    def __init__(self, dj_instance: DJ) -> None:
        assert dj_instance is not None, "dj_instance cannot be None"
        menu_options = {
            # LEADS YOU TO THE CONCRETE COMMAND CLASSES IN DJ_Commands
            'play': DJPlayCommand(dj_instance),
            'next': DJNextCommand(dj_instance),
            'previous': DJPreviousCommand(dj_instance),
            'shuffle': DJShuffleCommand(dj_instance)
        }
        super().__init__(image_name="casino_table6", menu_name="DJ Booth Controls", menu_options=menu_options)


# BARMAN MENU
class BarMenuComputer(Computer):
    """
    A computer object that presents a bar menu for ordering drinks.
    """
    def __init__(self) -> None:

        menu_options = {
            'coke - $5.00': BarCommand(5.00),
            'vodka coke - $17.00': BarCommand(17.00),
            'vodka - $12.00': BarCommand(12.00),
        }
        super().__init__(image_name = 'counter3',menu_name = "Bar Menu", menu_options = menu_options)


