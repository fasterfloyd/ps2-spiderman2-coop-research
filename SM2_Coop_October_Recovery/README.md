# Spider-Man 2 PS2 — October Co-op Recovery Pack

**Status: NOT PLAYABLE TWO-PLAYER CO-OP.** Recovered prior research and test code, not a completed game or verified new patch.

Target: Spider-Man 2 (2004) PS2 USA, SLUS-20776, PCSX2 ELF CRC E2DFCE12. Prior inspected ELF SHA256 `1ed83d628bdb7d9824ba793a6f0954da9a43b081231d1dbc1c69d168208eebbb`.

## Confirmed from the October files
- v7 read-only actor probe recorded `SPIDERMANX` object at `0x00B305A0`, class `0x39`, vtable `0x00646D20`. Only validated for earlier snapshots; it can move between sessions.
- v8 experimental native factory call at `0x004CC080` attempted to create an actor, but its class-string pointer `0x00677230` was wrong.
- v8.1 corrected the selector to `0x00677220` (`spidermanx:`). It remains **unverified** for visible spawning and may crash because it reuses Player 1's entity-ID pointer.
- There is no evidence of independent Player 2 input, a second camera, or online state synchronization working.

## Package contents
- `prior-experiments/v7_actor_probe` original read-only scripts.
- `prior-experiments/v8_factory` original one-shot factory experiment. **Risky**, may crash; requires previously installed v6 bridge.
- `prior-experiments/v8_1_fix` original one-word correction for an already installed v8 patch. **Risky**, not automatically installed.
- `tools/audit_patch.py` read-only inspection of an existing `.pnach` file; never edits PCSX2.
- `research/` recorded findings.

## Fast next step
1. In PCSX2, confirm SLUS-20776 and CRC E2DFCE12 in game properties.
2. Run `python tools/audit_patch.py "C:\path\to\SLUS-20776_E2DFCE12.pnach"` to check whether the expected v8/v8.1 lines are present. Script is **read-only**.
3. Read the original v8 and v8.1 README files before attempting any experiment. Back up memory cards and save states. Disable prior conflicting cheat groups. Never test on your only save.
4. Record the result of any existing v8.1 test: stage/status, returned object pointer, on-screen visibility, crash or freeze, and a screenshot. A pointer is **not** proof of a visible character.
5. If the factory works, next reverse engineering tasks are unique entity registration, actor insertion into scene/update lists, animation/render, Player 2 input ownership, then eventual network synchronization.

**No copyrighted game disc images or executable binaries are packaged.** This pack does not modify your original game files and makes no runtime changes by itself.
