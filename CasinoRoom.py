from .imports import *
from .NPCs.NPCClone import *
#from CasinoRoyale.BALANCE.PlayerBalance import *
from .GAME.SlotMachine import *
from .Cards.BlackjackComputer import BlackjackComputer
from .Cards.OneCardPokerComputer import OneCardPokerComputer
from .Cards.OneCardPokerStrategy import EasyPokerStrategy, MediumPokerStrategy, HardPokerStrategy


from typing import TYPE_CHECKING

from .COMMANDS.BalanceCommand import BalanceCommand

if TYPE_CHECKING:
    from coord import Coord
    from maps.base import Map
    from tiles.base import MapObject
    from tiles.map_objects import *
    from command import ChatCommand

import copy


class CasinoRoom(Map):
    '''The room where casino activities takes place '''
    def __init__(self) -> None:
        super().__init__(
            name="Casino Room",
            description="Lets get betting - go up to the casino tables to play games",
            size=(15, 15),
            entry_point=Coord(14, 7),
            background_tile_image='blue_tile',
            background_music='casino_bg',
            chat_commands = [BalanceCommand],
        )


    def get_objects(self) -> list[tuple[MapObject, Coord]]:
        '''Return a tuples of all the Map0bjects and their Coord on the Map '''
        objects: list[tuple[MapObject, Coord]] = []

        # add a door left of from bar to casino
        door_casino_bar = Door('side2_entrance', linked_room="Bar Room")
        objects.append((door_casino_bar, Coord(5, 14)))

        # add a door from back of casino to ranch
        door_casino_ranch = Door('back_entrance', linked_room="Ranch Room")
        door_casino_ranch.connect_to("Ranch Room" , Coord(0, 10))
        objects.append((door_casino_ranch, Coord(0, 10)))

        door1 = Door('tube', linked_room="Teleport Room")
        objects.append((door1, Coord(14,14)))

        npc1 = NPCClone('I LOST ALL MY MONEY NOOO', 2)
        #npc2 = npc1.clone()
        #npc2.set_encounter_text("It's my lucky day today")
        #objects.append((npc1, Coord(12,7)))
        objects.append((npc1, Coord(5,7)))

        # creating dealer guys

        dealer = NPCClone('To start Betting interact with the table',2)
        objects.append((dealer, Coord(11,0)))

        dealer2 = dealer.clone()
        objects.append((dealer2, Coord(11,8)))



        #create slot machine object TO INTERACT WITH
        slotmachine = SlotMachineUtility()
        objects.append((slotmachine, Coord(6,6)))

        # blackjack
        blackjack_table = BlackjackComputer()
        objects.append((blackjack_table, Coord(9, 2)))


        ########BlackjackComputer().copy()
        blackjack_table2 = BlackjackComputer().clone()
        objects.append((blackjack_table, Coord(9, 10)))


        # easy poker
        e_poker_table = OneCardPokerComputer(strategy=EasyPokerStrategy(), image_name='casino_easy')
        objects.append((e_poker_table, Coord(3, 1)))

        # medium poker
        m_poker_table = OneCardPokerComputer(strategy=MediumPokerStrategy(), image_name='casino_medium')
        objects.append((m_poker_table, Coord(5, 1)))

        # hard poker
        h_poker_table = OneCardPokerComputer(strategy=HardPokerStrategy(), image_name='casino_hard')
        objects.append((h_poker_table, Coord(7, 1)))


        slotmachine2 = SlotMachineUtility(image_name ="slot_machine2")

        for x in range(0, 15):
            if x != 11 and x != 10:
                coord = Coord(0, x)
                slotmachine_copy =  slotmachine2.clone()
                objects.append((slotmachine_copy, coord))

        return objects

