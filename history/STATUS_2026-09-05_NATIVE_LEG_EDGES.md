# Native paired boundaries and leg-grab lifecycle — separate v43 candidate

Newer working source/build: `STATUS_2026-09-05_NATIVE_BLADE.md`. The v43 evidence
below remains tied to the v43 executable and payload; it is not silently
recounted as full leg-grab coverage of the newer blade candidate.

The full natural-roster goal remains unfinished. The installed CMD and portable
v42 release ZIP are unchanged; none of these candidate changes have been
silently substituted into the release.

## Build

- `diagnostic_v43_edge_candidate/mkport_edges.exe`: SHA-256
  `441275ACEAF434C5917F72781936E212D7C9786A40F1516F5FA5A992276DD7AB`.
- Required payload: `diagnostic_v43_jump_candidate/roms/mk2ks/mk2ks.mdata`,
  `31B89318C7D9C6A15706063A1A953D80E5F426AF6EC980009B5040626CAE206B`.
- This builds on the native mirror-palette/contact candidate documented in
  `STATUS_2026-09-05_MIRROR_PALETTES.md`. Its earlier 88 cases, and the contact
  build's earlier 258 cases, are historical results for different executables.

## Real corner-state defect and game fix

The four `diagnostic_v43_edges_*` tests reproduced incorrect clipping on the
preceding `402DC8FE...` executable. MKII's unconditional VBLANK boundary handler
clamped the paired victim between scripted flip poses. That changed the actual
throw trajectory even though the callback still used correct coordinates.
Original unmodified MK3 corner recordings show that the complete paired path
must be preserved, including outside the ordinary walking bounds.

The actual victim process now enters dedicated action `0111h` while Sonya is in
grab action `0110h`. The native boundary entry `FF8054E0` branches to a trampoline
in checked free program bytes `F1700..F18FF`. It exempts only the current player's
actual process when that process is paired, its enemy actor is Sonya ID 18, and
its enemy process is still actively grabbing. It uses only native scratch
registers A3/A5. Every other case executes the exact displaced MOVE/CMP and
returns to the original boundary code at `FF805510`.

The real process globals are P1 `01060260` and P2 `01060E30`; the nearby
`01060240`/`01060E10` locations are button dispatch tables, not process pointers.
Release immediately changes the victim to native knockdown action `0506h`, so
MKII's normal clipping, outward-velocity cancellation and gravity resume. No
frame hook, proxy identity or permanent sprite flag is involved.

## Boundary observer correction

Early edge-build diagnostic failures are retained. They included two incorrect
observer assumptions: the trailing fighter can oscillate one pixel during
ordinary body pushing at a wall, and a frame sample can precede VBLANK clipping
on the very field where release damage occurs. Neither justifies altering the
authored paired offsets or deleting the bounds check.

The corrected observer proves that the leading body reaches the exact native
edge in both approach samples. It observes the boundary routine itself before
and after clipping (`FF8054E0`/`FF805630`), checks the exact native bounds and
zero outward velocity at the clamp event, and requires clipping to resume on
the release field (or the next observed field). All 46 authored paired fields,
their native poses and IDs, and the exact 35-damage/47-or-48-field release checks
remain enforced. Boundary-test harness hash at this milestone:
`C41EFCFA25E8A82DC22C0E01BA3338C5AD3B0FE7349FF12AAE9E76C66FA22C83`.

All 56 `regression_v43_edges_p1_*` / `regression_v43_edges_p2_*` corner cases
passed: fourteen selectable fighters, both edges, both Sonya player sides.
The six preceding `diagnostic_v43_edge_phase_*` cases also passed. Twelve
`regression_v43_edges_core_*` cases passed on this executable: both mirrors,
whole jumps, ladder/loss lifecycles, native wins, basics, grid and navigation.

Reviewed corner captures: Sonya mirror left edge
`regression_v43_edges_p1_sonya_vs_sonya_corner_left/snap/mk2ks/0037.png`, and
Kitana victim right edge
`regression_v43_edges_p2_kano_vs_kitana_corner_right/snap/mk2ks/0037.png`.
Original MK3 `diagnostic_v43_mk3_leg_corner_left/snap/mk3/0019.png` provides the
corresponding donor pose reference, including Sonya's original outfit colors.

## Repeated grabs, KO, next round, and interruption

`mk2ks_leg_lifecycle_test.lua` uses ordinary selection and controls to perform
five alternating-facing grabs to a real KO, waits for the native next round,
then completes a sixth grab. It checks one activation/catch and one release
damage event per command, exact startup/release scheduling, native ready
continuations, own identities, floor recovery and cleared paired states.
Optional mash mode repeats the attacker's chord during the active grab and
presses the victim's chord while caught. It does not force process state or
health. Actual body palette RAM is compared with original normal/alternate
colors before, during and after grabs, including the next round.

The first `diagnostic_v43_leg_retrigger_side1_kano` completed all six grabs.
The expanded initial round/mash suites found a base-observer defect when P1 is
stock and P2 Sonya: the existing constructor allowance watched only P1's custom
HUD entry. One normal next-round null-object field was consequently reported
as a P2 identity error. All six grabs and palette checks themselves passed in
those runs. The observer must independently watch P2's real HUD event; the
two-field construction limit must not be broadened arbitrarily. This is now
corrected: `last_native_p2_hud_frame` observes P2's actual extended HUD entry
independently for every named P2 fighter. The corrected Kitana case reads P2's
HUD at frame 2689, accepts its normal construction field at 2690, and retains
zero identity errors throughout the subsequent round. The four affected
round/mash cases were rerun under the `_p2hud` prefixes and all passed. No game
identity or constructor code was changed to accommodate this test correction.

`mk2ks_leg_interrupt_test.lua` adds a real opposing uppercut during Sonya's
startup, followed by a fresh grab after native hurt recovery. Initial timing
probes that did not actually interrupt are retained as failed diagnostics,
not counted as interruption coverage. Entering the opponent's crouch before
pressing HP, then pressing HP two fields after Sonya's command, produced an
actual 40-damage interruption and successful 35-damage retry in the P1 Kano
victim diagnostic. P2 requires the counter one field earlier because of native
task ordering. The final runner defaults to delay 2 for P1 Sonya and delay 1
for P2 Sonya, without changing game scheduling. Both victims on both sides
pass the same strict requirement: one entered startup, no initial catch, 40
actual uppercut damage, native recovery, then a single successful 35-damage
retry. These are startup interruption tests, not paired-projectile interruption
tests.

## Final verification on this executable

`diagnostic_v43_edge_candidate/verification.json` records **144 passed runtime
cases**, with exact build/payload hashes and per-case log hashes. The bounded
inventory in `tools/verify_edge_candidate.ps1` validates every expected case
and its relevant result markers rather than counting whatever result files
happen to exist:

- 12 `regression_v43_edges_observed_*` core cases after the P2 observer change:
  both mirrors, both jumps, both ladder/loss lifecycles, both native wins, both
  20-action basics, the 31-check selection grid and 10-check navigation route.
- 56 `regression_v43_edges_p1_*` / `_p2_*` complete-roster corner cases.
- 20 cannonball, 20 square-wave and 16 knife/ring command cases under
  `regression_v43_edges_{ball,square,commands}_*`, including their existing
  rejected-input, blocking, miss and follow-up checks.
- 16 repeated-grab round cases: both grabber sides against Kano, Sonya, Kitana
  and Sub-Zero, normally and with in-grab button mashing. The four corrected
  mixed P2 cases use `_p2hud`; the original four red results are retained and
  excluded. Each case completes six grabs (96 total), including a real KO and
  one successful grab after the next native round starts.
- Four `regression_v43_edges_leg_interrupt_*` actual startup interruption and
  retry cases, against Kano and Sonya on both player sides.

All 14 asset tests passed again; their output is preserved in
`diagnostic_v43_edge_candidate/asset-tests.log`. `git diff --check` passed.
All test sessions are terminal and no candidate emulator process remained.

Final base observer SHA-256:
`EE3896F4488C4AB04724136CF918DC8C3647C353B33ADCA7F87F50DABDE99991`.
Lifecycle harness SHA-256:
`50C9F9A145934ED6589FA1D1E4E1F7F913D327B0DD25B9BE1C37401B356D29E3`.
The manifest retains earlier per-run harness hashes; the corner/special suite
was not silently relabeled as having run a later observer. Earlier edge-core
and timing diagnostics are additional historical evidence, not added to 144.

The post-next-round Sonya mirror capture
`regression_v43_edges_leg_rounds_side2_sonya/snap/mk2ks/0034.png` was reviewed:
both own names/shadows remain visible, one fighter uses the original alternate
outfit, both are grounded, and the native round-win icon is present. The
lifecycle observer performs 44 custom-body palette checks per Kano/Sonya
case (including eight after the next round) or 22/4 when the victim is stock.

The installed v42 executable (`41385589...D13A891`), its selected
`roms_v22_clean` payload (`2F29937E...EED31FF`) and the portable ZIP
(`1568AB02...91A8`) were rehashed and remain unchanged. The older fallback
`roms/mk2ks/mk2ks.mdata` is not the installed CMD's selected payload.

## Remaining work

The current-build regression inventory is complete for the cases above, not
for every natural-roster requirement. Startup interruption is not proof of
interruption by an already-live projectile during paired motion. Boss rejection,
late-round/finish-state grabs, further reselect/join/morph paths and complete
move/victim semantics still require work. Remaining moves/grabs, native voices
and sounds, finishers, AI, and all ladder/ending routes remain within the full
goal. A passing leg-grab milestone does not complete that goal.
