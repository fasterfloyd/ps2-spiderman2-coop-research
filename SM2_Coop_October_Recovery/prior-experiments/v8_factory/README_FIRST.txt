Spider-Man 2 (2004) PS2 USA — SECOND SPIDERMAN FACTORY TEST v8
Game SLUS-20776 / CRC E2DFCE12 ONLY

EXPERIMENTAL, UNVERIFIED IN PCSX2. NOT A WORKING TWO-PLAYER MOD.
This is the first one-shot attempt at calling the game's actual SPIDERMANX character factory via custom injected MIPS code. It uses Player 1's existing entity identifier pointer; that might be invalid for a second actor, causing a crash, a duplicate ID conflict, or no visible character. It does NOT spawn a guaranteed visible second Spider-Man or enable player control. You are responsible for backing up saves.

INSTALL / TEST
1. Copy your 100% save somewhere safe. Turn off autosave if applicable. Do not save progress during this test.
2. Keep the previously verified Player 2 v6 bridge INSTALLED and remove older experimental v3/v4/v5 tracers.
3. Fully CLOSE PCSX2. Double-click INSTALL_V8.bat, choose your existing PCSX2 cheats folder.
4. Restart PCSX2, ensure both the v6 bridge and v8 experiment cheats are enabled, and load a free-roam game.
5. Enable the PINE IPC port 28011, as in v6. Double-click SHOW_SECOND_SPIDERMAN.bat, press TRY CREATE SECOND SPIDER-MAN exactly once.
6. It reports whether the native factory returned a second SPIDERMANX object. Look around in-game for the second Spider-Man. An object pointer alone is NOT proof it renders.
7. If PCSX2 freezes/crashes or Player 1 disappears, CLOSE PCSX2, run REMOVE_V8.bat and restart. Restore your backed-up save if needed.

TECHNICAL
The original hook at 0x00519234 calls the existing v6 stub at 0x000FF000. v8 replaces exactly its 0x000FF054 JAL, routing it through code at 0x000FD800. A PINE request at 0x000FF114 makes a guarded ONCE-only call to the native game class factory 0x004CC080. The class name comes from the game's own "SPIDERMANX" string at 0x00677230. The duplicate ID pointer comes from the existing actor at 0x00B305A0. Return pointer at 0x000FF118, stage at 0x000FF11C. The renderer/scene inclusion/AI and independent P2 control are NOT implemented.

The installer backs up the existing .pnach and preserves other unrelated cheat groups. The no-write test scripts don't modify the game's ISO or memory-card. Code assembly and patch merging were checked offline; gameplay success CANNOT be inferred without running in your PCSX2.
