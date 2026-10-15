# MK2 Kano/Sonya — native cannonball milestone (v42)

This is a verified milestone, not completion of the full natural-roster goal.

## Installed build

- Active project: `C:\Users\kando\Documents\Codex\2026-08-29\i-ha\work\mk2port`.
- `mame-mkp/mkport.exe` SHA-256: `413855890FCE3BECAC9B24E11699FAD1CE465ACCBE4B27A93F2DD5819D13A891`.
- Payload and program chips are unchanged from v41. `mk2ks.mdata` SHA-256: `2F29937E0144FE54E490BB6D6C0BEBB99496CDF551F228C38F975F7EFEED31FF`; `mk2ks.ui`: `DBC1881B4696ACD33393D47DCBF626239B91EB6D8DB581003D4774A2F97483EB`.
- Recovery executable: `regression_v42_cannonball/mkport_v41.exe`, SHA-256 `6210AFF61D58C50B6E3D8CC3DBECAD2186DEB244D6483DAC8E43C198830A6F97`.
- Both lifecycle cases ran through the exact forwarding CMD in the current task folder, without a snapshot-view override. Its `-verifyroms` check passes. Build and `git diff --check` pass; no emulator processes remained after acceptance.
- This remains a custom-emulator port, not a ROM compatible with unmodified MAME.

## Kano cannonball

Hold Low Kick, then release. Kano's own native LK-release table entry now uses MKII's per-player press timestamp and grounded/action-ready gate. The original MK3 parser requires **more than 80 ticks**, not the approximate three-second hold sometimes quoted in guides. The port rejects an 80-field hold and accepts 81; holding without release, a short/repeated-short hold, the wrong button, or release while airborne does not activate it.

The routine uses Kano's own eight-composite rolling animation, native scheduler, movement, collision, damage, rebound and landing. No input injection, character-ID substitution, generic CPU table alias or borrowed Liu special routine was added. Its human knockdown/block reaction indices use compatible shared MKII reactions; exhaustive victim fidelity is not yet claimed.

- Flight: ten pixels per field, origin Y shifted down 16 pixels, up to 26 fields, first six fields without a collision check.
- Hit: 24 damage, rolling rebound at five pixels per field backward.
- Block: five chip damage, rolling rebound at one pixel per field backward.
- Rebound starts at eight pixels per field upward with native gravity `6000h`; ordinary landing restores stance/action readiness.
- Miss: stop and restore own floor after 26 fields. A ducking opponent is passed over without damage.

Loaded-program byte allocations (TMS address = `FF800000 + byte*8`):

- `FFB60..FFBBF`: charge/release parser. Native LK-release table `FF4F0 + 17*4` points here.
- `FFBC0..FFD7F`: Kano-owned action routine.
- `FFD80..FFD9F`: native attack descriptor, hitbox `(57,14,72,31)`, damage/chip `1805h`.

The existing converted main-animation 7 contains the eight exact original roll composites and native loop token. It is used instead of the older three-pose flying-kick list. No body payload regeneration was needed.

## Original-game reference

`mk3_cannonball_reference.lua` runs real controls and read-only observation against original MK3 rev 2.1 in stock MAME 0.289. Completed `diagnostic_v42_mk3_ball_ground` and `diagnostic_v42_mk3_ball_block` demonstrate the original ten-pixel flight, +16 origin, seventh-field first collision check, 24/5 damage, five/one-pixel backward rebound and grounded recovery.

Original parser `FF97CE80` uses helper `FF97EF90`, timestamp `01062490` and strict `>0050h` comparison. Original action is `FF9E6350`, attack descriptor `FFA5B520`, main-animation 26 root `FF828960`. The charge boundary was dynamically tested in the port; the original boundary is established from its parser, not claimed as a separate original-game input test.

## Final verification — 64 emulator cases, three asset tests

All 64 final cases passed on the executable hash above. Their individual `result.json` files and `regression_v42_cannonball/acceptance.json` identify the exact build. Inputs are ordinary emulated controls; health, positions, actor IDs and input histories are not patched. Optional diagnostic pinning in the older basics harness is disabled.

- **20 cannonball cases:** `regression_v42_ball_{kano,sonya}_{hit,block,miss,short,boundary,minimum,held,airborne,recharge,wrong_button}`. The fighter in the directory name is P1, so the `sonya` set exercises Kano on P2. Hit/minimum have 24 damage, 12 flight fields and 42 rebound fields; block has five damage, 13 flight fields and 42 rebound fields; miss has zero damage, 26 flight fields and no rebound. Negative cases have zero own roll entries/collision reads. All require exact trajectory/startup/collision counts, recovery, and a subsequent knife action (except the intentionally still-held case). Each also passes overall display, shadows, names, identity, cleanup and 1,243 combat fields without a stall or trap.
- **20 square-wave cases:** `regression_v42_square_{kano,sonya}_{ground,air,block,air_block,far,reversed,expired,wrong_button,airborne,with_block}`. Both Sonya sides retain v41's strict trajectory, anti-air damage, miss/rejection and subsequent ring-action checks.
- **16 knife/ring cases:** `regression_v42_commands_{kano,sonya}_{native,legacy,chord,reversed,expired,wrong_button,airborne,with_block}`. Positive commands and all seven negative classes retain overall display/shadow/identity/stability checks.
- **Two exact-CMD lifecycle cases:** `regression_v42_cmd_{kano,sonya}_lifecycle`. Each has 556 selection/transition identity checks, one ladder entry, two recoveries, one next-round reset, native finish/continue release, seven shadow checks, and 1,775/1,776 combat fields. Zero leaks, name/identity/ground errors, stalls or traps.
- **Two basics cases:** `regression_v42_basics_{kano,sonya}`. All 20 actions pass; 2,215/2,226 combat fields with zero roster/identity errors, stalls or traps.
- **Two victory cases:** `regression_v42_win_{kano,sonya}`. Two native wins each, own names/poses, correct lifebar shadows, 2,336 combat fields without errors.
- **Grid/navigation:** `regression_v42_grid` passes all 31 checks; `regression_v42_navigation` passes all ten, retaining native border/number/blink and zero-displacement assertions.
- `python tools/test_native_projectiles.py`: all three asset tests pass.

Reproduce special suites with `tools/run_native_cannonball.ps1 -CasePrefix NEW_PREFIX`, `tools/run_native_square.ps1 -CasePrefix NEW_PREFIX`, and `tools/run_native_commands.ps1 -CasePrefix NEW_PREFIX`. Runners refuse to overwrite evidence, check the executable hash before/after every case and clear other special-test modes.

Reviewed snapshots include both P1 hit/rebound and P2 block/ducked-miss captures, plus `regression_v42_cmd_sonya_lifecycle/snap/mk2ks/0014.png` (own ladder icon, no selector leftovers) and `0016.png` (Sonya versus stock Sub-Zero, shadowed lifebar names). The v41 stock-palette shadow fix is retained on both names and player sides.

`diagnostic_v42_kano_ball_hit` is not acceptance: its early follow-up observer counted projectile-object reads in addition to fighter-object reads. The observer now filters by the actual Kano actor, and every final case uses the corrected assertion. Five intermediate controlled ball diagnostics also passed but are not included in the 64-case count.

## Remaining full-goal work

Kano's other specials/grabs, Sonya's remaining specials, complete move/throw/victim semantics, voices, finishers, mirror alternate outfits, AI participation and all later ladder/ending/reselect/join routes still need implementation and verification. Cannonball and square-wave interruption/crossing/boss-target behavior need further coverage. Two imported body-palette compatibility hooks remain. Do not equate this milestone with a completed character port.
