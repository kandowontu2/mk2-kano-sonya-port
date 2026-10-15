# Native Kano blade swipe — separate v44 candidate

Historical first-blade milestone. Current follow-up source/build and native
sound/blood work are documented in `STATUS_2026-09-05_BLADE_FEEDBACK.md`.
The user-requested v44 WIP ZIP now contains this first-blade executable;
the newer feedback candidate remains separate. The installed CMD remains v42.

The full natural-roster goal is still unfinished. This turn made implementation
progress: a previously absent command now runs an independent native action
with its real body/effect sequence, damage, recovery and interruption cleanup.
The preceding release task verified the requested v42 ZIP. That ZIP and the
installed launcher build have not been replaced with this candidate.

## Exact build

- Executable: `diagnostic_v44_blade_candidate/mkport_blade.exe`, SHA-256
  `A3479747FBE10CE8F191CF2EA40FE8E6F949FA46FBB02984B84839B832401AF0`.
- Required payload: `diagnostic_v44_blade_candidate/roms/mk2ks/mk2ks.mdata`,
  `91001C2E6551CB850F919971D67806DE31D5F34D97C6CE0D9764B4F367F19DB3`.
  CRC32 `bd3a6d13`, SHA-1 `5d89dc9b34da9ec7a87fd277ee76fa5ac007f3c9`.
- Combined program remains
  `2444C00C201F849D4242A51D9FE85585C8A7AFCCF3145391F270F80C6F1CA0E8`.
- Working `midtunit_m.cpp` at build/verification:
  `4841867EFD8E33E01C37FCF0E29676B2190086DB08B522BB83083AB39DCDAF12`.

The builder integrates `tools/build_native_blade.py` after the existing native
projectile conversion. Exactly 7,700 payload bytes changed, all within the new
`1D0000..1DFFFF` allocation; the complete payload outside that region is identical
to the v43 jump/contact/edge payload. Existing donor body composites, projectile
assets, jumps and leg-grab data are unchanged. The native program patch is in
the executable, as with the earlier candidates.

## Original behavior and implementation

Original MK3 action `FFA2BB70` recognizes D,F+HP and uses action `0117h`.
Its ten body poses are `FF82FC40..FF82FFA0`, with a separate one-component
trail in groups `FF830000..FF830240`. Its palette is `FFC96600`: indices 13+
include blue/green trail colors that are not in Kano's body palette. Combining
the effect with the fighter or recoloring it through the body palette would
not preserve the original visual or collision separation.

The converted effect has ten native 18-byte descriptors at payload `1D0400`
(20-byte stride), a native 64-entry palette at `1D0100`, and 7,404 packed 6-bpp
pixel bytes at `1D4000`. Header `1D0000` is `KBL1`. Pixels are copied once to
unused graphics byte `1E08000`. Original X/Y offsets are preserved exactly;
the travelling knife's separate release-hand adjustment is NOT applied.

Checked free loaded-program bytes `F1900..F21FF` contain:

- `F1900` parser, `F1940` input record, `F1980` action.
- `F1B00` effect creation, `F1C00` native frame update/alignment.
- `F1C80` strike descriptor, `F1D00` phased body/trail script.
- `F1F00` native frame descriptors, `F2000` own victim reaction.

The HP parser chains to the existing knife parser on rejection and uses MKII's
real input-history matcher and grounded/action-ready gate. No input synthesis,
identity substitution, host drawing hook or idle render process was added.

The effect uses MKII single-frame allocation (`FF83ADA0`), frame updates
(`FF840B60`) and origin/facing alignment (`FF83E8F0`). Its descriptors are copied
to program ROM because the stock single-frame updater legitimately rejects
pointers below `FF800000`; that global guard is left intact. The parent process
owns the effect in its native attached-object slot at `+190`. Normal recovery
and hit handoff release the palette and delete the effect through `FF83EFD0`.

Pose durations are `2,2,2,2,2,4,4,12,4,4`, totaling 38 fields. The three original
phases retain the eight-field pause after pose seven. Relative advances are
`0,8,8,8,11,11,11,0,0,0`: 57 pixels when unobstructed. Native body pushing and
stage clipping remain active. There is exactly one collision check ten fields
after entry, with original bounds 109/20/75/67, 26 damage or 3 block damage.
Recovery action is `0618h`. Kano's independent reaction row 25 uses MKII hit
setup and semantic stumble animation 35 (MK3 animation 32), including the
six-pixel initial recoil/eight-field delay followed by four-pixel recoil.
Complete per-victim/KO semantics and audiovisual feedback are not yet accepted.

## Evidence and corrected observers

`diagnostic_v44_blade_baseline_side1_sonya_near` proves that the unchanged v43
edge build does not activate this move: zero blade entries/effects/strikes.
The first v44 case enters once, updates all ten poses, deals 26 damage and
recovers, but retains a red result for one premature palette-RAM observation.

The native palette allocator queues its upload. Frame notification occurs
before that queue is drained on the first allocation field. The final observer
watches the actual queue at `FF80C6B0` and completed upload at `FF80CA00`:
P1 near queues at field 1503 and uploads all 64 colors at 1504. It verifies the
first palette at that upload and each subsequent animation field directly in
palette RAM, rather than skipping the first color check or changing the game.
All ten effect origins and facings are checked at native alignment completion.

The original clean Liu reference misses an airborne Liu. That is not a rule
that every airborne fighter must be missed. The original Sonya reference
`diagnostic_v44_mk3_blade_sonya_air_selected` asserts actual victim ID 1, observes
Sonya near the jump apex (Y=8, floor=103), and records 166 -> 140 health at field
3919. The matching port Sonya cases hit for 26 and recover normally. The first
attempt at selecting original Sonya actually selected ID 5; its directory
`diagnostic_v44_mk3_blade_sonya_air` is retained and is not Sonya evidence.
The earlier port airborne diagnostics retain their red results from the wrong
universal-miss expectation. No collision code was changed to satisfy it.

Interruption uses an actual opposing uppercut after the blade trail appears.
P1 Kano's original diagnostic shows damage and native effect cleanup both at
field 1513, with the cleared slot visible in the next frame sample. The final
test measures cleanup against those actual events, not a guessed earlier field.
For P2 Kano, the counter starts one field earlier to beat native task priority;
the unchanged original timing legitimately let Kano win the simultaneous hit.
Both final cases require one entered/created swipe cancelled before its strike,
40 uppercut damage, no remaining blade frame in the display list, released
palette references, then one fresh swipe causing 26 damage and native recovery.

## Current-build verification

`tools/verify_blade_candidate.ps1` validates an exact 88-case inventory and
records its results in `diagnostic_v44_blade_candidate/verification.json`:

- 10 `regression_v44_blade_sonya_*` cases: both player sides, near, far,
  standing block, crouching block, and actual airborne Sonya contact.
- 8 `regression_v44_blade_mirror_*` cases: both Kano mirror sides, near, far,
  standing block and crouching block. Both original body outfits and the
  independent trail palette stay correct.
- 2 `regression_v44_blade_interrupt_*` actual interruption/retry cases.
- 16 existing knife/ring command cases, 20 cannonball and 20 square-wave cases
  under `regression_v44_blade_{commands,ball,square}_*`.
- 12 `regression_v44_blade_core_*` cases: both mirrors, jumps, ladder/loss
  lifecycles, native wins, basics, 31-check selection grid and 10-check navigation.

All 18 complete swipe cases check exactly 38 body poses, 38 palette observations,
10 aligned trail frames, one creation/nine updates, one ten-field collision and
normal teardown. The broader cases retain identity, shadow, display and trap
checks. Diagnostics are not included in the 88-case inventory. All 20 asset
tests pass; six are new blade conversion/allocation/palette/phase tests.
`git diff --check` passes. All emulator sessions are terminal; no test emulator
process remains.

Reviewed captures include P2 alternate-outfit Kano's mirrored swipe in
`regression_v44_blade_mirror_side2_kano_near/snap/mk2ks/0022.png`, and the
interrupted P2 Kano uppercut in
`regression_v44_blade_interrupt_side2_sonya_interrupt/snap/mk2ks/0022.png`.
The blade trail is absent after the latter hit while ordinary native blood and
the correct lifebar names remain visible.

The verified installed v42 executable/payload and portable release ZIP remain
unchanged, as do the preserved v43 executable/payload. Never run the new v44
executable with the old payload. Rebuilding the current working sources now
requires the new blade payload, not the v43 payload documented in older notes.

## Still required

This is a real implemented move, not full move or port acceptance. Blade-only
rejected-input tests, repeated activation/KO/next round, corner behavior, other
stock/boss victim states, move sound and blade-hit blood behavior remain open.
The complete v43 leg-grab suite has not been rerun on this executable; its 144
results remain evidence for the older v43 binary, not this one. All remaining
specials/grabs, voices, finishers, AI, reselect/join/morph paths, and full ladder/
ending progression remain within the unchanged overall goal.
