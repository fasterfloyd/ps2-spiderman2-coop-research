SPIDER-MAN 2 (PS2, 2004 USA) — v8.1 FACTORY NAME FIX

WHAT WE FOUND
The v8 test returned no object. Its one-shot MIPS dispatcher passed a selector pointing at 0x00677230, the uppercase string "SPIDERMANX". The native factory at 0x004CC080 compares it against the registry pointer at 0x0060A274, which is 0x00677220 in all five uploaded save states; that string is the lowercase "spidermanx:". Because the strings do not match, the factory skips the SPIDERMANX allocation branch at 0x004CDDBC.

THIS PATCH CORRECTS THAT SPECIFIC BUG.
It changes ONLY ONE .pnach word:
patch=1,EE,000FDA00,word,00677230
        becomes
patch=1,EE,000FDA00,word,00677220
It leaves the existing v6 bridge and v8 code intact. The corrected test GUI also checks the name registry at runtime.

HOW TO TRY IT
1. Back up your 100% memory-card save and any save states. Close PCSX2 fully.
2. Extract this zip. Double-click FIX_V8_TO_V81.bat. Select the exact folder containing your existing v8 SLUS-20776_E2DFCE12.pnach file.
3. The script creates a timestamped .pnach backup before editing. If it refuses, it changes nothing.
4. Restart PCSX2, enable v6 and v8 cheats if not already enabled, enter free roam.
5. Open TRY_SECOND_SPIDERMAN_V81.bat and click TRY CREATE SECOND SPIDER-MAN ONCE.
6. Screenshot the response AND check whether the game renders another character.

WARNINGS
This is an unverified in-game creation experiment, NOT confirmed co-op or a visible second Spider-Man. Correcting the name will allow the real construction branch to be attempted, but that call may still crash, return null, or create an actor without rendering it. The v8 dispatcher reuses Player 1's entity identifier pointer, which could cause conflicts. DO NOT save during testing. If a crash or instability happens, close PCSX2 and run UNDO_FIX_V81.bat (or disable the entire v8 cheat). Do not press the button repeatedly in the same game session.

No need to install this fixer if v8 was removed; this tool expects v8 already installed. It does not create or install v8 itself.
