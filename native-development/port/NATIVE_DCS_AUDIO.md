# Native DCS audio candidate

Current6AE0 checkpoint: the paired stock_wolf_6ae0_audio_native/control
recordings complete normally.39 Friendship cue events match; a fixed
five-second post-cue window is sample-identical and non-silent. The held-out
overlap model still has relative residual0.168446, so early overlapping
tails and whole-scene mix remain uncertified. See CHICKEN_REFERENCE_MODEL_CHECK.md
and generated_dcs/DCS_CHICKEN_CURRENT_CONVERGENCE.json. No custom driver or
host sample playback is used; the unchanged current26-chip set includes
the native four sound ROMs. Older numbered experiments below are historical.

This is a development candidate, not final audio/mix acceptance. The notes
below describe successive historical audio experiments. The current native
development IPS package and checked workspace launcher now use the SoundP
four-ROM DCS set, not the old pre-audio snapshot. Current034F stock-MAME
campaign audits verify all26 actual ROM chips, including those four sound
ROMs. They do not certify final audible mixing or complete Friendship tails.
There is no custom emulator or host-sample dependency in this native route.
Older references below to an unchanged release/launcher describe the state
at that experiment, not the current checked development launcher.

The source-owned `sonya_square_launch.wav` clip is polyphase-resampled to
31,250 Hz signed16-bit little-endian PCM. Its captured peak was only1000, so
the candidate explicitly normalizes to a16384 peak before the lossy codec.
Both the original WAV hash and the exact conversion/gain are recorded in
`generated_dcs/DCS_INPUTS.json`; final loudness/provenance review stays open.

The original HENRY compressor accepts the raw PCM input and generates KSSQ.CMP.
Original PLBUILD produces four real Wolf DCS ROMs with own playlists2000/2001/
2002 on native effect tracks1/2/3. All original CMP inputs are hard-linked into
the isolated `baseline/mk2-rebuild-main/soundp/` staging directory, never copied
into a custom emulator. `soundw/` remains unchanged for A/B control.

TMS sound-priority table entryFE maps to these three calls; SONYAMOV.ASM invokes
it through the native triple_sound mechanism. `dcs_source.py` reproduces that
source extension, and prepare_game_candidate.py includes it in fresh builds.

Build sound with `start_background_compile.ps1 -Target sound`, then game with
`-Target game`. Both run hidden, below-normal priority, with SDL dummy drivers.
`-Target sound-info` is the bounded tool-help/reference-decode diagnostic, not
a gameplay acceptance build. Python staging additionally uses NumPy/SciPy;
exact versions are recorded in DCS_INPUTS.json.

For the new sound bank, run test_wolf_baseline.py with `--game --special
--square --sound-candidate --audio`. Omitting --sound-candidate deliberately
uses the old soundw bank as control. Neither test uses a host sample device.

## Evidence

`qualify_dcs_square_audio.py` pins current program, graphics, sound ROMs, stock
MAME0.289, frozen controllers and source/encoded PCM. Cases126(native) and
127(control) each finish9000 fields with12 real Square activations and no
missing animation markers. Both pass the existing command/hit/recovery checks.

The original codec's decoded output correlates0.9875 with the staged input
(16-sample codec delay). For actual stock-MAME WAV output, the native-minus-
control signal matches the decoded full clip at>0.95 correlation for11 launches.
The last launch is interrupted by an actual KO and native Finish Him on the
same DCS track. Its pre-interruption prefix correlates0.99785; the checker
requires the actual KO and matching higher-priority port call for this exception.
It does not count the interrupted cue as full-length playback.

Audio analysis reads at most1.36 seconds from each capture at a time; it does
not load full WAVs into large floating-point arrays. Original input/control
WAVs remain in their test folders as evidence.

The observer uses the documented stock-MAME pass-through write tap and returns
no value, so it does not change emulated writes:
[MAME Lua memory API](https://docs.mamedev.org/luascript/ref-mem.html).
General codec reference consulted:
[DCS Explorer](https://github.com/mjrgh/DCSExplorer).
The candidate itself is built with the supplied original HENRY/PLBUILD tools,
not DCS Explorer code or a modified emulator.

Other moves, selection/winner calls, interrupted-move coverage, final mix and
full original voice provenance remain open. This is proof of one real native
sound cue and its build path, not completion of the full audio requirement.
# Bicycle candidate: bounded stock-MAME check

Square regression on this expanded bank also passed in runs
`stock_dcs_square_native130` / `stock_dcs_square_control131`: twelve actual
activations, eleven full clip matches, and one proven native Finish Him
pre-emption after a matching launch prefix. `qualify_dcs_square_audio.py`
now accepts explicit run names and verifies the expanded playlist chain and
all three native sound-table entries, rather than relying on the old bank.

The expanded SoundP bank has separate KSBL launch (calls 2003–2005)
and KSBC paired-cry (2006–2008) playlists. Authored KSBIKE.ASM calls the
launch at entry and the cry only after an unblocked catch. SoundW remains
the control; the development IPS archive has not been promoted.

Runs `stock_dcs_bike_native128` and `stock_dcs_bike_control129` completed
9,000 fields on stock MAME with the same controller and program/graphics.
Both passed the existing physical-command/hit/block/duck/far-miss/recovery
qualifier: 11 activations, 352 paired fields, 22 hit damage, 3 block damage.
No guest-memory writes or custom driver were used.

`inspect_dcs_bike_audio.py` records bounded waveform measurements in
`generated_dcs/DCS_BIKE_AUDIO_DIAGNOSTIC.json`. Launch prefixes correlate
above .99 with the decoded native clip. Raw cry comparisons were weaker
because the native mixer plays launch and cry on separate overlapping tracks.
The diagnostic now fits launch gain on its earlier cry-free 4096-sample
prefix, then subtracts that independently fitted launch from the cry window.
All eight cry segments (reference samples 24000–47999 at 48 kHz) correlate
above .994, with observed output latency below 0.1 seconds. These are bounded
half-second segment proofs, not complete-tail or final-mix acceptance.
All eleven launch events align within two fields of action 516 entry; all
eight cry events align within two fields of actual unblocked paired action
532 entry. Misses and blocks do not produce extra cry events in this fixture.
The original last cry tail exceeded the recording boundary. Follow-up runs
`stock_dcs_bike_tail132` / `stock_dcs_bike_tailctrl133` extend recording to
9180 fields, release all attack/direction controls after 9000, and retain the
original eleven activations/eight catches. All eight complete cry waveforms
now correlate above .98 after independent launch subtraction; the verifier
also checks each entire reference fits inside the captured output. Both
extended runs pass the original behavior checks on their first 9000 fields.
This diagnostic does not assert final mix, release readiness or full-port
completion. The recording extension is physical-input/observation-only.
Original codec roundtrip correlations were .9939 (launch) and .9812 (cry).
Each stream analysis reads at most two seconds, not a full-match float array.

## Current pop-enabled bank Square regression

Runs stock_wolf_game374/375 recheck Square on the current program and expanded
SoundP bank versus matching SoundW control. The verifier now validates the full
Square -> Bike -> Announcer -> Kiss -> Pop playlist chain and regenerates the
entire current native sound-table extension, instead of expecting an obsolete
three-entry table. It also checks actual archive program/sound/graphics bytes,
not just receipt hashes, and requires identical profiles except sound-candidate.

Twelve launches: ten entire decoded clips match, one matches the complete
nonzero reference region, and one is interrupted by the observed native
Finish Him priority event after a matching prefix. Both9000-field tests exit
normally without missing markers or Lua errors. See the regenerated
generated_dcs/DCS_SQUARE_AUDIO_QUALIFICATION.json. No ROM code changed.
This is current-link Square audio regression evidence, not final mix or full
port acceptance. Campaign/boss and other pending coverage remain open.

## Current pop-enabled bank bicycle regression

Runs stock_wolf_game376/377 use the current program/graphics with SoundP versus
SoundW and extended9180-field captures. inspect_dcs_bike_audio.py now validates
the complete playlist extension chain, identical profiles except sound-candidate,
and actual archived program, graphics and sound bytes. Both runs exit normally.
All11 launch prefixes and eight full cry waveforms pass their existing bounded
correlation thresholds after independently fitted overlapping launch subtraction;
all eight full cry references fit inside the recordings. No full-match floating
point arrays are loaded. The refreshed DCS_BIKE_AUDIO_DIAGNOSTIC.json records
the exact ROM hashes and measurements. Final mix, all other cues and broader
gameplay/campaign acceptance are separate and remain unfinished.

## Current native selection and winner announcements

The announcer verifier now validates the complete current playlist chain and
actual program/sound/graphics archive bytes, matching physical-input profiles,
frozen observer hashes, no guest writes, passive port taps and no Lua errors.
Existing current-link captures376/377 prove both selection names and Sonya's
winner call;363/364 prove both selection names and two Kano winner calls.
All complete decoded announcement clips (including tails) correlate above.98
against the isolated native output, with observed latency below.1 seconds.
No new emulator run or ROM change was needed: those immutable captures already
contain the complete events. Refreshed DCS_ANNOUNCER_AUDIO_DIAGNOSTIC.json and
DCS_KANO_ANNOUNCER_AUDIO_DIAGNOSTIC.json record the exact case/hash evidence.
This does not assert final mix/provenance review or full gameplay acceptance.

## Current flame-kiss regression

Runs378/379 recheck the current program/graphics and expanded SoundP versus
matching SoundW. The updated verifier accepts explicit immutable runs, validates
the pop extension, actual archived program/sound/graphics bytes, matching input
profiles, passive observers and no Lua errors. Both physical two-round-win
fixtures complete the231-field fatality with60 orb fields and116 burn fields;
fixed-point motion, victim origin, own poses and native completion pass.

Complete kiss and victim decoded references still match after independent
overlap subtraction. Fire matches before its observed native same-track Flawless
Victory interruption, but its whole reference is NOT proved. The report retains
fireWholeReferenceMatched=false, audioQualified=false and finalMixAccepted=false.
An uninterrupted fire case and final listening/mix review remain needed; this
regression must not be reported as full audio acceptance. Current evidence is
generated_dcs/DCS_KISS_AUDIO_DIAGNOSTIC.json plus each run's behavior receipt.

Non-flawless follow-up: extract_probe.lua now has an opt-in physical-input
fixture (--nonflawless for --kiss) which receives a real opponent punch each
round before winning normally. Attempts380/381 failed to reach a fatality:
their approach threshold55 was below the observed collision separation62.
They remain failed evidence, not audio passes. Corrected threshold75 allows
382/383 to win both rounds and complete the same231-field fatality; both pass
SPECIAL_ROOT_REGRESSION. Winner HP150 at Finish Him confirms actual damage.
These current SoundP/SoundW recordings are ready for uninterrupted-fire analysis;
the existing interrupted-case verifier does not yet qualify this new profile.
No game ROM or guest memory was altered for these fixtures.

Uninterrupted analysis now passes for382/383. The verifier derives the expected
absence of Flawless from the pinned --nonflawless profile, checks actual winner
HP is below161, and requires zero matching same-track Flawless events. It fits
fire independently after the full victim clip, removes independently measured
overlaps and compares the ENTIRE184801-sample fire reference (3.85s at48kHz):
correlation0.98446, latency28.1ms. The full reference fits both the bounded
six-second analysis window and recording. Complete kiss matches0.99001 and
victim0.98489. The interrupted378/379 regression also still passes separately.

Both reports are retained: DCS_KISS_NONFLAWLESS_AUDIO_DIAGNOSTIC.json records
fireWholeReferenceMatched=true; DCS_KISS_AUDIO_DIAGNOSTIC.json keeps the native
interruption case and false whole-fire claim. Final mix/listening and full-port
acceptance remain false; waveform/reference matching is not subjective approval.

Ball cue gap: current KANOMOV.ASM still has no native launch voice. The original
donor capture from historical diagnostic_v6640 was hash-checked and copied into
the stable samples/mk2ks input folder (audio asset only; no old emulator code).
extend_dcs_kano_ball.py now defines bounded native HENRY input/playlist staging
for calls2033..2035 and sound-table index261. Dry encoding verifies the original
SHA3D2FB8BD79C818AA2079B10E869D3F1CF444B914582DB560CA64D4408EE57BD7,
55465 source samples at48kHz ->36111 at31.25kHz. The extension has NOT yet
modified SoundP or the game caller; compiler integration, clean reproduction,
runtime waveform and interruption tests remain required. Existing sound-bank
proofs remain current until the explicit next extension stage.

Ball extension is now staged and compiled: calls2033..2035, KSKB PCM36111
samples, native table105 (priority sp_attkv1,duration72), one tsound0105h at
Ball init_special_act. SNDBUILD/SNDINFO include original HENRY encode/decode.
Hidden sound/game builds exit0 with no created window (17.50s/19.07s).
Five Ball/pop/ending source tests pass. Stock-MAME run389 physically activates
Ball13 times, rejects the first short charge, hits and returns to stance, with
no missing markers; captured audio is non-silent. That is NOT waveform proof
of the Ball cue: matching control capture, decoded comparison/interruption,
clean sound/program rebuild and updated package proof still remain required.
Earlier audio verifiers/clean receipts are historical until extended to the new
Ball playlist link. Development ZIP remains unchanged and is not current-ROM.

Ball playback389/390: original HENRY decode completes hidden in3.85s. The new
inspect_dcs_ball_audio.py pins actual archived program/sound/graphics, frozen
passive observers, matching profiles and all13 port events within two fields of
real Ball action entry. Twelve full decoded references correlate above.98;
the last full reference does not match. Its prefix matches above.98 and ends
before an actual same-track942 Finish Him call at frame7279 after CPU/victim
HP reaches0 at7277. The verifier requires those facts for the exception and
keeps allLaunchesFullyMatched=false, provenNativePreemptions=1. It does not
count that interrupted cue as a full clip. Each analysis reads at most2seconds
per stream, with no whole-match float allocation. Both runs pass the current
Ball command/hit/recovery smoke check. Final mix, mirrored/interrupted-hit
coverage and independent clean rebuild remain open.

Mirrored Ball391/392 now passes physical player2 selection/charge/hit/recovery
checks (13activations, short-charge rejection, correct Kano17 versus Sonya18).
The controller records actual slot IDs/actions and separate P1/P2 held-LK fields,
not relabeled logical players. The behavior verifier now distinguishes move
identity from slot, and its original389 side1 regression still passes.
Mirrored audio actual-ROM checks and waveform diagnostic pass; per-event full
matches/native Finish Him exception are recorded separately in
DCS_BALL_MIRROR_AUDIO_DIAGNOSTIC.json. No game ROM changed. This adds opposite
slot coverage, not all hit interruptions, mix or campaign acceptance.

Additional open cue found: Sonya's current KSFRIEND chicken loop has no native
sound call (only Kano's pop calls tsound in that module). Four retained donor
variants a5/aa/af/96 exist. prepare_chicken_pcm.py dry-encodes bounded inputs;
test_chicken_pcm.py pins each source SHA and resulting PCM SHA/sample count.
No playlist, sound bank, ROM or package is changed by this preparation. Original
per-pose callback timing/track usage must be reviewed before native integration;
do not silently substitute one repeated sample or count animation as audio proof.

Original timing now independently pinned by audit_chicken_donor_timing.py:
the donor program dump's even/odd bytes exactly match mk321u54/u63 in mk3.zip.
At FF9D28D0 the full14-pose stream, including its loop pointer, has callback6
to FFAA6AA0 immediately before pose indices2/4/6. At FFAA6AD0 the four native
records are00A51010,00AA1017,00AF1014,00961012. CHICKEN_DONOR_TIMING.json records
the donor SHA and exact locations. Callback instructions/random selection and
track-allocation policy still need auditing before implementation; the current
ROM/sound bank remains unchanged. Old custom-driver timing claims were used
only to locate data, not as the original-byte proof or native acceptance.

Record-selection instruction audit now runs the pinned local TMS34010
disassembler directly on the verified donor ROM. Callback FFAA6AA0 sets4 and
calls FFAA6C00; that helper calls FF927780, decrements the result, shifts by5
and adds the inline record-table pointer before decoding priority/hold/command.
Disassembly and disassembler SHA are recorded in CHICKEN_DONOR_TIMING.json.
The native MKII equivalent can use randu4, four table indices with priority
sp_woosh1 (0x1000) and holds16/23/20/18, then triple_sound. No sleep is added
to ani_calla callbacks. Cue markers belong before loop poses2/4/6 only.
MKII's three-effect-track allocator differs from the donor's wider allocator;
complete overlap/priority behavior is not yet proved and must be tested, not
claimed identical from the record match. Working ROM and sound bank unchanged.

First native implementation: extend_dcs_chicken.py stages four own PCM clips
and calls2036..2047 (three effect-track variants each). MKSOUND adds indices
106..109 using original0x1000 priority and holds16/23/20/18. KSFRIEND's
non-sleeping callback saves/restores A0..A6, calls native randu4, and dispatches
through triple_sound; ani_calla markers precede poses2/4/6. Six PCM/Ball/pop/
ending regression tests pass. Hidden sound/game compilation exits0, no windows,
18.08s/23.45s. Working ROM/sound now changed; earlier clean/package proof is
historical until refreshed for this stage.

Current stock-MAME run393 physically earns two wins and completes Sonya's
Friendship in176fields. All intro/loop poses and existing timings still pass;
no extra animation delay was introduced. Captured audio is non-silent but is
NOT yet exact cluck-waveform, variant distribution or track-overlap proof.
Matching control, decoded waveform, mirrored/eligibility and clean rebuild checks
remain required. Development ZIP remains unchanged, not this current sound bank.

Cue-event393/394 comparison now passes actual program/sound/graphics archive
checks, immutable observer/profile checks and both native176-field choreography
qualifiers. Original HENRY decodes all four cluck inputs, hidden4.72s. There are
39actual port cues with all four variants. Seven occur during death-state7 at
donor-derived ages89/95/101/131/137/143/173 (port tap counter onefield earlier).
32continue with Sonya's dance during result presentation after action completion;
all retain the three-per42-field cycle positions. This distinction was missing
from the first verifier assumption; that initial assertion failed rather than
being counted as a pass. Candidate/control events match variant/track/age exactly.
DCS_CHICKEN_EVENTS.json keeps waveformVerified=false, overlapMixVerified=false
and resultEndCleanupVerified=false. No audio-tail/cleanup or final mix claim is
made from port events alone; waveform analysis is the next gate.

Waveform investigation found a codec-tail defect before acceptance: KSC0's
10187-sample input decoded to10080 and HENRY logged Sample length discrepancy.
The missing107 samples contained79 nonzero values (peak154), so they were not
discarded as silence. The PCM encoder now pads each cluck with zeros to a full
240-sample HENRY block, preserving every original encoded input sample. Explicit
pad_chicken_inputs.py verifies staged/source hashes before regeneration; test
coverage checks old complete PCM prefixes and zero-only added padding.

Hidden sound rebuild14.49s and decoder3.76s both exit0, no windows. Decoded
lengths match padded inputs for KSC1/2/3:14160/12480/11520 samples. KSC0 still
decodes to10080, so zero frame padding did NOT fix its tail discrepancy. This
remains an unresolved codec input/setting issue, not a passed tail check.
Program/playlist/callback cadence is
unchanged, but sound ROM bytes changed.393/394 audio captures are historical
for the padded bank and must not qualify current playback. New paired captures,
waveform/overlap tests and independent rebuild remain required.

One additional zero240-sample guard block resolves KSC0's decode length loss.
guard_chicken_inputs.py verifies the staged hashes and that regeneration adds
exactly480 zero bytes to each previous input, preserving every source sample.
Hidden sound/decode builds exit0 in14.14s/4.29s. All decoded lengths now equal
inputs:10560/14400/12720/11760. Source-prefix/zero-padding tests pass.

qualify_chicken_codec_lengths.py initially found weak zero-offset correlation;
bounded +/-240sample alignment identifies the same16sample codec delay in every
variant. Aligned correlations are.99259/.99307/.99386/.99398. Raw and aligned
scores are both retained in DCS_CHICKEN_CODEC_LENGTHS.json; no threshold was
lowered to turn the raw scores into a fidelity pass. Final fidelity/mix and
runtime playback flags remain false. Fresh paired runtime captures are still
needed because the sound ROMs changed;393/394 cannot certify this guarded bank.

Fresh guarded-bank395/396 pass actual archive cue checks and both176-field
physical choreography qualifiers. All39 event ages/variants/tracks match the
control; no extra/skipped action cues. Initial2048-sample prefix fitting was
weak because it mainly spans the captured clips' quiet lead-in. Using4096
samples captures each cluck attack: seven action prefixes correlate.98542 to
.99717 with output latency23.5..29.3ms after sequential overlap subtraction.
No source waveform or acceptance threshold changed to produce those scores.

Held-out whole-reference comparisons (not used to fit gains) do not all pass
.98. The diagnostic records each measured score/match and retains false full
tail/whole-scene flags; do not conflate seven prefix matches with39 complete
clips or final overlap mix. Further independent overlap/tail investigation,
mirrored/cleanup checks and clean reproduction remain required.

Full-tail mismatch follow-up: the diagnostic now searches +/-4 output samples
around each prefix-derived alignment while preserving the original fixed score.
All six whole references prefer offset0; the three lower correlations remain
.97563/.97007/.97495. Small alignment jitter therefore does not explain those
specific mismatches. No threshold, ROM or waveform was altered. The sequential
prefix-fit subtraction is still an incomplete mixture model, and its failed
full-tail flags remain intact. Investigate independent overlap/mixer behavior
next rather than repeating identical captures or counting prefix proof as tails.

Independent16-clip sound rebuild passes: the existing clean12-clip inputs,
439 original compressed/tool inputs and old sound outputs are hash-verified,
then all four guarded clucks regenerate independently from source WAVs. The
original two-block playlist allowance contains the added guard, so the staging
script now explicitly derives playlist delay from unpaddedSamples and asserts
the padded input fits. This reproduces the current playlist without changing
cue timing. No working CMP/ROM imported; hidden compile16.72s, no window.
All16 fresh CMPs and four1MiB ROMs qualify byte-identical to working SoundP.
From-scratch preparation includes the seventh extension stage too.

Six PCM/source regressions pass. Clean program inputs were verified and134
hash-pinned generated outputs (2912158bytes) removed, preserving all sources
and rebuild inputs. Only MKSOUND.ASM/KSFRIEND.ASM regenerated; hidden clean
program build is in progress. All26-chip proof/package refresh must await that
build. This source/rebuild work does not close the three full-tail waveform
mismatches, mirrored/cleanup coverage or campaign/final release gates.

Clean program compile now exits0 in61.04s without a window; all129 fresh
objects/four program parts compare byte-identical to working. Full26-chip
rebuild proof refreshes against395, including the guarded16-clip sound bank.
These rebuild checks do not assert waveform/mix acceptance.

Mirrored397/398 also complete the physical176-field Friendship after two
natural round wins. Native port-event checks pass the same seven action cue
ages,39 total cues, all four variants and result cadence, with candidate/control
variants/tracks/ages equal. Actual archived program/sound/graphics are pinned.
The mirrored event report is kept separately as DCS_CHICKEN_MIRROR_EVENTS.json;
do not infer exact mirrored waveform/overlap or cleanup proof from cue events.

Negative audio eligibility399/400: both physical slots earn two round wins
using punches, then the rejected Friendship fixture never enters its action
or completion state and emits zero2036..2047 cluck requests. The new
qualify_chicken_rejection.py reuses the current behavior/actual-program/gfx
checks and additionally validates actual SoundP archive bytes and port history.
Per-run CHICKEN_REJECTION.json retains exhaustiveEligibilityProof=false and
positiveControlRequired=true; eligible395/397 provide the contrasting positive
cases. These bounded fixtures do not instrument the exact eligibility branch
or prove every command-history edge. No ROM/source gameplay bytes changed.

Post-scene rejoin401: opt-in --friend-rejoin input fixture physically inserts
coins/start after completion and navigates the normal selector again. It does
not modify RAM or force a new match. Source/sound ROMs unchanged. The trace
reaches selection6502, fresh combat7053, then600 consecutive live combat fields
with true Sonya18/Kano17,161/161 starting health and actual damage to Kano.
Death/winner state is cleared throughout that bounded fresh fight; no missing
marker/Lua fault. Actual current program/sound/graphics archive bytes are checked.
All cluck requests precede the selector; no new ones occur during selection or
fresh combat. FRIEND_REJOIN_QUALIFICATION.json explicitly leaves all process,
palette and audible-tail retirement unverified. This is bounded fresh-match
state/request cleanup, not complete lifecycle, waveform or campaign acceptance.

Independent Ball sound rebuild now passes. refresh_clean_sound_pop.py --ball
verifies the prior clean11 PCM inputs,439 original compressed/tool inputs and
old clean ROM hashes before independently regenerating clip12 from the stable
donor WAV. No working CMP or ROM is imported. Hidden sound-clean exits0 in
16.44s without a window. All12 CMPs and four ROMs have fresh build timestamps;
qualify_clean_sound.py confirms all four1MiB ROMs byte-identical to SoundP.
The from-scratch preparation route now regenerates and records all six stages
including Ball. Current hashes are in CLEAN_SOUND_QUALIFICATION.json.

Clean program inputs were hash-verified,134 exact generated outputs removed
(2912093bytes), and only MKSOUND.ASM/KANOMOV.ASM regenerated for this cue. A
hidden clean program compile is in progress; no source/rebuild inputs removed.
Full26-chip proof must be refreshed only after that build succeeds. The existing
development IPS ZIP is still historical, and no final release is claimed.

