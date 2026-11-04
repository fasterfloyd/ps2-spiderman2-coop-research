SPIDER-MAN 2 PS2 — PLAYER 2 ACTOR PROBE v7

This tool READS the live game. It DOES NOT spawn or control Player 2. It does not install cheats, modify saves or write any game memory.

NEW verified discovery from your game files:
 - The SPIDERMANX class has category 0x39 and allocation size 0x7D8.
 - Factory class-registration instruction at 0x004CDDBC allocates 0x7D8 bytes and 0x004CDDD0 calls initializer 0x002B9044.
 - All FIVE previously uploaded save states contain an instance at 0x00B305A0.
 - Class method-table pointer at actor+0x10 is 0x00646D20, category at actor+0x14 is 0x39 and actor+0x20 contains 'SPIDERMANX'.
 - These fields identify a game entity of the player-related class, but do not prove that it is independently renderable.

QUICK TEST:
 1. Leave your verified v6 P2 patch installed and open Spider-Man 2 in PCSX2.
 2. Run CHECK_PLAYER_ACTOR.bat from this folder.
 3. Walk or swing Player 1 around for 10 seconds while the recorder runs.
 4. Share P2_ACTOR_PROBE_V7.json.

This checks for a live player-class object and produces candidate motion-related fields to inform the first real actor-duplication test. It doesn't find NPC creation by itself.

If v7 says the actor was not found, DON'T attempt to patch the listed address: object addresses may differ with loading, memory layout or versions.

Safety: read only, no changes to your v6 cheat. Backing up saves is always recommended before modifying any game code.
