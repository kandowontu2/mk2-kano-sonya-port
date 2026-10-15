# Current Friendship audio and Babality regression — not release acceptance

Candidate: diagnostic_v786_native_fighter_fade_exclusions.
EXE SHA256: 8DD83D7300BBC3872B1F829EA2A557CA968F5148464C3518AAB16B8559A76B55.
Payload SHA256: 7896C93822473376AD724BB5E747EDE88C198203786F3F9B928CD1D860BAE019.

The previous goal turn made verified progress: the native fighter fade-list
integration passed actual palette, original body-pixel and stock-control
checks. This turn adds current-candidate audio and Babality regression proof.
No gameplay code, executable, payload or sample assets changed in this turn.
No material data was deleted. The existing v737 latest-test launcher and
production launcher/release ZIP remain unchanged; no release is promoted.

## Current Friendship audio revalidated

Twelve new cold, genuine-control cases on v786 cover four audible positives,
four samples-disabled positive baselines and four negative controls. Each
winner earns two original-combat KOs / 322 damage. No guest RAM writes,
health assistance, cheats, state fixtures or borrowed character identities.
The readonly observer logs native cue times, actor/task IDs, hold timers and
existing winner announcements; the physical input harness is unchanged v784.

The complete gameplay, scene and native sound-dispatch traces are identical
between each audible positive and its samples-disabled baseline. Baseline
subtraction therefore isolates the actual new samples plus existing voices,
without treating announcement overlap as noise or relaxing waveform limits.

audit_v791_native_friendship_audio_checked checks 2,496 inputs and eight
audible/rejected cases against the original DCS source oracle. All 80 cues
pass: two Kano bubble pops and 78 Sonya clucks. All four cluck variants and
native allocated voice indexes 0/1/2 are exercised; 28 audible overlap groups retain
their original waveform, complete tails, source loudness and cue timings.
Worst correlation: 0.9999918110182154. Worst residual RMS: 0.892628653 PCM
units. Actual output-rounding shifts are at most two PCM samples (the unchanged
strict gate permits at most four). Wrong commands and punch-used negatives
dispatch no Friendship cue. Native owner/identity, original choreography,
first-free independent voice holds and cleanup remain checked.

The implementation retains the original five-voice pool, and the donor oracle
checks all 20 hardware commands across all five voices. These genuine port
Friendship cues naturally require at most three simultaneous voices. They do
not exercise allocation indexes 3/4; donor command coverage must not be stated
as five-voice runtime allocation coverage.

The new verifier preserves the old v779 waveform/gain/overlap thresholds and
adds exact native fade-list validation. Actual guest changes relative to v768
are precisely the existing audio changes plus the verified fade extension:
978 changed bytes total, not a new audio implementation. The immutable v789
proof independently guards the complete current guest against the old guest.

audit_v792_native_friendship_audio_units passes 22 baseline/corruption methods,
covering wrong waveforms/volume, silence, lost tails, missing/mis-timed cues,
voice restart, wrong actor/task, timers, marker collision, missing native RNG,
and unrelated guest edits. Old v777/v779/v781 captures and proofs are unchanged.

## Current Babality regression revalidated

Ten fresh cold cases on the SAME v786 executable/payload cover Kano and Sonya
as the human performer and reciprocal victim, each in both slots/facings;
wrong-direction rejection for each; winning-round punch-use rejection for
each; and stock Kitana-on-Liu controls in both slots. All earn two original
combat KOs / 322 damage without health, identity, position or action writes.

audit_v794_current_babality_regression_checked checks 2,926 inputs. The exact
original baby artwork and palettes, native actor/Main ownership handoff,
victim IDs, physical character commands, floor placement, halfword pointer
retirement, object reuse and next-screen transition pass. Twelve rendered
baby samples match all 10,536 nontransparent original source pixels. All 182
stock frames are byte-identical to the previous verified Babality captures.
Both actual current Babality code/records and LK bindings remain byte-identical
to the previously accepted own-performer implementation.

audit_v795_current_babality_runtime_units passes seven test methods with
multiple subcases: all ten current runtime baselines; 17 positive corruption
subcases; four missing-native-action/retirement/reuse/input subcases; reboot;
exact original pixels and one-pixel corruption; and negative-action/proxy
subcases. This is current runtime/pixel testing, not a claim to rerun the
old static-command mutation matrix against a different whole guest.

## Frozen checkpoint and remaining goal

audit_v796_current_audio_babality_checkpoint rechecks all 2,934 pinned inputs
and freezes the current visual, audio, Babality and unit proofs together.
It also verifies the candidate build-input hashes, executable/payload hashes,
unchanged v737 test CMD and restored installed EXE. Full finisher acceptance
and full port acceptance remain false.

Next: current-candidate fatalities and stage finishers, then broader move,
selection/ladder cleanup/name/floor-shadow and interruption regressions.
Broader finisher input/distance/arena/CPU coverage and alternate/frozen runtime
remain beyond these human tests. Complete unassisted towers through both
bosses, continues/reselection/endings, secret-stage paths, whole-port final
regression and matching production launcher/release ZIP still remain.
