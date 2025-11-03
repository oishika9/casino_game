from ..imports import *
from typing import List
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from coord import Coord
    from maps.base import Map
    from tiles.base import MapObject
    from tiles.map_objects import *
    from NPC import NPC


class NPCBouncer1(NPC):
    """
    An NPC that sends a list of dialogues one-by-one each time the player interacts.
    After all dialogues have been shown, it prompts the player for their age.
    If the player's age is less than 18, the NPC teleports the player to Trottier Town.
    """

    def __init__(self, dialogues: List[str], staring_distance: int = 0) -> None:
        """
        Initialize NPCBouncer1 with the given dialogues and staring distance.

        @Preconditions:
            - 'dialogues' must be a non-empty list of strings.
            - 'staring_distance' must be a non-negative integer.
        """
        assert dialogues, "Dialogues list must not be empty."
        super().__init__(
            name="Bouncer",
            image='prof',
            encounter_text=dialogues[0],
            staring_distance=staring_distance,
        )
        self.dialogues: List[str] = dialogues
        self.prompt: str = 'Tell me your age? (Please type /age/<your_age> in chat)'
        self.teleport_room: str = 'Trottier Town'
        self.dialogue_index: int = 0  # Tracks which dialogue has been shown so far.
        self.waiting_for_input: bool = False  # True when the NPC is waiting for age input.
        self.conversation_finished: bool = False  # True once the conversation is complete.

    def player_interacted(self, player: "HumanPlayer") -> List:
        """
        Generate dialogue messages when the player interacts with the NPC.

        @Returns:
            A list of message objects (DialogueMessage) representing the dialogue sequence.
        """
        messages: List = []
        if self.conversation_finished:
            # Conversation already complete; no further messages.
            return messages

        if self.dialogue_index < len(self.dialogues):
            messages.append(
                DialogueMessage(self, player, self.dialogues[self.dialogue_index], self.get_image_name())
            )
            self.dialogue_index += 1
        else:
            messages.append(
                DialogueMessage(self, player, self.prompt, self.get_image_name())
            )
            self.waiting_for_input = True

        return messages

    def process_player_input(self, player: "HumanPlayer", input_text: str) -> List:
        """
        Process the player's input (expected to be their age) and return appropriate messages.
        
        @Preconditions:
            - input_text must be a string that can be converted to a positive integer.
        
        @Postconditions:
            - If the age is less than 18, the player is teleported to Trottier Town.
            - Otherwise, a welcome message is returned.
            - The conversation state is reset and locked.
        
        @Returns:
            A list of message objects (DialogueMessage and/or ServerMessage) reflecting the outcome.
        """
        messages: List = []
        if self.waiting_for_input:
            try:
                age = int(input_text)
                # Assert that the age is a positive number.
                assert age > 0, "Age must be a positive integer."
                if age < 18:
                    messages.append(
                        ServerMessage(player, "Teleporting you to Trottier Town...")
                    )
                    messages.append(
                        DialogueMessage(self, player, "You are too young!", self.get_image_name())
                    )
                    # Teleport the player via the room's teleport object.
                    player.get_current_room().teleport.player_entered(player)
                else:
                    messages.append(
                        DialogueMessage(self, player, "Welcome! You may continue your journey.", self.get_image_name())
                    )
                    print("Player meets the age requirement.")
            except (ValueError, AssertionError) as e:
                messages.append(
                    DialogueMessage(self, player, "Please enter a valid number for your age.", self.get_image_name())
                )
                print("Invalid age input:", e)
            finally:
                print("Finished processing player input.")
                # Reset conversation state.
                self.waiting_for_input = False
                self.dialogue_index = 0
                self.conversation_finished = True

        return messages