# MK2 Kano/Sonya — native command and runtime-table repair (v40)

Historical milestone: the installed v42 build and current 64-case evidence are documented in `STATUS_2026-09-05_CANNONBALL.md`. The v41 square-wave and both lifebar shadows are retained.

This is a verified milestone, **not a finished full-character port**. Both fighters remain their actual IDs through selection, ladder, combat and tested round transitions. The input/character proxy is removed. Knife and ring commands now have native records and release routines; the rest of their independent specials, finishers, voices, alternate outfits and full progression remain unfinished.

## Installed build and launch

- Active project: `C:\Users\kando\Documents\Codex\2026-08-29\i-ha\work\mk2port`.
- `mame-mkp/mkport.exe` SHA-256: `94FA414EAF4778B4E68F8FDD90D852319F80B6038D831AFE94071A07B644933C`.
- Installed `roms_v22_clean/mk2ks/mk2ks.mdata` is unchanged from v39: SHA-256 `2F29937E0144FE54E490BB6D6C0BEBB99496CDF551F228C38F975F7EFEED31FF`, CRC `44421fbb`, SHA-1 `55a18f010bc7598de254a060772ca5f38c1c7c47`.
- Program chips are unchanged. Loaded-ROM table/code extensions are applied by `init_mk2ks()` in the custom executable. This is not a standalone ROM for unmodified MAME.
- The current task's forwarding `PLAY_MK2_KANO_SONYA.cmd` invokes the active project's launcher. ROM verification and a two-second headless boot through that exact forwarding CMD pass.
- The launcher now explicitly uses the project's `artwork` directory. `artwork/mk2ks/default.lay` contains only the native game screen, no portrait/bezel elements. Stock MK2 artwork in the emulator source tree is untouched.
- Build and `git diff --check` pass. One intermediate link attempt failed because a test was still running; the subsequent completed link produced the hash above. No emulator processes remained after final verification.
- Recovery executable from v39: `regression_v40_native_commands/mkport_v39.exe`. It uses the same installed payload. Do not confuse intermediate v40 builds with final acceptance evidence.

## What changed

An audit found a remaining broad CPU read alias: P1 character-table reads using IDs 17/18 were silently redirected to entry 1. This did not overwrite the visible/canonical ID, but it still borrowed Liu's callback/parameter rows. It has been deleted, along with global animation-root/move rewriting, input-injection handlers and their scanline observer/state. Both sides now reach their actual native table entries.

The twelve command tables added in v39 now give the added IDs a native no-special result by default. Only implemented custom commands are bound. This intentionally removes the old F,F and Block+button convenience specials rather than claiming their borrowed semantics are complete.

- Kano: **Down, Back + HP** throws his knife.
- Sonya: **Down, Forward + LP** releases her rings.

Each has an independent native command-history record, forbidden-button mask, parser and standing release routine. They use MKII's own input history, grounded/action-ready gate, scheduler, animation and projectile/hit primitives. There are no generated inputs or temporary character-ID substitutions. Release audio omits Liu's character voice. Existing converted native projectile graphics/palettes from v39 remain unchanged.

Removing the alias exposed genuine missing tables. These now have explicit rows for both new characters:

- Forward/backward walk packed cadence/speed. The old backward lookup read adjacent instructions as `0xC1000` motion, exceeding the camera's supported range and trapping at `FF9F96F0`.
- Contextual high-punch override. The old lookup jumped to instruction data `03B40D3F`.
- Standing block cadence.
- Shared human throw dispatch, paired-throw cadence, thrown alignment and landing callbacks. A close-range P2 Sonya throw previously indexed beyond `FF8B8440` and trapped at `FFA1E800`. New entries use shared human primitives and the actors' own animation tables, not Liu's special voice/continuation.

The two legacy imported **body-frame palette metadata** compatibility hooks still exist in the CPU. They are not identity/input proxies. Converting all remaining donor body frames to fully native data remains separate work; do not describe the entire port as free of emulator compatibility code.

## Loaded-ROM allocations

Byte offsets are relative to the 1-MiB main program; TMS address = `FF800000 + offset * 8`.

- `FF540`, `FF560`: facing-aware command records, 36-field history window.
- `FF580`, `FF5C0`: knife/ring parsers; `FF600`, `FF680`: own release routines. Reserved through `FF6FF`.
- HP dispatch entry at `FF180 + 17*4` points to Kano's parser; LP event table `FF1D0 + 18*4` points to Sonya's parser. Event order is HP, LP, Block, HK, LK, not raw input-port bit order.
- `FF700`: forward packed parameters, source `FF906AB0`, operand `FF906990`.
- `FF750`: backward packed parameters, source `FF906CD0`, operand `FF906910`.
- `FF7A0`: contextual HP callbacks, source `FF8333E0`, operand `FF833320`.
- `FF7F0`: block packed cadence, source `FF8702C0`, operand `FF8700D0`.
- `FF840`: throw callbacks, source `FF8B8440`, operand `FF8B6C10`.
- `FF890`: throw landing callbacks, source `FF8E5310`, operands `FF8B8250`, `FF8B8B40`, `FF8B8F90`.
- `FD580`: throw word cadence, source `FF8B9460`, operands `FF8B8870`, `FF8B8A20`.
- `FD5C0`: thrown word alignment, source `FF8B9A30`, operand `FF8B98B0`.

Existing rows are preserved. Allocations check vacant storage and supported source operands before modifying loaded ROM.

## Final verification — 24 emulator cases and 3 asset tests

All final cases below ran the `94FA414E...B644933C` executable with the unchanged v39 payload. No emulated character/position/health writes or pinning were used. Every listed case reports its overall pass result, not just successful command rejection.

- `regression_v40_final_{kano,sonya}_{native,legacy,chord,reversed,expired,wrong_button,airborne,with_block}`: 16 cases, both actual custom players. Positive commands each produce eight native projectile-entry word reads per side, converted-frame reads and damage to both players (health 73/73 after four hits each). All seven negative input classes produce zero projectile entries/frame reads. Each case observes 2,337 combat fields, zero stalls/traps, identity/name errors or portrait leaks. Main display target has one native screen and no external art.
- `regression_v40_final_basics_{kano,sonya}`: 20 basic-action checks each; walking, jumping, flips, crouch/block, punches/kicks, uppercut, sweep and roundhouse all reach expected own animation entries. 2,215/2,226 combat fields, zero stalls/traps or identity errors.
- `regression_v40_cmd_{kano,sonya}_lifecycle`: launched through the exact user-facing forwarding CMD, with default automatic snapshot view (not a raw-screen-only override). Both retain native IDs for 556 checked pre-HUD fields, read their native ladder entry, recover twice and rebuild once for the next round. Zero leaks, identity/name/ground/position errors, stalls or traps. Main and snapshot targets both report `Native game`, `has_art=false`. 1,775/1,776 HUD-visible combat fields; native loss/continue actor release is also observed.
- `regression_v40_final_{kano,sonya}_win`: both players are custom fighters; real walk/uppercut inputs win two rounds. Own native KANO WINS / SONYA WINS scripts and own victory poses are visible, with zero identity/name/leak/stability errors across 2,336 combat fields.
- `regression_v40_final_grid_full`: all 31 actual-input directional checks pass, with correct canonical/live IDs and all 1,064 native border pixels.
- `regression_v40_final_navigation`: ten checks pass; 1,064 border pixels, 66 player-number pixels, two blink colors, animated Sonya pose and zero measured background shift.
- `python tools/test_native_projectiles.py`: all three asset tests pass.

Reproducible command suite: `tools/run_native_commands.ps1 -CasePrefix NEW_UNIQUE_PREFIX`. It refuses to overwrite evidence, checks executable hashes before/after every case and rejects any overall stability/display failure. Lua observers release their taps before emulator teardown. Optional `MK2KS_TRACE_TABLES=1` is read-only and restricted to suspected table tails, not the whole ROM.

## Visual evidence inspected

- `regression_v40_cmd_sonya_lifecycle/snap/mk2ks/0001.png`: native Sonya highlight, centered number and own pose.
- Same directory `0014.png`: native Sonya ladder icon; selector portraits/pose are gone.
- Same directory `0017.png`: Sonya defeated by Sub-Zero, no selector portraits over the HUD. `0021.png` also has no selector overlay later in the loss sequence.
- `regression_v40_final_kano_win/snap/mk2ks/0019.png` and corresponding Sonya directory: own fighters, names and victory scripts.
- `regression_v40_final_kano_native/snap/mk2ks/0073.png`: P2 Sonya rings hitting Kano with their native effect palette.

## Intermediate failures — not acceptance

- `regression_v40_negative_*` and `diagnostic_v40_narrow_*`: real contextual-HP/walk-table crashes before repair.
- `diagnostic_v40_basics_kano`: backward movement froze the camera; only two basic checks passed.
- `regression_v40_parameters_*`: walk/contextual repair passed, but later throw coverage was still missing.
- `regression_v40_verified_kano_legacy`: real P2 throw crash; the prefix name does not make it accepted. Final repaired rerun is `regression_v40_final_kano_legacy`.
- `regression_v40_final_grid`: its 30-second window ended after 22 successful checks. It was incomplete, not a passing test. The full 45-second rerun is `regression_v40_final_grid_full`.
- Original whole-ROM diagnostic taps were intentionally stopped and replaced with narrow read-only taps because they imposed excessive observer overhead. Their incomplete traces are not game-stability evidence.

## Still open

The full natural-roster goal remains active. Only the knife/ring specials now have native independent command/release paths. Kano's ball/grab and Sonya's other specials, exact move/hitbox/timing semantics (including throws), finishers, voices, mirrors' alternate outfits, AI participation, all later ladder/ending/reselect/join routes and remaining animation mappings still require implementation/verification. Do not restore a blanket Liu read alias or shortcut input injection to make unfinished paths appear functional.
