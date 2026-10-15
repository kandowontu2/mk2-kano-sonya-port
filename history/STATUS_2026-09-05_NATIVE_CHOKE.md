# Native Kano choke — v45 candidate

The native D,F+LP choke is implemented and has a verified 100-case runtime /
30-test asset milestone. The full Kano/Sonya integration goal is NOT complete.

## Exact current build

- Executable: `diagnostic_v45_choke_release_candidate/mkport_candidate.exe`
  SHA-256 `FD8A14306C20F61920BB02AEEC715496D7F3188E27BC3F030F027473BA3DB546`.
- Required payload: `diagnostic_v45_choke_assets/roms/mk2ks/mk2ks.mdata`
  SHA-256 `C6A77F803191830D471F0127D540AF27039C259ABAC9A9235804B83DFE1A3ED9`.
- Gameplay source: `mame-mkp/src/mame/midway/midtunit_m.cpp`
  SHA-256 `CCC7A82098A016FBE9AE2BD3C03C0CC224C37261C616364C9E4A920EAC542C38`.
- Exact inventory, individual harness/log hashes and current build-input
  checks: `diagnostic_v45_choke_release_candidate/verification.json`.
  Reproducible audit source: `tools/verify_native_choke.ps1`.

Installed CMD is still v42 (`41385589...D13A891`). Both delivered release ZIPs
are unchanged and were fingerprinted again. Do not rebuild current source
against a v42/v43/v44 payload: the new ROM registration and typed-data guard
require the corrected v45 data. This candidate has not been packaged/promoted.

## Implementation

The move uses a native LP history parser and action gate, own action 0111h,
zero-damage catch, three-pose lift, four four-pose squeeze cycles, four separate
8-point damage pulses, and a native fling from the actual lifted position.
There is no Liu attack invocation or character-ID substitution. Miss/block
recovery and the bounded six-field contact window follow the original move.
Blocking, ducking and airborne targets are not caught in the tested scenarios.

Original MK3 2.1 D,F+LP input captures and FFA2F030 disassembly establish the
3/5/3-field animation phases and 32-point total damage. Reference directories
are `diagnostic_v45_mk3_choke_*`; the initial `sonya_near` directory used only
40 approach fields and is actually a miss. `sonya_close` is the actual catch.
Both Kano mirror sides were independently captured too.

The builder had misidentified fourteen negative packed X/Y operands as
overlapping pointers. The corrected payload changes exactly fourteen bytes,
preserves both main-56 victim phase terminators, and properly relocates only
the frame pointers. The old v44 payload fails all fourteen coordinate checks.
`diagnostic_v45_choke_assets/payload-delta.json` and the negative-control log
preserve this evidence. The loader rejects the corrupt old records.

Custom victims retain their own original seven paired records. Stock human
victims use their own MKII high-hit composite with authored upper-chest grip
pivots; the pivots are checked against actual ROM pixels and the original
contact path in both directions. They are adaptation data, not claimed
original MKII choke offsets. Visual audits are in
`diagnostic_v45_choke_pose_audit`. The boundary exemption requires the actual
Kano grabber and its paired victim action 0112h; ordinary boundaries resume on
release. Sonya's existing leg-grab state is still independently recognized.

Program allocation: bytes F2200..F33FF, guarded as unused before emission.
Kano reaction row 26 belongs to this catch. Existing blade row 25 and Sonya's
leg row 25 remain separate.

## Runtime defects and observer corrections

The first ROM-registration attempt (`4D1D2D61...F4640`) failed its checksum
audit before gameplay; its data registration was corrected in the subsequent
candidate. The first runtime candidate (`929EFCC3...384948`) pre-stepped the
falling animation. That skipped its first timed fall pose and hid the last
held pose for one player side. The final executable removes that pre-step:
the native fling itself advances the animation after one field, as in MK3.

The test initially assumed requested horizontal velocity was immediately
present in actor+40. Native FF831AC0 actually writes the player's velocity
request, and FF828590/FF8285B0 later publish the actor velocities. Close stock
bodies can first undergo the native three-pixel separation phase at FF828620;
Shang's lean places his origin close enough to need this transition. The
current observer checks the actual signed request, original fling parameters,
preserved final held pose and subsequent actor motion. Shang's two reruns
allow the bounded eight-field separation window; other final cases passed
the stricter four-field check. Native edge cancellation is accepted only
when its actual boundary instruction was observed. No game-state writes or
forced velocities were introduced to make these checks pass.

Earlier failed logs remain intact, including the inaccurate edge-cancellation
hypothesis. `diagnostic_v45_choke_velocity_kitana` identifies the real writers.
The verifier explicitly selects the corrected evidence, not every directory
that happens to contain a green marker.

## Verified coverage

The exact final inventory is 100 terminal cases on the same executable/payload:

- 50 choke cases: all twelve stock humans on both sides, both custom mirrors,
  and twelve Sonya-target/input modes per attacker side. Tests inspect the
  actual 22 paired steps, coordinates, timings, four damage pulses, native
  launch request, recovery, original/alternate palettes and rejected commands.
- 8 choke lifecycle cases: seven inputs each, six to KO and the seventh after
  the actual native next round. Both sides against Kano/Sonya/Kitana/Sub-Zero;
  native win/HUD reconstruction, clipped lethal damage and palettes pass.
- 12 Sonya leg cases: both sides, Kano/Sonya victims, near and both corners.
- 4 blade lifecycle cases: both sides and both custom victims, eight attacks
  each through KO and the next round.
- 12 roster cases: grid, navigation, mirrors, jumps, single-player ladder /
  loss / continue lifecycle, wins and twenty basics per added fighter.
- 14 existing-special smoke cases: native/wrong-button/blocked-input knife
  and ring, cannonball hit/minimum charge, square-wave ground/air.

The existing-special smoke cases are not the complete earlier 56-case suite.
The normal parent gates include native display-art checks, HUD name shadows,
actual IDs, names, object cleanup, stalls/traps and process exit status.
Thirty asset tests pass with the actual candidate payload; none are skipped.
Functional captures now use 400x300 where supported to limit workspace growth.

## Still required for the full objective

Choke-specific audio, full corner/interruption/projectile interaction/boss/CPU
semantics, Sonya bicycle and other remaining native specials, original voices
and announcements, complete throws/animation/victim behavior, finishers,
CPU roster participation, full ladder progression/endings and final
integration/launch acceptance remain open. This milestone does not prove
those requirements or make the current candidate a finished release.
