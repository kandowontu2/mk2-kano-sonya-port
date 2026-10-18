# Chicken reference-model check

## Prefix-only shared-filter experiment

The optional joint --shared-filter experiment fits one shared nine-tap FIR
on the159744 existing training-prefix samples, without refitting cue phases/
latencies/gains or reading validation targets. A synthetic known-filter test
and a validation-target corruption test verify the fitting boundary. The
feature matrix is11501568 bytes; input remains bounded to15 seconds, never
full-match float arrays. Computation ran hidden/BelowNormal with one BLAS
thread; no emulator/compiler or native assets were changed.

On current6AE0 matched recordings, held-out214781-sample correlation rises
0.99193084 ->0.99298362, relative residual0.16844627 ->0.16036525. Training
correlation0.98579242. The prefix system has rank9/condition437.88. This is
only a small improvement, not an explanation of the remaining residual or
proof of MAME's actual output filter. The separately named shared-filter
report keeps all full-tail/whole-mix/release acceptance flags false. The
unfiltered baseline report is refreshed separately with original metrics.
Next isolate nonoverlapping native cluck playback rather than assume a
larger fitted model establishes individual voice correctness.

## Current6AE0 paired refresh

inspect_chicken_convergence.py now verifies a fixed current-build post-cue
window, with recording hashes tied to the matched-event receipt. Starting
at sample5731950 (one second after the last command), all240000 samples
over five seconds are exactly equal: maximum/RMS difference0. Native RMS
278.879575 confirms a non-silent shared background. Only that bounded
window becomes floating-point data; no full-match float arrays. This
supports finite post-cue convergence on current6AE0, not correctness of
each overlapping early tail or whole-scene audio acceptance.

stock_wolf_6ae0_audio_native and stock_wolf_6ae0_audio_control both complete
normally at9000 fields. The event checker verifies current program/graphics/
sound bytes, exact stock MAME SHA256, frozen matching controllers and actual
recording/trace hashes. The matched-control bank requalifies:455 compressed
inputs unchanged,12 playlist volumes muted,13 changed U2 bytes, U3/4/5
identical. Neither recording uses host samples or a custom driver.

All39 native/control cluck events match age/variant/track. Current full-dance
boundary-reference prefixes match33/39; only3 full references meet the
existing tail criterion. Joint disjoint validation has214781 samples,
correlation0.991930841342522 and relative residual0.168446274621740. These
reproduce the earlier diagnostic limitation on current6AE0 rather than
resolve it. No threshold was weakened and neither individual tails nor
whole-scene mix are certified. Reports in generated_dcs now identify these
explicit current runs. Recordings ran sequentially, hidden/BelowNormal;
no emulator/compiler remains live. Program/package unchanged.

Current stock-MAME runs 533 (SoundP) and 534 (SoundW control) reproduce the
earlier overlapping Friendship audio result. Seven action-phase prefixes match;
only three of the first six full references exceed the existing 0.98 threshold.
The seventh tail and whole scene remain unverified.

An experimental reference model now averages a piecewise-constant 31,250 Hz
decoded source over 48,000 Hz output intervals. It searches 64 source phases,
using only each 4,096-sample prefix to choose phase, latency and gain. This is
motivated by the boundary-blending resampler in the locally available MAME
sound.cpp, not a claim that the complete stock output path is reproduced.

Result: still three of six full references pass. Scores are approximately
0.97574, 0.98157, 0.98767, 0.97053, 0.97563 and 0.98625. Resampling alone
does not explain the residual. No ROM, audio bank, threshold, or release status
was changed. Sequential subtraction also couples overlapping reference errors;
these scores do not independently prove the overlapping mix is correct.

Reproduce with `inspect_chicken_waveform.py --boundary-reference`.
The original SciPy-reference diagnostic remains the default and writes its
original report. The experiment writes `DCS_CHICKEN_BOUNDARY_DIAGNOSTIC.json`
separately. Each input WAV is read in a bounded three-second window; this check
does not load whole-match floating-point arrays or launch an emulator/compiler.

## Control and joint-overlap follow-up

`inspect_chicken_control_residual.py` compares six consecutive half-second
windows before the first cue: all 144,000 samples are identical between runs
533 and 534. It hashes both WAV files and writes
`DCS_CHICKEN_CONTROL_RESIDUAL.json`. This rules out pre-existing recording
drift in that interval, not background changes caused by later voice allocation.

`inspect_chicken_joint_mix.py` freezes the earlier prefix-selected phases and
latencies, then fits all seven gains simultaneously on the union of their
prefix windows. Validation excludes that entire union and ends before the
eighth command. It uses a bounded seven-column matrix (under three seconds),
not whole-match arrays. There are 28,605 training and 20,497 validation samples;
the matrix has full rank seven. Held-out correlation is 0.99413, but relative
residual norm remains 0.14399. Output is
`DCS_CHICKEN_JOINT_MIX_DIAGNOSTIC.json`.

This supports overlap/subtraction error as part of the weaker individual-tail
scores. It does not prove each voice independently, the seventh full tail,
the complete result-screen dance, or final mix acceptance. Original failed
individual-tail results remain intact, and all release flags remain false.

Next: account for remaining mix residual and extend disjoint validation to the
complete dance, without fitting validation tails into their own acceptance data.

## Full recorded dance and control limitation

The `--full-dance` option now evaluates all 39 recorded commands, through one
second after the last command. The prefix model matches 23/39 above 0.98.
Joint sparse fitting uses 712,898 matrix entries rather than a dense full-match
matrix. Held-out full-window correlation is only 0.29657; this is not a pass.

However, the sound-write log contains command 2019 at 111.323484960 seconds,
mapped by DCS_ANNOUNCER_INPUTS.json to Sonya's custom win announcement. That
sample exists in SoundP but not the SoundW control. The full window therefore
contains another deliberately different sound not included in the chicken-only
model. Both full-dance diagnostics are retained; the joint report explicitly
lists the unmodelled announcement and rejects control equivalence. Its residual
cannot establish a cluck playback defect. The earlier seven-cue window ends
before this command and is not affected by this particular confound.

Next: use an announcer-matched control bank or explicitly model and validate
the announcement separately. Do not alter native cluck scheduling or audio
content based on the confounded full-window score.

## Explicit announcer model experiment

Both scripts now offer `--model-announcer` together with `--full-dance`
(the waveform script also requires `--boundary-reference`). This includes the
logged command 2019 and its native decoded KSSW reference, using the existing
announcer diagnostic's 8,192-sample prefix length rather than the cluck's 4,096.
It writes separate ANNOUNCER_BOUNDARY and ANNOUNCER_JOINT reports.

Result: the full held-out correlation improves only to 0.36904, still a failure;
relative residual norm is 0.93173. Thus the custom announcement alone is not
an adequate explanation of the complete residual. Known announcement coverage
is recorded separately from control equivalence, which remains unproven.
This experiment does not certify the announcement or any individual cluck tail.
Use a genuinely matched sound-bank control next; do not keep adding free model
parameters merely to obtain a passing correlation.

## Matched-bank control build and stock playback

`prepare_chicken_muted_control.py` stages a separate diagnostic bank under
baseline/chicken_muted_control. It copies all 455 compressed clips unchanged,
including announcers, and changes only the twelve chicken playlist setvol
operands from 100 to 0. Play operations, durations and routing remain intact.
The old builder needs MK2.EVD and MK2.LOC in addition to its other inputs;
initial missing-input attempts failed before producing ROMs. These staging
requirements are now included in the generator. No current playable files were
modified. `build_chicken_muted_control.ps1` successfully completed in 13.23s,
with hidden dummy video/audio and below-normal priority; no window was created.

`qualify_chicken_muted_control.py` verifies exact playlist transformation and
input equality. The resulting bank differs only in U2 (13 bytes); U3/U4/U5 are
byte-identical to current SoundP. This is a diagnostic bank, not a release.
The term "muted" is a filename convention, not a claim that operand zero gives
mathematical digital silence: native DCS volume behavior remains in scope.

Stock-MAME run 535 completed normally with that bank and the unchanged native
program/controller. `inspect_chicken_events.py stock_wolf_game533
stock_wolf_game535 --muted-control` verifies the same 39 cue events, controller,
current program/graphics and exact diagnostic sound bytes. Matched reports are
separate from the historical SoundW comparisons.

Both waveform and joint scripts accept `--matched-control`. Full-dance joint
validation now has 214,781 held-out samples, correlation 0.99193084 and relative
residual norm 0.16844627. Training correlation is 0.98544865. The sparse matrix
has 712,902 entries and converges in 14 iterations. Sequential prefix matching
improves to 33/39. This strongly improves the comparison, but does not certify
individual full tails, exact mix or clean scene exit. All release and complete
scene flags stay false. Do not carry conclusions from the mismatched SoundW
full-window residual into native audio changes.

## Frozen per-cue held-out tail diagnostics

The matched full-dance joint report now includes39 per-cue tail timelines.
Phase, latency and gains are unchanged; every sample used by any prefix fit
is excluded. Each cue's complete resampled reference fits inside the actual
observation window (now checked from sample bounds, not inferred from a CLI
flag). Metrics distinguish overlapping from nonoverlapping support. Zero
norms produce null metrics, not invalid JSON NaN or a false perfect score.

All39 cues have held-out joint-tail samples (3931..15441 per cue). Their
joint-model correlations range0.9514..0.9949. Overall held-out correlation
remains0.99193084 and relative residual0.16844627. Several tails overlap
completely with another reference, so these are joint timeline diagnostics,
not isolated-voice proof. No fit parameters or audio/game assets changed.
Individual-voice, full-scene and release acceptance flags remain false.

## Finite historical post-cue convergence

The matched533/535 recordings have an exactly identical240000-sample PCM
window starting119.4156041667 seconds (one second after the last6478 cluck
cue timestamp) and lasting5 seconds. Maximum absolute difference and RMS
difference are0; native-window RMS is278.87945, so this is not merely both
recordings being silent. The comparison uses fixed timing, without fitting
phase/gain/latency or modifying sound assets.

Recording SHA256 values:

* native533:2526843B64FF92F6EEC6D72BE2689EE1DA1C3D2F6240DADCEF85906F7C5FAF7A
* matched control535:B124DCD3BCCADFB39F03D0E83A41BE305B64D4CA30B66A190DC24E2840AF0357

This is finite post-cue convergence on the historical matched-bank recordings,
not current-program audio capture, each voice's early-tail correctness,
absence of every transient or full overlapping-scene listening approval.
It does not promote the remaining full-scene/release acceptance flags.
