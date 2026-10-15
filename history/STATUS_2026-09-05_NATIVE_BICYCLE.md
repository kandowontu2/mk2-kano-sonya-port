# Native Sonya bicycle — v46 candidate

Sonya's B,B,D+HK bicycle is implemented as an independent native action. The
exact final candidate passes 78 runtime cases and 37 asset tests. This is a
partial integration milestone, NOT completion of the full Kano/Sonya goal.

Follow-up: `STATUS_2026-09-05_BICYCLE_LIFECYCLE.md` records 90 refreshed runtime
cases, 37 asset tests and one input-driver test on this unchanged candidate.
The driver now releases P2 High Kick correctly. Eight real KO/next-round and
four actual startup interruption/retry cases pass. A separate `PLAY_CANDIDATE.cmd`
has its own verified launch path; the normal installed launcher is unchanged.

## Exact current build

- Executable: `diagnostic_v46_bicycle_asset_candidate/mkport_candidate.exe`
  SHA-256 `FCA7B8174C7D019236835ECFBEB8E8254622CE4405CA8842CAD04782F47FE96A`.
- Required payload: `diagnostic_v46_bicycle_assets/roms/mk2ks/mk2ks.mdata`
  SHA-256 `5CA9EE80B2737F7A295554C22BF3D4068C2552F90C744BA1D125B41251945D55`.
  CRC `a25e6424`, SHA-1 `97cdbaf0dddd4804299f7bc77d9d62b7b55101ee`.
- Gameplay source: `mame-mkp/src/mame/midway/midtunit_m.cpp`
  SHA-256 `BE4624B49C69626A44D0A0B7940DF957DE33033C67AE330D761B927276AC9BE4`.
- ROM registration: `mame-mkp/src/mame/midway/midtunit.cpp`
  SHA-256 `63AD19F6D5DAF3079146240F22595C0C1B61114A02493C217F6362DE9A961CD4`.
- Exact inventory, individual result/log hashes, build-input checks and
  supporting source hashes: candidate `verification.json` and `build-info.json`.
  One-shot audit source: `tools/verify_native_bicycle.ps1`.

The installed CMD remains v42 (`41385589...D13A891`); its ROM audit passes.
Delivered v42 and v44 WIP ZIP hashes are unchanged. This candidate has not
been installed or packaged. Current source requires the corrected v46 payload,
not v45/v44/v42 data. The previous v45 executable and payload are preserved.

## Original reference and implementation

Six original MK3 2.1 real-input captures are in `diagnostic_v46_mk3_bicycle_*`.
They select actual P1 Sonya/P2 Kano and confirm B,B,D+HK reaches special 1.
`tools/audit_bicycle_reference.py` checks their startup displacement/cadence,
22 hit damage, 3 standing-block chip, duck/duck-block misses, and paired
rise/float motion. Its JSON is in `diagnostic_v46_bicycle_assets`.

Original FF9E4DA0..FF9E6340 and the typed FF83E620 script establish:

- Three startup poses, two fields each, +5 facing-relative X/+10 Y per pose.
- A ten-pose looping bicycle phase, four-field cadence and rising collision
  window with the original stage-ground-relative C0h ceiling.
- A hit pairs the actual opponent: three-pixel forward/upward lift, then
  sixteen fields at one pixel forward/half a pixel downward. The lift is
  bounded by 32 fields and the original E0h height limit.
- The opponent stays +48/-32 relative to the attacker, with facing mirrored.
  Custom victims retain their original six-pose stumble loops; stock humans
  use their own MKII stumble composites. Stock contact offsets still need
  a full body-by-body artwork audit, not just coordinate equality.
- Release uses the native 4/-6-pixel fling, A000h gravity and five-field
  falling cadence. Sonya reverses her startup poses and lands independently.
  Standing block and miss use their separate rebound/forward-fall paths.

HK dispatch is bound to Sonya's own history parser. Native actions are 0204h
startup, 0214h paired attacker and 0215h paired victim. There is no held-LK
Liu action call or character-ID substitution. Allocation is F3400..F43FF;
Sonya reaction row 26 is distinct from her leg row 25 and Kano's choke row 26.
Boundary exemption requires the actual Sonya attacker and paired states.

## Defects found and corrected

The first candidate (`143898F0...00DA409`) passed a permissive near-hit test,
but inspecting its actual velocities exposed a three-pixel float. The
stricter observer rejected the next build (`303E5654...FDC1D21`) on all six
near/air/held positive cases. Requesting both player velocities alone did not
fix it: MKII FF8285F0 skips velocity publication entirely while close-body
push suppression is active. The paired action now owns both current actor
velocities and their ordinary player requests at each phase change. Tests
remain read-only; no observer writes force the required motion.

The paired-motion build (`FBC8165F...117E3AC3`) then passed 76 of its 78 cases,
but Sonya mirrors still failed four velocity samples. A new asset test found
the original FF8369C0 composite pointing at corrupt FFB1FE90 rather than
FEB1FF90. The relocator had mistaken a null terminator plus the next frame's
low halfword for a pointer and modified the wrong two bytes. Prioritizing
fields validated against actual frame descriptors also fixes Kano FF825EC0.

The corrected payload changes exactly four bytes at 4BD9, 4BDB, 6D39, 6D3B;
`payload-delta.json` records them. Both Sonya mirrors now pass with no other
gameplay change. The old v45 payload fails the new tests in three checks;
its negative-control log is retained. All validated frame-member fields in
both original fighter blocks are now checked, along with both victim loops.

Earlier failed logs, builds and the read-only velocity trace remain intact.
The initial asset invocation used an incorrect output subdirectory and skipped
three selected-payload tests; it is NOT acceptance evidence. The final selected
payload run executes all 37 tests without skips.

## Verified coverage on FCA7B817 / 5CA9EE80

- 50 bicycle cases: twelve stock human victims on both attacker sides; Kano
  victims and both Sonya mirrors; eleven additional input/target modes on
  both sides. Checks include real activation/rejection, pose presence, paired
  field cadence, contact coordinates, rise/float velocities, release fling
  parameters, exact damage/chip, grounded recovery and native mirror palettes.
- 12 core roster cases: grid, navigation, both custom mirrors, jumps,
  single-player ladder/loss/continue lifecycle, wins and twenty basics each.
- 12 leg-grab regressions: both sides, Kano/Sonya victims, near and both corners.
- 4 choke regressions: both sides against Kano and Sonya.

All 78 processes exit zero. Applicable parent gates check display cleanup,
actual IDs, names, HUD shadows, stalls/traps and object leaks. The asset suite
adds seven bicycle/conversion tests to the preceding thirty. Source/build/
payload/harness hashes and the preserved releases passed the final audit.
Functional screenshots use 400x300. Selected original, custom mirror and stock
victim captures were visually inspected; that is not exhaustive artwork QA.

## Still required for the full objective

The follow-up completes scoped repeated bicycle KO/next-round and startup
interruption testing. Next are corners, projectiles and boss/CPU semantics. Move-specific impact/
voice/screen-shake feedback and original voices/announcements remain unfinished.
Complete stock-body contact fidelity, throws and victim behavior, finishers,
CPU roster participation, full ladder progression/endings, comprehensive
other-special regressions and final installed-CMD/release acceptance remain
open. The user wants natural integration in all aspects, not just this move.
