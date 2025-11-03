# CasinoRoyale

## COMP303 project. Casino Royale is a Virtual Entertainment Hub where players can experience a lively and engaging environment inside an interactive casino-themed virtual space.

MAIN DESIGN PATTERNS USED:
-Singleton: Ensures one instance of components like DJ, BalanceManager, and Scoreboard
-Command: Encapsulates player inputs (chat and menu commands) such as /age, /balance, Deal, Hit, Stand, Quit, play, next, etc.
-Observer: Decouples events from reactions (balance changes trigger sounds and UI updates; horse-race outcomes update a scoreboard sign), winning and losing triggers different sound effects, etc.
-Strategy: Varies payout logic for slot machines (StandardStrategyWithWheel, JackpotStrategy) and playing difficulties for poker.
-Prototype: Enables cloning of NPCs and utility objects for reuse without reinitialization.

---

(Entrance):
NPC Interaction: Meet the Bouncer (NPCBouncer1)
-Steps through a dialogue sequence.
-Prompts for the player’s age using /age/<your_age> (AgeChatCommand).
-Teleports underage players back.

---

(Bar):
Drink Ordering: Approach the bar counter and choose from menu options (BarMenuComputer):
-coke - $5.00, vodka coke - $17.00, vodka - $12.00 (BarCommand).
DJ Booth: Use menu options on the DJBoothComputer to control music:
-play, next, previous, shuffle (DJPlayCommand, DJNextCommand, etc.)
-Visual emotes flash in rhythm with the music.

---

(Casino):
SlotMachine, Blackjack, Poker

---

(Ranch - extension of casino):
Bookmaker NPC: Interact with HorseBookmaker to start horsebetting
ScoreboardSign displaying cumulative wins
