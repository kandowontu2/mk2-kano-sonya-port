# Native blade feedback and command coverage — v44 follow-up candidate

The full natural-roster goal remains unfinished. This candidate adds native
blade swish/cut sounds, victim hurt feedback and hit blood without changing
Kano's identity, move animation, collision, damage or authored recovery.
Final current-build verification completed: all 102 exact runtime cases and
20 asset tests passed. `diagnostic_v44_feedback_candidate/verification.json`
records the checked hashes and results; installed build and both releases are unchanged.

## Exact artifacts and preserved releases

- New executable: `diagnostic_v44_feedback_candidate/mkport_feedback.exe`,
  SHA-256 `B1DA05A999230413182123E87DF905D252B9BB7C7F0A4B6B09A8FEAEC13043FF`.
- Required payload is unchanged:
  `diagnostic_v44_blade_candidate/roms/mk2ks/mk2ks.mdata`,
  `91001C2E6551CB850F919971D67806DE31D5F34D97C6CE0D9764B4F367F19DB3`.
- Current `mame-mkp/src/mame/midway/midtunit_m.cpp`:
  `7D3DA1619783A5C4126913A7C91487237A7AD2B9E28C069F359854B752567A69`.
- Blood-only intermediate executable's historical path is
  `diagnostic_v44_blood_candidate/mkport_blood.exe`,
  `239C56FF2EB7CE8DA2BE7DB1D864E88F12C6F3C4887DDF883338F6A731A0339B`.
  This superseded build may be in the workspace cleanup archive; its archive
  manifest records the original path and checksum for restoration.

The installed CMD still uses v42 `41385589...D13A891` with its original
`roms_v22_clean` payload. The original v44 blade executable `A3479747...401AF0`
is preserved. The user-requested v44 WIP ZIP contains that earlier blade
executable, not this new feedback candidate. Its SHA-256 remains
`C72E5B40A01CC566167D41FD221B4170D0417A496C132B1B4E044B099EAB5C7F`.
The older v42 ZIP remains `1568AB02...B91A8`. Neither release was rebuilt or
silently promoted. The build process restored the installed executable from
its hash-checked v42 recovery copy in a `finally` block.

## Native implementation and source evidence

Only the existing blade action/hurt emitters changed. Allocations, descriptor
addresses, body/trail data and the 38-field action sequence are unchanged.
There are no new CPU hooks, frame hooks, identity substitutions, persistent
flags, injected game inputs or host-rendered effects.

Original MK3 blade reaction `FFA4A5A0` requests blood type 1 before victim
setup. MKII type 1 at `FF9A7F70`, dispatched by `FF9A5B00`, uses the same
generator parameters and two splashes/six particles as MK3 `FFA68290`:
`20000,10000,50000,30000,00010001,40000`, repeated three times. The original
native dispatcher checks blood-disable state `01061A60`; this patch calls
that dispatcher, not a bypass into the effect generator. Operator-menu
blood-disable runtime coverage remains open.

The actual victim's own `FFF90000` blade-hurt reaction now requests that
recipe once. Standard MKII blood allocation, palette upload, facing/origin,
display insertion, physics and cleanup own the effects. No blood is requested
on the miss/block path. Native palette `FFAF2A40` contains fifteen entries
including transparent zero; all fourteen opaque entries are checked on all
eight allocated blood objects. Cleanup uses the original `FF9B0E50` path.

MKII's two native weapon-swipe actions `FF8734B0` / `FF873750` explicitly
separate an ordinary attack grunt from sound command `C8`. This is the shared
unvoiced weapon-swish effect, now called once at Kano's own blade entry.
Native cut reaction `FF8DC460` separately calls command `44` before victim
setup and selects a hurt grunt afterward. Kano now uses those native cut
feedback primitives without using the stock weapon action/reaction itself.
His original 26 damage, bounds, timing and six-/four-pixel recoil remain his own.

The airborne fallback changes from `FF8D4BC0` to `FF8D4C10`, exactly as the
stock cut reaction does: skip the extra generic `19` blunt-impact sound,
then perform native airborne grunt/fling/recovery. Grounded victims use
`FFA11FD0`; airborne victims use `FFA11EE0`. Actual victim IDs remain intact,
including the already-extended Sonya female-grunt branch. This implements
MKII-style shared weapon/victim feedback, not new character-specific donor
voice samples or full audio acceptance for every move.

## Runtime observers and retained diagnostics

`mk2ks_blade_feedback_test.lua` extends the real-input blade test. It checks
one native recipe on hit, zero on block/miss, actual victim ownership, eight
separate stock-frame allocations, eight real display insertions, 112 native
palette color comparisons and eight native cleanups. All original 38-field
body/trail/palette and ten-origin assertions remain enabled.

It also checks one entry-field swish, one contact-field cut and one initial
victim grunt on a hit. Sound requests are followed through `FFA13BA0` into
both actual high/low command-byte writes to DCS at `01D01030`; acceptance is
not just observing the high-level sound routine. The original sound record
and one of its three native channels must match. Later airborne landing
sounds remain native and are not miscounted as duplicate contact grunts.

`mk2ks_blade_command_test.lua` uses ordinary selection and real controls on
both sides. Valid and held-button commands must produce exactly one blade,
one effect and one 26-damage hit, then recover. Reversed directions, expired
history, wrong button, actual airborne state and held Block must produce no
blade action/strike/trail/blood. The Block precondition checks the actual
pressed input bit and native standing/crouching block action `0301/0302`.
No emulated state is written by either observer.

Retained development evidence is not included in final acceptance:

- `diagnostic_v44_feedback_baseline_side1_sonya_near`: old v44 passes its
  movement test but has zero blade-hit blood requests and zero sound requests.
- `diagnostic_v44_blood_first_*`: blood works, but the first observer wrongly
  reads color 15 beyond the fifteen-entry stock palette (zero is included).
  The observer now uses the palette's actual count; no palette was changed.
- `regression_v44_blood_*`: eighteen feedback and twelve core cases passed
  on the blood-only intermediate, not the final audio candidate.
- `diagnostic_v44_blade_inputs_*`: initial command observer used `IN1` for
  Low Punch instead of MKII's `IN2`, failing initialization. Some negative
  result lines were spuriously green without installed taps. That batch was
  stopped, retained and excluded. The fixed observer requires all five taps,
  and both the runner and verifier explicitly reject every `[LUA ERROR]`.
- `diagnostic_v44_blade_inputs_fixed_*` / `diagnostic_v44_blade_block_state_*`:
  corrected inputs, but the Block precondition originally omitted actual
  native crouching-block action `0302`. A read-only trace established the
  state and held raw input. The game was not changed to satisfy this check.
- `diagnostic_v44_feedback_audio_*`: three initial final-audio build cases
  pass near/block/air feedback, including actual DCS command transmission.

## Final verification inventory

`tools/verify_blade_feedback.ps1` uses an exact 102-case inventory, validates
the selected executable/payload and error-free terminal logs, then runs the
twenty asset tests and writes `diagnostic_v44_feedback_candidate/verification.json`.
It refuses to overwrite existing final evidence.

Inventory: 18 `regression_v44_feedback_{sonya,mirror}_*` full feedback cases,
two actual uppercut interruption/retry cases, fourteen blade-specific input
cases, sixteen existing knife/ring command cases, twenty cannonball cases,
twenty square-wave cases, and twelve native roster/core cases. The inventory
excludes all diagnostic and intermediate-executable results above.

## Remaining full-goal work

Repeated blade use through KO/next round, corners, more stock/boss victims,
operator blood-disable coverage and other interruption/victim semantics need
further work. The full v43 leg-grab suite is still not rerun on this candidate.
Remaining moves, character-specific voices, finishers, AI, reselect/join/morph
paths and all ladder/ending progression are not accepted. Neither this
feedback milestone nor the portable snapshot completes the user's goal.
