# Current-link Choke / Leg Grab checks

Stock-MAME physical-input runs327/328 use the entry-grounding-corrected ROM.
The qualifiers now verify actual archive program bytes, all current graphics
sockets, immutable controller hash, absence of guest-memory writes/Lua errors,
and expected physical player side. Current source/map pins are per-run.

Kano Choke against Sonya (run327, side1): eight completed69-field holds,
four8-damage pulses in the first hold (32total), all eight owner poses,
own victim pose/trajectory, zero held velocities, release/recovery, and
block/duck/far rejections. Observation through9000, no missing markers.

Sonya Leg Grab against Kano (run328, side2): seven46-field holds, 35 damage
per release, seven owner/five victim poses, exact paired offsets, six holds
with the full recovery window observed, standing block caught, low-block/
far/incomplete-chord rejection. Observation through9000, no missing markers.

The first Leg qualifier invocation incorrectly supplied side1. Its empty
fight selection was a verifier invocation error, not a gameplay regression.
Correct side2 passed. Explicit side/profile checks now catch that mistake.

These current cases do not cover every victim, boss, stage edge, AI matchup,
interruption or final audio mix. No gameplay source or damage rule changed.

## F650 current-program refresh: runs608/609

Both runs finish normally at9000 fields with no missing markers/Lua faults.
Updated qualifiers verify all26 actual ROM chips, not only program/added
graphics, and pin themselves plus the shared verifier. Five local verifier
integration tests reject in-memory program/sound/original/added-art corruption
and accept the actual current26-chip set. No ROM file is mutated.

Choke608 (Kano P1, own Sonya victim): eight69-field holds,552 held fields;
first hold has four8-damage pulses at4144/4156/4168/4180,32 total. All eight
own body poses and the native paired victim trajectory are observed. Tested
block/duck/far rejections and both actors' first-hold recovery pass.

Leg609 (Sonya P2, own Kano victim): seven46-field holds with35 damage per
release; six have the full recovery observation window. Seven owner/five
victim poses and exact paired offsets pass. Standing block is caught; low
block, far range and incomplete chord are rejected. Block-first and
simultaneous chord fixtures pass. The optional early-LP-first telemetry
flag is false: do not claim that input-order case was accepted.

The71 selected source/tooling/patcher/local-ROM-verifier tests pass. These
finite cases still do not qualify all victims, bosses, edges, interruptions,
AI matchups or the final audio mix. No native game source/ROM changed.

## Opposite-side F650 refresh: runs620/621

Kano P2 Choke620 passes eight69-field holds,552 paired fields,32 first-hold
damage in four8-damage pulses, all eight own body poses/own victim art,
zero held velocities, tested block/duck/far rejection and recovery.
Sonya P1 Leg621 passes seven46-field holds,35 release damage, seven owner/
five victim poses, exact paired offsets, six full recovery windows, standing
block catch and low-block/far/incomplete-chord rejection. The P1 release
damage sample offset is47 (P2 fixture46), as checked explicitly by the
verifier; neither fixture claims early-LP-first acceptance.

Both exit normally at9000 fields, verify all26 current chips, and report no
missing markers/Lua faults. Combined with608/609 this covers both physical
player sides for these defined own-victim fixtures, not all victims, edges,
interruptions, AI or audio. No native source/ROM or emulator changes.
