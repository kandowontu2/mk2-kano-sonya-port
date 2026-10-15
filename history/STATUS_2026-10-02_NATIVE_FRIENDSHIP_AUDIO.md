# Native Friendship audio checkpoint — not release acceptance

Experimental candidate: diagnostic_v777_native_friendship_audio.
EXE SHA256: CB70C659300DFEE6E964B22D93653A72917FE1B6C7ACF9044354B8486B55E584.
Payload SHA256: 7896C93822473376AD724BB5E747EDE88C198203786F3F9B928CD1D860BAE019.
Driver SHA256: CEEC7CF14BEC67C75CED1CAF53070CE06FE1D99F16FA025D7BE40E53945B9D1E.
Map/config SHA256: 07C1FA27AAA0B1C836E462BC6EC13D62DFF405FA2B7F1358D7BB34B51731DA85.
PLAY_LATEST_TEST_BUILD.cmd remains v737; production CMD and release ZIP are
unchanged. Installed EXE was restored to its previous verified hash. No files
were deleted during this work.

## Implemented

Kano's original bubble pop and all four original Sonya chicken variants are
integrated into their owned native MKII Friendship actions. Original MK3
tables are 006E1F21 (both pop entries) and 00A51010/00AA1017/00AF1014/00961012
(four cluck variants). The low-byte fields 16/23/20/18 are native voice hold
timers; the selected base command is offset by one of five hardware voices.
All twenty cluck command captures are PCM-identical within each variant.

Five actor-owned hold timers and the native MKII 1..4 random-range routine
select the original variants and first-free overlapping voice. Native token-6
callbacks advance the timers by three elapsed pose fields and trigger sounds
only at the original three poses, preserving the existing animation/handoff.
Sampling those timers at cue times has the same first-free decisions as
per-field decrementing; it is not a transplanted MK3 global sound scheduler.
The five added sample channels remain separate from announcements/fatalities.
Kano has a separate pop channel. No host RNG, proxy actor or single-channel
cluck retrigger is used.

Pop dispatch occurs at native action age 183, immediately before bubble group
FE9D2750, corresponding to original age 185. Sonya dispatches at ages
89/95/101 and then every 42 fields, immediately before chicken poses 2/4/6.
Original Sonya's actual pose/dispatch ages are 90/96/102; its initial actual
body pose is age 49 versus this port's age 48. Do not confuse native pose
state with the later visible framebuffer or subtract Kano's two-field
setup difference from Sonya's cue timing.

Original DCS output is isolated using time-aligned cold baselines. The new
48-kHz mono WAVs retain complete native delivery-to-PCM latency and tails.
Only the port's existing 0.70 routing gain is compensated; no added fades,
boosts, resampling or substitute stock effects are used.

The first v775 trial revealed that FFxx markers can alias ordinary native
sign-extended DCS byte writes and play clucks during combat. It is retained
as failed evidence, never accepted/promoted. v777 uses distinct full-word
6AA0..6AB3 cluck markers and 6AB4 pop. All wrong-command/punch-ineligible
cases are silent for the added cues; positives have no cues outside their
Friendship actions.

## Verified scope

- Original captures: v770/v773 scene/actual sound-table/DCS-byte traces and
  v771/v772 isolated playback. These donor captures are assisted references,
  explicitly not unassisted port gameplay.
- audit_v774_original_friendship_audio_checked: five exact extracted assets,
  103 input hashes, twenty hardware cluck commands checked for channel identity.
- audit_v778_native_friendship_dispatch_checked: eight cold genuine-human
  physical-input cases on v777, no cheats/guest RAM writes/health assistance.
  Two earned KOs / 322 damage each; own real IDs, ground anchor, body order,
  bubble palette/foreground pixels, rejection gates and cleanup still pass.
  220 checked inputs; 22 baseline/corruption test methods pass.
- Four v777 samples-disabled cold gameplay runs provide native DCS baselines.
  Four v780 read-only extra-announcement trace runs use the SAME v777 candidate
  and produce byte-identical WAVs to their v777 audible runs. The extra traces
  account for the existing winner voice overlapping later chicken cycles.
- audit_v779_native_friendship_audio_checked: 327 checked inputs, eight
  bounded runtime cases and 80 audible cues: two pops + 78 clucks. All five
  source voices are exercised. Twenty-eight audible overlap groups fit the
  original source samples at their native trace times and routing gain.
  Worst waveform correlation is 0.999991811; worst residual RMS is 0.892 PCM
  units. Only <=4 output-sample fractional rounding is allowed, not field-scale
  timing searches. Existing announcement interpolation is modeled from the
  unchanged samples.cpp implementation, including repeated-double rounding.
- audit_v781_native_friendship_audio_units: 22 further baseline/corruption
  methods, including silence, wrong volume/waveform, missing tails, bad cue
  timing, shared-channel restart, wrong actor/task, pool holds, marker alias,
  missing native RNG and unrelated guest edits.

The v779 verifier preserves strict waveform/gain/overlap gates; existing
winner announcements are modeled, not dismissed as noise. Actual guest-ROM
changes versus v768 are confined to the two owned Friendship actions and
the reserved audio streams/callback area. Prior gameplay tables remain intact.

## Still required before promotion / whole-goal completion

Full body display/palette/cinematic verification under native MKII finisher
dimming, stock Friendship controls, broader input/distance/arena/CPU coverage,
and current-candidate Babality/fatality/stage-special regression remain.
Selection, floor shadows, combat, endings and all historical work are not
wholesale recertified by these targeted audio cases. Full unassisted towers
and both-boss clears, whole-port regression, final production CMD and matching
release ZIP also remain. Full port / full finisher acceptance are false.

Pre-edit preservation: audit_v773_pre_friendship_audio_inputs contains all
v768 build inputs, samples, build-info and latest CMD, with snapshot hashes.
audit_v776_pre_marker_collision_fix preserves the failed v775 driver/config
and build-info. Use snapshots to resolve historical source hashes; do not
overwrite frozen proofs or pretend historical builds used today's live sources.
