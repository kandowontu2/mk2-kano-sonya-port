# Kano/Sonya native integration release — 2026-10-15

## Current build and evidence

All fourteen original requirements pass the final root audit in
`audit_root_final_acceptance_20261015/report.json`. The final package is
`release_mk2_kano_sonya_20261015/MK2_Kano_Sonya_20261015.zip`; extract it and
run `PLAY.cmd`. Its member hashes/CRC and extracted CMD/complete ROM/23-sound
checks pass. The executable, game assets and modified compile sources are
unchanged; only the checker's stale status message and release docs changed.

The evidence combines current runtime and explicitly conserved component
tests, including both native identities, UI teardown, ordinary/special/CPU
combat, shadows, audio lifetimes, finishers, stage and campaign/secret routes.
It does not claim all possible input/RNG histories, four fresh current
campaign wins or subjective speaker judgement. Compilation-time incomplete
flags remain historical and are superseded by the final release audit.

Temporary extraction and the recent documentation-only intermediate ZIP
were removed. Measured allocation is lower by 252.49 MiB this pass, including
the final deliverable. Required sources and proof/reconstruction data remain.
Older dated notes below retain their original checkpoint scope.

## Historical verified checkpoint — 2026-10-12

The high-memory recording host5752 was stopped at the user's request. Its
unsaved raw video/audio and models were lost; they are not retained or
recoverable evidence. That recorder has not been restarted. Earlier saved
reports remain available, subject to their individual scope and source pins.

Recent bounded native tests exited normally at about118–122MiB working set.
They verify sampled presented body/shadow points during idle, walking,
crouching, kicks, jumps, contact reactions and uppercut knockdown/recovery.
Ordinary uppercut-hit and landing pain packets reach the correct native
male/female branches under Kano17/Sonya18 with matching actor ownership.
These are finite checks, not universal visual or heard-audio acceptance.
See CURRENT_PRIVATE_POST_RESET_STATUS.txt for current detailed evidence.

The existing public CMD's file verifier passed again: executable, ROM assets,
runtime receipts and seventeen waveform files match its expected release.
This proves file consistency only, not fresh interactive launch or finished
gameplay. The CMD and ZIP remain the older checked work-in-progress, not the
new private diagnostic build and not a finished release.

Full integration remains incomplete: broader runtime/arena/audio ownership,
remaining finishers, campaign/secret/morph/cinematic contexts and final
combined regression plus matching finished CMD/ZIP are still required.
No new emulator build, ROM copy, ZIP or retained raw media was made here.

## Historical checkpoint — invalidated RAM-retention claim

The following record is preserved for history only. Its claim that raw
recordings remain in host5752 RAM is false after the requested stop.

The corrected IN2 recording has finished normally (native21456, exit0) and
passes its actual capture/state checks with no Lua errors. All1800 dense
display snapshots and1646 PCM/DAC callbacks remain in host5752/session61435 RAM.
The new control checker passes every1063 live callback/26 Low Kick commands,
including real walking, native health/choices and eight effective fault tests.
All578 input pins are unchanged; see
`audit_native_selector_fresh_lowkick_controls_checked/report.json`.

There is a real161→135 hit on Sonya, but it precedes the only recorded private
voice launch (Square2571). It does **not** prove hit-induced voice cleanup.
Individual attack-instruction, source-timed owner, waveform, full display and
broader interruption/runtime acceptance remain open. No game is currently
running; retain the existing raw recording for those checks, rather than
replaying it. Full original scope stays active; public CMD/ZIP unchanged.

## Preceding resumed/live-capture checkpoint

Resumed after user request. The old host/session is now confirmed absent;
fresh test host5752/session61435 accepts commands. Independent complete
current models and the full collector preflight pass after explicit exact
historical-source relocation, with original hash gates/failures preserved.
The corrected ordinary IN2 Low Kick test is now **running**: native21456,
parent5752. It has not yet passed gameplay/interruption qualification. Observe
that same handle until its actual terminal; do not restart on output timeout.
Earlier raw RAM was lost with the old host; saved reports remain intact.

No new emulator build/ROM/raw-media/ZIP; public playtest unchanged. All original
requirements remain active, including broader runtime/final-release checks.

## Preceding blocked-access checkpoint

Current goal status: **blocked**, not complete. The same test-session input
restriction has recurred across at least three goal turns. Fresh process
inspection confirms the retained Python host is alive and no native game is
running; read polling succeeds, but commands are denied. The corrected IN2
controller remains prepared/unexecuted. Source checks cannot substitute for
the remaining live gameplay, finisher/victim/audio cleanup, stage/campaign/
secret/morph/cinematic and final combined release checks. The full original
scope is preserved. Resume requires restored test-session command access.
No new game/build/ROM/raw-media/ZIP/deletion; public playtest is unchanged.

## Preceding source-only guard evidence

Latest source-only addition: Sonya's complete second-finisher dispatch block
still matches its preserved actual compiled/decoded proof. A new guard test
passes722 local combinations of both slots/all19 opponent IDs/all19 performer
IDs, checks the true opponent pointer and ID, and rejects eight effective
faults. Bosses12/13 retire safely; ordinary/secret/added opponents route to the
owned action. All15 tracked current compile inputs remain unchanged.

See `audit_current_sonya_orb_boss_guard/report.json`. This is a source bridge
and local guard test, **not** current in-game finisher/animation/audio/cleanup
acceptance. No new game/build/ROM/raw-media/ZIP or deletion was performed.
The retained host is still alive, but terminal input remains denied; the
prepared corrected IN2 interruption capture has not run. Full original scope
remains active, and the public release remains the older playtest.

## Preceding voice-owner evidence

Latest addition: actual saved voice-owner fields now verify normal Square Wave
and Bicycle clip-end cleanup. All13850 owner snapshots match source-derived
timing/identity, both physical-slot arrays are clear at terminal, and17 effective
fault tests reject. This closes normal EOF cleanup only, not hit/KO/reset/morph
cleanup or all sound priority contexts.

The new Low Kick test itself was rejected: its inherited input lookup omitted
MK2's separate IN2 port, producing19 Lua callback errors. The original failure
is preserved. An IN2 binding/release correction is prepared but **not run**;
the retained terminal currently denies input, while the original Python host
remains live and the native game has exited. No successful interruption test
or gameplay fix is claimed from this recording.

The independent finite receipt is
`audit_native_selector_sonya_voice_owner_eof_sealed.json`:1686 unchanged whole
input pins and all15 compiled sources verified. New exact metadata/source was
compressed to14725897 stored bytes, with no new build, ROM, raw-media or ZIP
copies. The full original scope remains active; the public release is unchanged.

## Preceding movement/channel evidence

Latest addition: all19 sound-channel clocks and all133 native sound packets
pass for the retained Sonya CPU recording. Both fighters' complete horizontal
movement through the actual Bicycle contact, release and separate recovery
also passes:721 native word writes,376 instructions and166 next-frame physical
state comparisons. Eighteen sound/packet and nineteen movement corruption tests
reject; no new game or gameplay-source change was needed.

The integrated receipt is
`audit_native_selector_sonya_cpu_air_channels_horizontal_sealed.json`:
1660 unchanged whole input pins, all15 compiled sources and public endpoints
verified. New small source/metadata files were LZX-compressed from783225 to186832
stored bytes, with no new build, ROM, raw-media or ZIP copies.

This supersedes the earlier packet/channel/released-horizontal gaps only for
this recording. Broader opponents/arenas, private voice-owner retirement, sound
priority/heard quality, remaining effect cleanup, finishers and campaign/secret/
morph/ending contexts remain open. The full original scope is active, and the
public CMD and ZIP still point to the older playtest, not a finished release.

## Preceding contact/display/audio evidence

Latest private evidence: the retained real Sonya CPU walk/jump trial exited0.
Its complete native choice history contains three Bicycle Kicks: two misses
and one actual22HP unblocked contact. The entire contact's startup, paired
poses/lift/float, release, falls and separate recoveries pass; Sonya actually
launches another kick after regaining control. All1042 live input/state
callbacks retain true Kano17/Sonya18 roles. Eight state/control and sixteen
contact-phase corruption tests reject; the original earlier-Leg-Grab cleanup
checker rejection remains intact, not relabeled as a gameplay failure.

All1800 native scanouts and all1746 saved full CPU/DMA rendering passes match
exactly, including457703424 VRAM words and held snapshots. Fifteen effective
renderer faults reject. Twelve whole digest-bound RAM frames were inspected:
correct bodies, shadows, paired motion, release/landings and subsequent kick;
name shadows present and no selection portraits left over combat.

The whole1646 PCM/DAC callbacks and1580160 stereo frames match the native
source model with zero differences, including six launch/cry cues and two
Sonya winners. The next launch stops both old voice channels before starting
its new clips. That stop/cache behavior is source-bound; an incorrect overlapping
cry model changes920 channel samples. Nine waveform/source and twelve DAC/ROM
faults reject. The unrelated three-Ring and flush-before-stop checker failures
are preserved. No native replay, audio fit or persistent raw media was used.

See `audit_native_selector_sonya_cpu_air_sealed.json`:1652 whole source/evidence
pins, zero mismatches, all15 compiled-source files/fixed endpoints unchanged.
New small metadata/source files are compressed to about14.5MiB; no new build,
ROM, raw-media file or ZIP was added this turn. The original RAM host remains
available, with no native game running.

This closes finite contact/display/source-waveform checks, not the whole port.
Same-run native packet/all19 channel/owner/horizontal/effect-cleanup checks,
wider opponents/arenas/interruption, remaining finishers/victims/campaign/
secret/morph/cinematic integration, final combined acceptance and matching
public CMD/release ZIP remain open. Normal CMD/public ZIP remain the older
playtest; private current work has not been promoted.

The entries below are historical checkpoints.

Latest: four current v6640 released-input cross-character paid continues pass:
Kano→Sonya and Sonya→Kano, each in both physical slots. Every initial game
earns two genuine CPU collision losses, then uses actual credits/Start and
the complete original native UI/navigation/ladder controller. The P1 startup
punch is released correctly in both slots. Continued real actor/Main/roster
IDs17/18 and CPU roles remain exact; no Liu proxy, Game Over/restart or guest
health/position/CPU/RNG edits are used.

The whole existing adaptive actual-response controller is reused: native
walk, jump, standing punch and full recovery must actually occur, then180
ordinary Block survival fields follow. Inputs alone never count as responses,
and a hit-induced airborne reaction cannot substitute for the measured jump.
All four UI state/pixel contracts pass: native border thickness/blink/player
number, animated poses, unshifted backdrop, portrait/pose erasure, real ladder
objects and full visible source rasters, own selected-player ladder portrait,
and stock-style black lifebar-name shadows. Offscreen scheduled icons are
bound to native objects/world coordinates, not claimed as rendered pixels.
Twelve actual full native selection/ladder/match frames were inspected; this
finite appearance review does not claim every continued move raster or arena.

All72 original state/raster faults, nine additional image faults and36 actual
control-response faults reject. The pre-game Lua composition exit3 and two
fixed-time control attempts remain unaccepted: their commands landed in real
CPU hurt/get-up windows. The adaptive tests do not convert those inputs into
successful moves or relabel the original reports. Generated-gate retrieval/
parser/fault-predicate checker corrections retain their executed sources.
See `audit_cross_continue_adaptive_checked_*`, corresponding pixel/control/
visual receipts and `audit_cross_continue_adaptive_progress_storage/report.json`.

All native jobs and RAM review hosts are closed. No new build, ROM copy,
raw image/audio/guest transport, WAV or ZIP was added. Normal CMD stays on
v6508; private v6640 is not promoted. Broader continued stages/audio and
post-ending fresh joins, remaining finisher/secret/cinematic integration,
the full changed-source requirement audit and final matching CMD/release
remain open. The earlier cross-character gap below is now historical for
these four stage-zero routes only.

Latest: the Kano P2 challenger CPU-audio carry-in gap is closed for this
actual route. The retained native PID69532 exited0. Its expanded recorder
caught CPU Sonya's Bicycle launch/cry at1493, one field before the old1494
window, and the same human Kano launch/paid join/new-match controls. The
full-cold recorder remains rejected: native boot resets the DAC ring at5.52s,
leaving that one early callback without DAC transport. No boot-audio pass or
missing chunk is invented. Instead the intact interval starts at the first
original fully published, full-health precombat field1477, before either cue.
Every scheduled sound callback27.00s through the original terminal is used.

All1,986,240 stereo frames match the source-exact native DCS/DAC/cache/
resampler plus CPU Bicycle launch/cry, CPU Sonya winner, human Kano launch,
and both selection announcements. All4,528 physical/owner fields and9,056
battle-channel fields pass, including CPU EOF and human noncombat retirement.
Six audible waveform/source faults, four DAC faults, eight sound-ROM faults
and sixteen real owner/marker/position/coverage faults reject. The original
boot-recorder and scoped absolute-ordinal checker rejections remain intact.
No completed run was replayed, no native state was changed and no new build,
ROM copy, raw media or ZIP was produced. See
`audit_challenger_retained_precombat_checked/report.json` and
`audit_challenger_retained_precombat_faults/report.json`.

Released-input cross-character continues remain a concrete next requirement:
v6621 accepts four same-character routes on v6508, not the cross-character
matrix on current v6640. Broader continued stages/audio, post-ending joins,
remaining finisher/secret/cinematic integration and final combined acceptance
with matching public CMD/release ZIP still need completion. Normal CMD stays
on v6508; private v6640 is not promoted. The entries below are historical;
their old CPU carry-in limitation is superseded only for the interval above.

Latest: four current v6640 Shang morph/late-special/native-return cases pass,
covering Kano Ball and Sonya Square in both physical slots. The roster stays
Shang6 while the actual form ID is17/18. Original forward/return stores,
canonical floors, all19,208 continuous physical/owner fields and38,416
battle-channel fields remain checked. The native scheduler can defer return
while a late special is active; the unchanged return instructions and genuine
12-field final transformation are verified. Restored Shang walks, jumps and
attacks normally. Every8,424,960 stereo frames matches the original launch
source plus complete native DCS/DAC/cache/resampler, with zero differences.
All72 same-run state/input/source faults and68 PCM/source/DAC/ROM faults reject.
Twelve original frames were inspected: correct form bodies and alternate Kano
palette, floor shadows, retained Shang lifebar name and clean return body.
This is finite morph coverage, not a claim that every morph/secret branch or
all raster pixels have been accepted.

The preceding challenger checks also complete all four Kano/Sonya routes in
both slots: real credits/start, correct highlights, selection teardown,
rebuilt true17/18 fighters and ordinary post-join controls. Whole sound is
source-qualified for both P1 cases and Sonya P2. Kano P2 began with an already
active CPU Sonya Bicycle source whose launch preceded the observation window;
its complete gameplay/own-source teardown passed, but its full mixed-audio
window remains explicitly unverified. Do not infer the missing launch clock
from PCM. That observer gap, broader changed-source integration/continue/
finisher/secret/cinematic coverage, final combined acceptance and matching
public launcher/release ZIP remain open.

See `audit_morph_startup_return_progress_storage/report.json`,
`audit_launch_challenger_transition_progress_storage/report.json` and
`audit_launch_challenger_transition_p2_progress_storage/report.json`.
All native jobs and RAM hosts are closed. No builds, ROM copies, raw media,
WAVs, raster files or ZIPs were added. Sixteen compiled folders remain;
normal CMD still uses v6508, private v6640 is not promoted. Exact preceding
document bytes are at `status_history_morph_startup_return`.

The entries below are historical checkpoints; read their stated gaps alongside
the newer evidence above.

Both current v6640 Sonya Bicycle KO/reset cases now pass through genuine
original Liu Kang fireballs. Eight22HP hits earn each KO, then the original
winner/round-init/precombat sequence refills health. Both slots activate a
fresh Bicycle, receive another original fireball hit, recover and execute
ordinary walk/jump/punch controls. All8,350 continuous physical/owner fields,
16,700 battle-channel states, native health stores and sampled original
body descriptor/clip/FIFO publication remain checked. All115 observed native
projectile hit/miss branches bind original rectangles, source child/parent/
victim ownership and all18 real contact/health writes, including lethal
7→0 saturation. All three original fireball animation descriptors are
verified byte-for-byte, not approximated with one persistent rectangle.

Every3,661,440 stereo frames across the two full runs matches the native
DCS/DAC/cache/resampler plus all36 original Bicycle launch/cry sources,
including exact shared60Hz retirement and the auxiliary stream's native
short-circuit update behavior. Zero channel samples differ. All58 actual
state/input/body/stale-source/projectile faults and40 PCM/source/DAC/ROM
faults reject. See `audit_bicycle_launch_ko_round_checked_p{1,2}/report.json`,
`audit_bicycle_ko_round_faults_p{1,2}/report.json` and
`audit_bicycle_ko_projectile_faults_p{1,2}/report.json`.

The first new adapter boot failed before gameplay with native exit3; its
source, stderr and rejected capture remain untouched. The corrected cold
jobs exit0 with complete RAM-only transport. Original checker namespace
and high-only descriptor rejections are preserved; additive corrections
qualify the same completed jobs without replay or game-state writes. All
native jobs and RAM hosts are closed. No build, ROM copy, raw media, WAV,
raster file or ZIP was made. Sixteen compiled folders remain; normal CMD
still uses v6508 and private v6640 is not promoted.

Alongside the preceding Kano/Square results, this closes these finite
Bicycle KO/reset/source-lifetime contexts, not every possible ownership
transition or full-port acceptance. Selection/morph cleanup, broader
integration and the final matching launcher/ZIP remain open, with all six
original groups retained. Exact preceding documents are at
`status_history_bicycle_launch_ko_round`.

Sonya now passes two actual Square Wave KO/next-round runs on current v6640,
one in each physical player slot. Five native40HP uppercuts in P1 and seven
native26HP jump kicks in P2 earn genuine KOs. Both traverse original modes
2→5→6→7→2, refill health natively, activate a fresh Square Wave, recover and
execute ordinary walk/jump/punch controls. True18 roster/actor/Main/floor
bindings, all native health writes and sampled body descriptor/clip/FIFO
publication remain checked across7,774 continuous physical/owner fields and
15,548 battle-channel states. All44 actual state/input/body/stale-source
counterexamples reject. No health, position, actor or sound state was forced.

Every3,408,960 stereo frames across these two complete runs matches the full
original DCS/DAC/cache/resampler plus owned Square source prediction, with
zero differing channel samples. All14 actual source launches and12 pre-KO
incoming hits are accounted for, including lethal contact and fresh owners
after reset. Sixteen PCM/source, eight DAC and16 sound-ROM faults reject.
See `audit_sonya_launch_ko_round_checked_p1/report.json`,
`audit_sonya_launch_ko_round_checked_p2/report.json` and
`audit_sonya_ko_round_faults_p{1,2}/report.json`.

The original two terminal0 attempts had an incomplete passive observer:
Lua's multi-return substring expression retained only its declaration.
Those rejected captures and executed sources remain unchanged. After both
were confirmed terminal, two fresh cold regression jobs used the corrected
observer with identical physical controls. A separate dynamic-source lookup
failure is also preserved; its adapter reads the retained whole predictor.
These are test-observer/model fixes, not suppressed native game failures.
All four native jobs and both full RAM carriers are now closed. No build,
ROM copy, raw media, authored WAV, raster file or ZIP was generated.

This closes these finite both-slot Square KO/reset/source-lifetime cases,
not Bicycle KO/reset, selection/morph cleanup, all arenas or whole-port
acceptance. Normal CMD remains v6508; private v6640 is not promoted. All six
broader integration/release groups remain open. Exact preceding document
bytes are retained in `status_history_sonya_launch_ko_round`.

The entries below describe earlier checkpoints; their stated gaps must be
read alongside the newer evidence above, not as new failures.

Two real current v6640 Kano mirror runs now earn a KO through four native
low-kick/roll clashes, traverse the original winner/round-init/precombat
states, refill both actual health bars to161, activate fresh rolls, recover,
and execute ordinary walk/jump/punch controls. Both true17 rosters and owned
Main/floor bindings stay correct across7,476 continuous physical fields;
temporary null actor publications occur only during native round-init mode6.
Every original damage/reset/sentinel/animated-fill health store is bound to
its native PC/opcodes and fully explains every observed health transition.
Actual native IN0/IN2 words and sampled body descriptor/clip/FIFO publication
remain exact. No health, position, actor, RNG or sound state was forced.

The surviving roll does NOT keep playing through the winner state: the
existing compiled noncombat guard retires it before the winner announcement.
The older EOF-only test assumption is retained as a rejected model receipt.
Its correction derives a unique original60Hz guard tick from actual native
mode/owner snapshots, not from fitting PCM. All7,476 owner snapshots and
14,952 battle-channel states qualify across both runs, including fresh
post-reset owners and final retirement.

The second held run's entire1,650,240 stereo frames match the source-exact
native DCS/DAC/cache/resampler plus original winner/roll samples and compiled
voice-speaker mixing order, with zero different channel samples. The first
noninteractive host released its PCM before this comparison; its waveform
acceptance remains explicitly false. Native terminals were0; no completed
job was replayed. This verifies these two Kano mirror/round contexts, not
Sonya KO/reset, selection changes, morphs, all arenas or all-port audio.
See `audit_launch_ko_round_checked_p1/report.json`,
`audit_launch_ko_round_v2_checked_p2/report.json` and
`audit_launch_ko_round_p2_eof_model_rejection/failure.json`.

All44 actual KO/reset/identity/health-fill/body/input/stale-source-state
counterexamples reject across both same-run logs. The held full audio proof
also rejects six actual PCM/roll-channel faults, four DAC faults and eight
whole sound-ROM faults. Actual native jobs and both RAM hosts are closed.
Only finite compressed source/gzip/digest/proof leaves remain. No new build,
ROM copy, raw media or release ZIP was made, and the normal launcher remains
v6508. All six broader integration/release groups remain open.
See `audit_launch_ko_round_faults/report.json`.

Current v6640 now passes four real human mobility/ground/shadow cases against
stock Kitana, one per character and physical slot. All148 retained400x254
native frames replay exactly from actual pre-DMA VRAM, full draw ordering,
source graphics, display flips and loaded palettes. Both imported characters'
eleven standing samples have the same sole row228 and stage/camera-relative
offset-1 as Kitana. Both real jumps, crouch releases, walking and landings
retain their actual owned native floors. All120,162 original compressed
shadow-row copies match their native cache ownership, source stepping,
quarter-height cadence, pen15, coordinates and callers. Visible black floor
shadows are present in every retained movement raster. This is Dead Pool
coverage, not all-arena/all-pose/all-finisher grounding acceptance.

The initial KanoP1 job ended normally0 but its collector discarded one HUD
name source after comparing it with uninitialized ROM-lane space. Its failed
report remains unchanged. The compiled startup code generates that stream
from the actual UI mask and original HUD gold ramp, including shadow pen2.
Same-terminal exact raster replay uses this independently predicted name;
the lost actual source stream is explicitly NOT accepted as captured bytes.
The other three previously unstarted native jobs retain and verify every
actual source stream against the corrected full native initialization oracle.
No first-job replay, game-state writes or new build were used.
See `audit_launch_ground_native_names_checked/report.json`.

All72 actual native row/raster/identity/latch/VRAM/palette/source/sole/shadow
counterexamples reject across the four same-run RAM carriers. Eight full
current native frames were visually reviewed for standing, jumping,
crouching and walking, without writing any image files or borrowing old
runtime acceptance. Natural feet placement and visible shadows agree with
the exact source/raster checks. All native jobs and the RAM review host are
closed. See `audit_launch_ground_faults/report.json` and
`audit_launch_ground_visual_review/report.json`. The normal v6508 launcher
is unchanged, v6640 remains private, and all six broader integration/release
groups remain open. This is verified finite progress, not whole-port release.

Fresh v6640 presentation checks now pass all four real Kano/Sonya campaign
selection-to-first-match contexts, without changing the original physical
controller or native game state. All684 displayed callbacks and both actual
guest/owned GFX inventories per case remain RAM-only. The entire original
state/pixel model checks dedicated portraits, settled horizontal/vertical
navigation including Reptile, native cursor thickness/blink/player number,
animated poses, unchanged backdrop alignment, immediate portrait/pose
clearing, genuine native ladder icon consumers, true fighter identity and
stock-style lifebar name shadows. All46 original reported-failure test methods
pass against these actual current frames, including the broken Sonya
selection, thin/shifted border, frozen animation, lingering portrait/pose,
wrong underlying fighter and missing name shadow counterexamples.

All15,952 cold-boot/selection/ladder/first-match battle-owner snapshots are
clear for both slots, with24 actual stale actor/Main/ID/HP or missing/duplicate
field faults rejected by the exact executed owner gate. All four actual native
jobs ended normally0 with empty stderr and no transport errors. Their RAM
carriers are released. See `audit_launch_candidate_ui_checked/report.json`
and `audit_launch_candidate_ui_cold_owner_faults/report.json`.

Twelve full actual current frames equal retained native PNG backing pixel for
pixel (1,219,200 RGB pixels); no historical runtime acceptance is transferred.
The main agent visually inspected both characters' selection, ladder and
fight frames: correct numbered native borders/poses; ladder icons without
full selection avatars/poses; real Kano/Sonya bodies and name shadows.
See `audit_launch_candidate_ui_image_backing/report.json`. This is finite
visual review, not a universal floor-shadow/sole-alignment/full-raster claim.
Side-by-side sole placement across complete native poses remains part of the
ground/render audit, alongside remaining ownership/transition integration.

No new build, ROM copy, raw media, authored WAV, raster file or ZIP was made.
The normal launcher remains v6508; v6640 is not promoted. The complete original
remaining groups and final matching release remain open. Exact preceding
document bytes are retained in `status_history_launch_candidate_ui`.

Two actual selected-Kano mirror runs now verify simultaneous roll startups
with either player controlling the full two-cycle/ordinary-follow-up driver.
The native scheduler resolves both rolls in each cycle: P1 takes24HP and
its startup source stops, while P2's independently owned source keeps its
complete original tail. Both true actors recover naturally. All eight real
markers bind their own actor/Main/ID and physical slot; the shared60Hz timer
starts at the earlier actual marker, not separately for each voice.

The entire original repeated-special physical/body-descriptor/clip/FIFO,
health ledger and walk/jump/punch recovery contract remains checked, with
only actual mirror identities/HP and the exact original close elbow admitted.
All native IN0/IN2 reads match the whole real button timeline. Every1,278,720
stereo frames across both runs matches the full original source prediction
with zero differences; neither player source is omitted or fitted. All56
actual owner/Main/ID/HP, stale-owner, interrupted-clock, cross-player
cancellation, body/FIFO and input-bit faults reject and whole positives restore.
See `audit_launch_dual_roll_checked_p{1,2}/report.json` and
`audit_launch_dual_roll_faults_p{1,2}/report.json`.

This is finite same-character overlapping-start/hit/EOF ownership coverage,
not complete mixed-character overlap, relaunch, KO/reset/selection/morph,
all rendering or full integration. Both native jobs ended normally0, their
qualified RAM carriers are released, and no new build/ROM/raw media/WAV/ZIP
was created. The ordinary launcher remains on v6508. All original remaining
integration groups and final matching release remain open. Exact preceding
document bytes are in `status_history_native_dual_roll`.

Latest projectile-counter checks now qualify two genuine incoming hits and
complete recovery for Kano's roll and Sonya's Bicycle in each player slot.
All eight hits are real original Liu Kang projectile contacts, each doing
22HP damage. The checks retain the whole physical input delivery, true
character/actor ownership, native collision branches, health ledger,
body-descriptor/clip/FIFO and subsequent walk/jump/punch recovery contract.
Kano is hit by the original low fireball; Sonya by the high fireball. Native
air hurt preserves the special action value while changing the actual hurt
flags/body/flight state; cleanup is verified from those source-owned states,
not an assumed uppercut action. Both exact original low-fireball descriptors
and every observed hit/miss branch are checked against the unchanged ROM.

Every2,137,920 complete stereo frames matches the original source prediction
with zero differing samples, including the precise timer/stream stop of each
owned interrupted launch/cry. All100 actual semantic,32 waveform/source,
16 DAC and32 sound-ROM counterexamples reject. See the four
`audit_launch_fireball_faults_checked_bicycle_p{1,2}_delay1/report.json` and
`audit_launch_roll_fireball_checked_ball_p{1,2}_delay16/report.json` receipts.
Earlier executed fixed-word fault and high-only descriptor model rejections
are preserved; additive adapters correct those exact checker errors without
replaying the native jobs or dropping their complete positive contracts.

All five new native jobs ended normally0 with no observer transport errors.
The one high-fireball Kano attempt remains unexercised for incoming damage:
the roll hit Liu before the fireball was released. It is not an accepted
interruption or proof of invulnerability. All five RAM carriers are released.
There is no new build, ROM copy, authored WAV, raw media or release ZIP.
The ordinary CMD still selects v6508; v6640 remains private. This closes only
these finite both-slot roll/Bicycle interruption and source-stop checks,
not full interruption/raster/game integration or a finished release. Overlap,
KO/selection/reset/morph ownership, current full presentation regression and
the other original integration/release groups remain open. Exact preceding
document bytes are retained in `status_history_native_projectile_interruption`.

The following input-correction notes describe the preceding checkpoint;
its unlanded counter attempts remain unchanged historical evidence.

Latest native-counter work corrected a passive test-observer error: address
01D00000 is DCS status, not the physical input register. The compiled map
places IN0/IN2 at01600000/01600020. The retained Bicycle P1 run now verifies
all2,264 IN0 reads,1,164 IN2 reads and every668 original IRQ fields per port
against the complete real button timeline. Four actual bit/missing-field
faults reject. Prior Square interruption core proofs remain unchanged; their
input-read descriptions were incorrect and did not prove button-bit isolation.
See `audit_native_input_delivery_address_correction/report.json`.

The same retained Bicycle run passes the whole native two-cycle recovery,
health, true identity, body-descriptor/clip/FIFO and walk/jump/punch contract.
The first checker rejected its legitimate close elbow because it expected
only standing action101. The correction admits the exact unchanged original
action114/animation22 startup, six actual grounded startup fields, native60B
contact/recovery and the real24HP close strike; the rest of the original gate
is retained. Four actual action/contact/floor/damage faults reject. See
`audit_native_close_recovery_checked/report.json` and
`audit_native_close_recovery_faults/report.json`. This is not an accepted
incoming-hit interruption or a complete port/release claim.

The grounded and jump counter attempts so far do not land an incoming hit on
Kano's roll or Sonya's Bicycle. Actual late HP does enter the stock uppercut,
but Bicycle hits its startup; earlier cold-crouch presses were ignored.
The measured early jump crosses above Bicycle, while the later jump is caught
by its startup. These are retained unexercised attempts, not green interruption
tests or proof of invulnerability. One failed observer boot exited3 due to
its Lua concatenation error; its corrected successor and other jobs exit0.
Kano/Bicycle interruption coverage remains open. The ordinary CMD stays on
v6508; no candidate promotion, new build, ROM copy or release ZIP occurred.
Exact preceding current-document bytes are in
`status_history_native_input_correction`. The full integration goal remains
active, including the final matching playable launcher and finished ZIP.

Current playable: `diagnostic_v6508_native_projectile_identifiers`.
Run `PLAY_MK2_KANO_SONYA.cmd`; the root latest alias and both task-folder
wrappers now route to the same checked repaired build. The versioned v5219
launcher, build, ZIP and saved settings remain available and unchanged.
This is a repaired work-in-progress, not a finished-release claim.

New isolated candidate: `diagnostic_v6640_kano_ball_launch`, accessible through
`TEST_KANO_BALL_LAUNCH_V6640.cmd`. It is not promoted to the normal launcher.
Kano's missing roll-start voice now uses the actual original MK3 Kano group4
command0208 donor waveform, including its measured delivery latency and full
tail. The native roll action issues one owned cue; no generic grunt or proxy
character substitutes for it. Only246 initialized guest bytes change, comprising
one port marker and four relocated internal branches; all old roll instructions
and every other guest/GFX byte are retained.

The new executable passes the full sixteen-case two-cycle specials regression:
32 real activations/recoveries,18,260 owned actor fields,295 full-screen digests
and194 rejected actual semantic counterexamples. See
`audit_v6646_kano_launch_special_matrix_checked/report.json`.
Four additional native audio runs cover both slots with samples enabled and
disabled. Every2,760,960 stereo frames matches the full source prediction;
the enabled runs account for1,380,480 frames with both real roll-start cues,
complete tails and exact per-player channel clocks. Their samples-disabled
controls retain identical entire physical/RGB and original DCS DAC/clock
chronology. Wrong source/slot/loop/pause/length/clock, PCM, DAC and ROM faults
are rejected. No raw PCM, DAC, guest or RGB transports were written to disk.

The first host identity capture remains rejected despite its natural terminal;
the successor uses prompt read-only kernel process queries. The first audio
model's saved-source-number rejection is retained: native samples.cpp assigns
that number using the previous source length, so a first playback reports-1
while its live source pointer advances. The corrected model preserves that
exact operation, full source-position/EOF checks and every-output-sample
equality; it does not skip the first cue or weaken the audio window.

The retained native CPU mirror match now passes both actually chosen rolls,
including complete contact/damage/recoil/landing and both recoveries, plus
both declared completed chokes. The whole 1,800-field state/health/AI ledger
retains its genuine human KO and native round reset; 47 actual motion faults
are rejected. See `audit_v6666_kano_cpu_launch_motion_checked/report.json`.
Every 1,580,160 stereo frames matches the complete native DAC plus both real
roll-start cues and the true Kano winner source, with 23,044 precise physical
channel states, 74 native packets and all 148 actual DSP reads accounted for.
Four DAC, eight ROM, eight raw/source-output and fourteen actual audio-record
faults are rejected. See `audit_v6671_kano_cpu_launch_audio_checked/report.json`.
This is the actual changed native trajectory, not a claim that it matches the
old one-roll/42-scene fixture: all 98 actual full-screen callback digests remain
retained, but source-raster acceptance is separate. Both null actor publications
during native mode6 teardown are bound to the full independent round ledger,
not fabricated fighting actors. Original capture and host-model failures remain
false; the same naturally terminal match was qualified without replay.

Two genuinely interrupted Square Wave cycles now pass in each physical slot
on the isolated v6640 candidate. P1 receives two real 40HP stock uppercuts;
P2 receives two real 26HP stock jump kicks. Both retain true Sonya identity,
the complete native health/body/publication ledger, full recovery and ordinary
walk/jump/punch afterward. All battle audio owner/identity fields clear by the
first gameplay callback after contact, and interrupted source clocks freeze.
Every 1,053,120 stereo frames across both complete windows equals the source
prediction, including the unsynchronized native stop operation and cached
samples. The proofs reject 36 actual semantic-record faults plus their full
PCM/source, DAC and sound-ROM fault suites. See
`audit_v6692_launch_interruption_checked_square_p1_delay1/report.json` and
`audit_v6697_launch_jump_interruption_checked_square_p2_delay1/report.json`.
This is Square Wave interruption evidence, not complete fourteen-channel
clock, raster, all-move, KO/reset/selection/morph or full-port acceptance.
Nine other physical input attempts produced no incoming hits; their genuine
terminal captures remain explicitly unexercised, not falsely counted passes.
The original broad stock-kernel assumption rejection is preserved: legitimate
port relocations lie inside that interval. Its correction validates the whole
independently reconstructed current guest and explicit unchanged air-kick/
health-writer intervals. No failed capture or old report was rewritten.

Broader CPU overlaps, remaining hit/KO/selection/reset/morph ownership cleanup and full
current UI/ground/render/audio regression remain necessary before public
promotion. Remaining continued-game, arena, finisher, secret/morph/
cinematic and final release requirements below are unchanged. Earlier native
results do not automatically qualify this newly compiled build.
The three dirty sources and installed executable were restored exactly after
compilation, and the generated compiler cache was removed. Exact preceding
status-document bytes are in `status_history_v6659`, `status_history_v6674`
and `status_history_v6700`;
old reports remain intact. No new build, ROM copy or ZIP was made for this
same-run CPU qualification. The ordinary CMD remains on v6508.

Follow-up: the historical player-two continue driver left the other player's
startup High Punch held. Its eight routes remain finite identity/control
evidence under those actual inputs, not clean P2 presentation/input-isolation
proof. `audit_v6601_input_release_discrepancy/README.md` documents the native
IO semantics. New drivers release that key and observe every real IN0 callback,
including boot frame0. No playable binary or ROM was changed for this work.

The corrected genuine paid-continue captures now cover Kano and Sonya in
both human slots. The full stock-controlled border/number/blink/background/
animation/portrait-and-pose teardown/true owned match/name-shadow model is
retained. Continued stage-zero ladder views are checked against native
source positions and actual objects: a character above the viewport is not
incorrectly required to render on screen. All visible added tower portraits
are complete source-raster matches; offscreen raster rendering is not claimed.
The cold-start full-reveal both-icon check remains separate and unchanged.
Original failed capture reports are preserved. Broader continue audio,
post-ending fresh joins and the remaining full-port requirements remain open.

The historical single-player matrix covers eight real CPU-earned routes: Kano and
Sonya, either human slot, keeping or switching character on paid continue.
Each route verifies two genuine161HP losses, physical payment before Game
Over, the requested real character/Main, a genuine CPU opponent, actual
walk/jump/punch/recovery and180 further native gameplay fields. That driver
used earlier P2 payment with the startup-key leak described above; those
inputs must not be promoted to clean-input visual or ordinary-control proof.
A restart after Game Over is rejected.
Paired leg-grab damage and child Ring damage resolve to the actual CPU
ownership links, not an assumed direct attacker process. See
`audit_v6600_single_continue_matrix_checked/report.json`.

Earlier failed captures and ineffective observer/fault selectors remain
recorded. Exact executed source snapshots preserve intentional test-source
alias changes; no captured failing report was changed to pass. Six inspected
PNG scenes are bound back to every byte of their native unscaled screen
buffers. Kano/Sonya match names and floor shadows are present; the inspected
Sonya-P2 transition clears completely. Early observer labels mentioning the
ladder can still capture CSS before its native fade and are not ladder proof.
Full continued-ladder visual/audio and post-ending fresh-join checks remain.
No new executable, ROM payload copy or ZIP was created for these tests.

Current launch proof: `audit_v6554_repaired_default_launcher_checked/report.json`.
The actual ordinary CMD passes the native ROM audit, sixteen-voice checks,
five mismatch-denial simulations, unscripted cold boot, Windows executable
identity and natural terminal checks. Isolated tests preserve user settings.
Four further actual normal-CMD combat cases pass both projectile moves in both
slots, two activations each and ordinary walk/jump/punch afterward: 3,210 actor
fields, 71 full-frame digests and all fifty original corresponding fault tests.
See `audit_v6562_repaired_public_contract_checked/report.json`.

Fresh repaired Ring hit/block/miss checks cover 247 full continuously reconstructed
screens with native ownership, floor-shadow copies and retirement/erase checks.
Kano's blade/blocked-knife/KO/reset sequence passes all 641 complete scenes,
source-derived art, palettes, FIFO projection and same-field retirement checks.
The new Ring audio proof compares 561,600 stereo frames to the native source
prediction and qualifies twenty packets and ten audio faults. These finite
cases do not establish every arena, overlap, effect or sound-priority context.
See `audit_v6558_repaired_projectile_storage/report.json` and its child reports.

Original strict Kano capture rejection remains false: precisely one historical
field expected the old instruction-overread task ID CB0C instead of repaired
ordinary P2 ID0800. The additive qualifier derives both IDs from the actual
whole guest images, compares all 14,238 rows and rejects six actual-row faults.
All 641 scene records are identical. No failing captured report was rewritten.
One inherited native CPU-choice hook emitted a 54,551-byte PNG; it is explicitly
disclosed and retained as pinned evidence, not falsely reported RAM-only.
The selected new projectile evidence/source files occupy 9,188,370 allocated
bytes after lossless compression. No additional build, payload copy or ZIP
was created; the regenerated compiler cache remains absent.

Promotion and storage receipt: `audit_v6566_repaired_native_handoff/report.json`.
The ordinary timed boot also created its native 1,692-byte exit snapshot;
this is disclosed separately from the RAM-only gameplay/audio transports.
Exact former root/task launcher bytes are in `launcher_history_v6552`.
Old reports remain immutable: their historical routing hashes deliberately
differ from the current aliases. The compile-time build manifest is also
unchanged; later runtime acceptance is recorded separately.

Still open: broader projectile/CPU/arena/shadow/audio contexts; current
post-ending fresh joins and full continued-ladder visual/audio coverage; remaining Pit/Tomb
stock-victim choreography and sound priority; cannonball donor launch-cue
CPU/interruption/overlap fidelity and new-build regression before promotion;
remaining secrets, morphs and cinematics; final combined regression
and a matching finished release ZIP. Existing v5219 campaign/finisher evidence
is not automatically complete changed-build acceptance. The existing v5219
ZIP remains a historical playtest package, not the current repaired playable.
Goal: active.

## Earlier checkpoints (historical, before current launcher promotion)

Latest checkpoint: `audit_v6535_repaired_candidate_progress/report.json`.
The isolated projectile-identifier repair is compiled as
`diagnostic_v6508_native_projectile_identifiers`; it is not promoted to the
public launcher or ZIP. Every newly observed initialized guest byte matches
the independent reconstruction: exactly 158 bytes changed in two packed-ID
tables and their two lookup operands. All stock rows, payload/art/audio and
other compiled sources are unchanged. Preexisting dirty canonical sources
and installed executable were restored exactly after compilation.

All four fresh cold CPU/challenger routes now pass on this candidate, including
the exact Sonya-P2 lockup. The CPU ring still earns the KO at 2130 and native
join purge runs at 2156; every pre-purge physical/health/actor record is unchanged.
The ring now has ordinary task ID 0700 instead of bogus protected B700. Actual
post-purge task membership shows both the ring and linked polling task retired;
the native assertion is absent, selection returns, and the real Kano/Sonya
match completes 600 ordinary fields per slot. All four cases qualify 6,240
joined actor fields, 32 gameplay faults and three root-cause faults. See
`audit_v6527_repaired_challenger_fault_scope_checked/report.json`.

Sixteen fresh repaired-build special cases pass: all eight moves, both slots,
two physical activations each, complete recovery and ordinary walk/jump/punch
afterward. The whole original gate rejects 194 actual-record faults and checks
18,260 actor fields. All 295 captured full-frame digests and entire non-guest
special/actor/input/health/body/publication traces match the prior accepted
v5219 cases. This does not prove all projectile/CPU/KO/shadow/audio contexts.
See `audit_v6515_repaired_special_matrix_checked/report.json`.

Four fresh repaired-build UI cases also pass the whole original selection,
navigation, portrait/animated stance, native numbered/blinking border,
backdrop, teardown, ladder-icon and true first-match/name-shadow checks.
All 684 displayed callbacks are byte-identical to the prior accepted UI;
46 original state/pixel test methods pass. Twelve full frames are bound to
existing native PNGs, including the first-match floor-shadow presentation.
This is finite UI/first-match coverage, not all arenas or airborne shadows.
See `audit_v6533_repaired_selection_transport_checked/report.json`.

Actual failed runs and qualifier/recorder mistakes remain preserved. The first
new-candidate join run failed host identity observation; its entire gameplay
and captured pixels match the passing successor. The first UI recorder used
the wrong native snapshot API signature; its naturally terminal game and Lua
assertions remain a failed qualification. Only the recorder binding changed,
then all four full UI cases and their negative tests were executed successfully.

The regenerated object/archive cache was removed, with retained candidate,
source and prior playable hashes verified. Its post-deletion size aggregation
failed, so exact reclaimed bytes are unknown, not estimated. Recovery receipt:
`audit_v6523_compiler_cache_retirement_recovery_checked/report.json`.
The new executable occupies 17,997,824 allocated bytes after lossless compression;
the selected new candidate/source/test evidence set occupies 20,686,083 allocated
bytes, excluding its hardlinked existing payload and the checkpoint output.
No new ROM payload copy, raw media or release ZIP was created. All native test
processes are terminal; the cache remains absent.

Next: repaired projectile hit/block/miss, overlap/render-group retirement and
native shadow/audio checks, then appropriate launcher promotion. The broader
remaining work below stays open. Existing v5219 campaign/finisher/CPU evidence
does not automatically qualify every aspect of a changed build. Goal: active.

Previous source-only diagnosis: `audit_v6506_challenger_projectile_progress/report.json`.
It preserved four identical genuine Sonya-P2 failures and staged the guarded
repair; the new compiled/runtime evidence above supersedes its unbuilt status.

Previous checkpoint: `audit_v6485_current_requirement_routes/report.json`.
The current CMD now has four verified paid cross-character continuations:
Kano to Sonya and Sonya to Kano, in both physical player slots. Each uses two
real collision-earned losses, coins/Start, native re-selection, a new match,
and ordinary walking/jumping/landing. All 1,280 consecutive continued-fighter
fields retain the requested real ID, roster and Main ownership; sixteen
actual-record corruptions are rejected. No executable or ROM was changed.

Five native runs were used: four passing cases and one retained test-hook
failure. That failed run completed gameplay but its RAM snapshot hook had a
missing Lua callback binding. Its corrected successor has identical complete
physical input, state, health, mode and independent post-field rows, empty
stderr, and 453 full-frame RAM digests. No raw images/audio were written.
The exact new source/evidence set occupies 4,926,773 allocated bytes after
lossless compression; all native and capture processes are terminal.

The requirements audit also resolves two reporting-format issues: the human
move journal has no generic `passed` flag but pins eighteen passing current
children; the full ending report uses `sourceInputs`, whose 676 pins are intact.
Two historical Tomb reports pin an older version of the evolving cleanup
notes. Those mismatches remain disclosed, not rewritten or counted intact;
no tested code or asset hash mismatch was found in the inspected pin maps.

Remaining work is concrete: current single-player continue and challenger/
post-ending join routes; remaining Pit/Tomb stock-victim choreography and
sound-priority coverage; cannonball donor launch-cue fidelity (the current
move has no startup cue); remaining secret/morph/cinematic integration; then
the combined visual/audio regression and finished matching release. Existing
four campaigns/endings and separately qualified CPU move cases are not
untouched work. These continue tests do not claim complete UI pixel/audio,
all route, all arena or full-port acceptance. The goal remains active.

Run `PLAY_MK2_KANO_SONYA.cmd`. It now selects v5219; the task-folder CMD forwards
to this same launcher. No compiler or Python is needed to play. The launcher
checks its executable, payload and sixteen voice assets before starting.

The actual default-CMD cold boot, clean ROM audit, native executable identity,
natural exit and unchanged user settings are recorded in
`audit_v6241_current_default_launcher_checked/report.json`. That test was
headless; it is not an interactive visual/audio-quality approval.

The canonical CMD also passed sixteen isolated physical-input combat tests:
all eight specials in both player slots, two activations per case, followed by
walking, jumping and punching. True Kano/Sonya IDs and ownership remained
stable through 18,260 observed actor fields. The original verifier rejected
194 actual-record mutations. See
`audit_v6266_current_cmd_special_matrix_checked/report.json`.
These were headless two-player tests against Sub-Zero, with samples enabled;
they do not replace the separate ladder, airborne-contact, shadow or audio
fidelity checks. No playable files, builds or release ZIPs changed.

The existing portable playtest ZIP is
`release_v5986_current_playtest/MK2_Kano_Sonya_v5219_CURRENT_PLAYTEST.zip`.
Its standalone dependency checks and video/audio backend startup are recorded
in `audit_v5990_current_portable_terminal_checked/report.json`. This is a
work-in-progress package, not a finished-release claim.

## Verified integration evidence

- `audit_v5445_current_ui_visual_progress`: real Kano/Sonya in both player
  slots; dedicated selection presentation, player numbers/blinking cursor,
  ladder cleanup/icons, first-match sprites, lifebar-name and floor shadows.
  This is bounded current-build UI/pixel/selection-audio evidence.
- `audit_v5322_current_subzero_all_special_body_shadow_progress`: all eight
  special moves, repeated activation, both slots and airborne Square contact,
  including owned body and native shadow evidence in the tested arena.
- `audit_v5698_current_campaign_four_case_matrix_checked`,
  `audit_v5732_current_four_case_ending_pixels_progress` and
  `audit_v5747_current_four_case_ending_audio_progress`: both characters/slots
  naturally clear both bosses, show their own endings and return to attract;
  bounded ending pixel and source-audio checks are separate from all combat.
- `audit_v6236_current_mileena_source_audio_progress` adds current-build
  Mileena-victim native state/effect-delivery/audio checks after the broader
  recent stock-finisher and Sub-Zero checks. It retains the full open scope.
- `audit_v6252_current_friendship_scene_progress` and
  `audit_v6259_current_friendship_audio_progress`: both characters' own
  Friendships in both slots, full visible sequences and source-derived audio,
  including overlapping calls, winner announcements and channel cleanup.

## Still open

Final integrated acceptance remains open: remaining stage-finisher branches,
arena/CPU/KO/overlap art and audio, other victim/finisher/morph/secret/cinematic
coverage, and the combined release regression. Existing campaign/ending passes
must be reused, not rerun merely because the original work-group label persists.
Do not claim full acceptance from a checksum, a single arena or a cold boot.

The current frozen-source inventory is
`audit_v6273_current_native_branch_inventory/report.json`: forty typed guest
tables, the separate Pit payload table, all six original-derived ladder
schedules and eight character-owned CPU special branches. It rejected 127
actual table/consumer/ladder/router corruptions. This is structural evidence,
not automatic runtime acceptance of every branch.

A mixed-CPU case is Sonya's leg grab followed by Square Wave after her own
cleanup but before the victim finishes recovering. The standalone leg verifier
expects an ordinary follow-up and rejects this different continuation. That
original rejection is preserved; it is not, by itself, a gameplay softlock.
`audit_v6281_current_existing_cpu_inventory/report.json` requalifies four
complete standalone CPU leg cycles and all three actual Sonya RNG choices
from the existing enabled/disabled traces, rejecting twenty real record
faults. It explicitly retains both mixed-case rejections and does not claim
full ring-child, CPU leg artwork/shadow/audio or compound-sequence acceptance.

`audit_v6283_current_cpu_leg_square_compound_checked/report.json` separately
qualifies the actual mixed sequence in both existing samples-enabled/disabled
traces: original leg choreography and individual handoffs, the complete
54-field Square rise/flight/fall/landing/cleanup, then a newly set-up ordinary
attack with native 26-point contact and its own grounded cleanup. All-mode
health and live state ledgers cover the sequence and subsequent callbacks;
24 actual-record faults were rejected. Only the standalone Square test's
idle-tail assumption is replaced by this explicit continuation check, not its
move mechanics. This does not certify mixed-sequence artwork/shadows/audio or
every ordinary attack. No playable files, native boots or builds changed.

`audit_v6299_current_kano_cpu_ball_checked/report.json` adds a fresh current
native Kano-versus-Kano CPU match: its naturally chosen ball inflicts 24 damage,
has thirteen rolling fields and all forty-two recoil fields, follows the
original two-body separation limit, lands, and clears both actors' special
states at their distinct recovery points. Whole-match ledgers cover 3,602
physical fields, the earned KO and original round reset; eighteen real faults
were rejected. The observer uses normal buttons and no forced AI choice.
This is bounded motion/pose/state/health evidence, not CPU ball artwork,
shadow/audio or register-tap acceptance. Knife and blade were not reached in
that ball run. The original different-scenario knife rejection and host-check
failures are preserved. Both actual emulator runs ended naturally; the first
selected stock Baraka and is not a Kano acceptance case. No builds or ZIPs
were created. Further CPU checks should vary legitimate human distance/jump
responses, not repeat the same already-verified opening ball sequence.

`audit_v6311_current_kano_cpu_blade_knife_checked/report.json` reuses the later
naturally terminal `audit_v6303_current_kano_cpu_confirm265_ram` match, without
another emulator run. A real one-field selection-confirm variation reached
both CPU branches: blade at frame 1871 and knife at frame 2442. The blade has
all ten authored body poses/38 fields, exact advances, fresh native locks,
26-point contact, both individual ready handoffs and cleared trail pointer.
The physically blocked knife has all 49 parent-body fields, 50 owned-child
fields, original guard/Block query, six-point contact, six impact groups,
individual parent cleanup and native child retirement. All 21 actual-record
faults were rejected. Whole-match ledgers retain 3,602 physical callbacks,
201 native HP stores, 420 source-bound state stores and both natural KOs.

The original two-choke/two-knife scenario is still rejected, not rewritten as
a generic match test. The executed floor-extent and entry-mode assumptions,
plus an adapter error, remain recorded in 6305/6307/6309. The corrected knife
check covers its entire actual lifecycle; unrelated later KO floor changes
are outside that window, while the state/HP inventory remains whole-match.
Its actual entry occurs during the native mode-7 to mode-2 round handoff;
all subsequent knife callbacks through retirement are verified as mode 2.
This is motion/pose/contact/state evidence, not complete attached-effect
allocation/retirement taps, raster, floor-shadow or audio acceptance. Those
checks and the broader integration/release work remain open. No playable
files, builds, ZIPs or raw media changed during this qualification.

`audit_v6328_current_cpu_blade_knife_body_shadow_checked/report.json` adds
112 actual drawing fields around those same naturally chosen blade/knife
moves. The additional read-only capture in 6317 preserves every original
input, native RNG, state and HP observation from 6303. All 456 fighter body
components and 13,325 native floor-shadow copies are independently bound to
the compiled original/imported assets, true owners, camera, floor, compressed
source rows and original shadow pen/cadence. Both entry frames and recovery
tails are included; all 26 actual-record faults were rejected. The original
missing mode-7 post-pose binding and subsequent host adapter errors remain
recorded. The corrected check binds that actual refill field's post pose and
world position to its body/shadow publications, rather than dropping it.
This does not certify blade-trail or knife-effect raster, whole RGB erasure,
audio, every arena/CPU continuation or the finished port. No build/ZIP/raw
media was created. The one additional emulator capture ended naturally.

The root `PLAY_LATEST_TEST_BUILD.cmd` had still pointed to a retired v737
folder. It now forwards to the canonical current launcher. Its byte-identical
old contents are recoverable in `launcher_history_v6318`; explicitly versioned
old launchers, including v1250, remain unchanged. The actual repaired alias
passed native ROM validation and all sixteen voice-asset checks from outside
the workspace, with current saved settings unchanged; see
`audit_v6322_current_latest_launcher_checked/report.json`. Normal current-CMD
gameplay remains covered by 6241/6266. The ordinary v1250 game observed during
the prelaunch check was left alone, not terminated or used as current evidence.

Fourteen compiled candidate folders are retained for current/historical
dependencies. `v5219` is a version/checkpoint label, not 5,219 compilations.
Use current binaries in place; do not create new build trees or raw media for
ordinary verification. See `WORKSPACE_CLEANUP_CURRENT.md` for retired data.

`audit_v6344_current_cpu_blade_allocation_checked/report.json` now verifies
the actual current CPU blade's complete native sprite-pool lifetime, not
only a cleared parent pointer. The blade is popped from the original pool,
attached to its true Kano Main at frame 1871, follows all ten body/effect
poses for 38 fields, and executes original cleanup, retirement, pool push
and detach at 1909. Both immediate post-retirement fields have no render-list
membership and retain native free-list membership. All 3,314 whole-match
free-head half-stores remain source-bound; no address normalization is used.
All 24 actual-record faults were rejected, and the full original motion,
HP/state/native-choice and physical-input chronology remains unchanged.

The first added observer incorrectly overwrote its completed blade context
when the later knife used the same Main field. That actual trace and its
rejection remain in 6337/6339. The successor fixes observer bookkeeping only:
it records the first matching blade-object detach once, and retains every
later Main write under a separate tag. All eight later writes are checked:
four original round-reset zero-fill stores and the distinct knife object's
full publication/clear transactions. The earlier helper namespace error,
which occurred before native launch, remains recorded in 6335. Both actual
emulator runs exited naturally; neither was restarted or forced into a move.

This adds effect allocation/attachment/retirement evidence, not full blade
or knife effect raster, palettes, whole-screen erasure, audio, every arena or
the finished port. Those checks and the broader integration/release audit
remain open; the full goal stays active. No playable source, executable,
ROM, release ZIP or build folder changed. The complete native guest was
compared in RAM; RGB callbacks were hashed, not accepted as effect-raster
proof. Neither raw buffer was retained. The original qualified
allocation model and its assembly/combat/lifecycle dependencies also remain
byte-identical to the earlier 2912 qualification.

`audit_v6359_current_cpu_effect_render_checked/report.json` now adds the
complete continuous blade/knife rendering check for that current CPU sequence:
641 consecutive fields, 65,125,600 exact RGB pixels, original native queue,
DMA/shift/flip/clear operations, source-derived artwork and complete palettes.
All ten blade-trail phases and the knife's introduction, flight and impact
are visible with their real ownership and camera projection. Both effects
erase normally, including the intervening KO/round reset and recovery tails.
This uses one initial VRAM base; comparison targets never seed the replay.
Eight actual art/ownership/projection record faults are rejected.

The original capture's failed flag remains intact in 6349: its host collector
hashed numeric allocator half-stores as well as graphic data, so its final
literal-text comparison rejected an otherwise identical chronology. The
successor checks all 3,326 original numeric words against their exact SHA256
digests, with all other characters and every input/AI/RNG/HP/state/pool row
unchanged. It does not normalize addresses, discard rows or change gameplay.
The premature host read and overly strict same-field retirement and incorrect
single-frame projection assumptions remain recorded in 6351/6355/6357.

The actual last blade publication precedes native retirement within frame
1909; its committed field displays at 1910 and clears at 1911. Original
single-frame drawing bypasses multipart descriptor offsets. Both facts are
source-bound, not substitute offsets or relaxed cleanup rules.
`audit_v6361_current_cpu_effect_retirement_order_faults/report.json` rejects
all three real publication/retirement-order faults, including a stale draw
after retirement within that same field.

The native capture exited naturally with no observation errors. Guest, GFX,
VRAM and RGB buffers stayed in RAM; only digests and compressed logs remain.
No playable source, executable, ROM, build folder or ZIP changed. This closes
blade/knife artwork, palette and full-screen erasure verification for this
sequence, not CPU-move audio, every arena/continuation or final port acceptance.
The full integration/release goal remains active.

`audit_v6368_current_cpu_blade_knife_audio_ram/report.json` and
`audit_v6373_current_cpu_blade_knife_audio_checked/report.json` now qualify
the same naturally selected current CPU blade/knife sequence's full sound
window: 584 consecutive sound updates and 560,640 exact stereo sample frames.
Every sample equals the original native DAC/resampler plus the source-timed
Kano winner clip, with original float mixing, gain and final conversion.
There is no waveform fit, timing search, trimmed callback or raw-media file.
Both startup and terminal complete original sound-ROM inventories match.

The blade swish/cut and knife release are bound to actual MOVI/call bytes,
native caller addresses and true Kano owners. The complete victim grunt
selector retains actual victim17 and its physical Main role, not Liu Kang.
All 56 native packets, 112 port words and 112 actual sound-chip reads are
checked in order. Every one of 8,176 precise channel states and 8,946 video
channel states matches original playback arithmetic and finite retirement.
Eight real cue/owner/packet/delivery/channel faults are rejected, alongside
the independent raw-PCM, mix-operation, DAC and whole-sound-ROM fault suites.

The initial helper module/local-name collision was prelaunch only (6364).
The first actual capture exited naturally but its host gate expected a video
snapshot before the audio entry occurred (6366). The corrected frame range
is1872..2510; all 584 audio callbacks remain. Native sample EOF clears its
source pointer/number but retains length and completed position. That exact
bookkeeping and the preceding selection clip's repeated-double endpoint are
source-derived, not integer approximations. The source-slice and channel
preflight failures remain recorded in6367/6370. The corrected full capture
also exited naturally, and its waveform passed before the independent6373
delivery/channel check. Host repair cannot discard retained RAM buffers.

This closes CPU blade/knife sound verification for this Kano mirror sequence,
not all CPU moves, mirrors, arenas or final integrated release acceptance.
Both actual native audio runs ended with no transport errors. No playable
source, executable, ROM, build folder or ZIP changed; verification artifacts
are losslessly compressed. Reuse these results and the earlier campaign/UI
passes. Broader Sonya CPU/effect cases and the full remaining integration
scope stay open.

`audit_v6378_current_cpu_ring_render_ram/result.json` and
`audit_v6382_current_cpu_ring_render_checked/report.json` now qualify an
actual full-hit Sonya CPU Ring Toss on the exact current v5219 executable and
payload. The whole original physical-input sequence uses boot613,
confirm264, original approach and retreat; no RNG, character or health write
forces the contact. Sonya remains native18 and the human victim remains17.
The ring is born at2092, deals the native unblocked22-point hit at2098,
retires at2126 and leaves Sonya ready at2127. The complete earlier physical,
AI/RNG, HP and state chronology is unchanged. Whole-match ledgers retain
incomplete and interrupted continuations rather than relabeling them complete.

All80 consecutive displayed fields2078..2157 match the independent original
CPU/DMA/shift/scanout renderer:8,128,000 exact RGB pixels,424 full palette
checks and one initial VRAM base, never comparison-target reseeding. The
independent donor-art comparison covers86 original pieces; native FIFO/cache
and camera/flip/source projections cover429 actual publications and1,211
cache parts. All five release body poses, all seven impact poses and both
flight poses actually executed before this short collision are visible.
This hit does not exercise all four cyclic flight poses. Thirty displayed
post-retirement fields contain no ring pixels. All7,225 owned native
compressed floor-shadow copies pass the unchanged source-row/copy-cadence
check; body floor anchors and complete observed RGB are separately checked.
That is bounded sequence evidence, not universal shadow geometry approval.

The preserved6380 checker failure exposed a missing cross-check for a mutated
unowned DMA source. The6381 successor adds source/command/frame equality to
the independent passive register observations for every native DMA, retaining
the complete original positive and all seven real record-fault tests. All
seven now reject and the full positive restores. The two actual VRAM/RGB
pixel mutations also reject. No gameplay code was changed for this repair.

The earlier5324 jump-on-launch CPU Ring was a miss, not this full-hit proof.
Its miss/mirror branches and the current Ring's full source-audio check remain
open, alongside compound CPU leg/Square art/audio and the broader final
integration/release scope above. The actual capture process165876 exited
naturally with no observation errors; this independent check needed no new
emulator run. Guest, GFX, VRAM and RGB stayed in RAM. No playable source,
executable, ROM, build folder or ZIP changed. Keep these finite passes and
the existing UI/campaign/ending results; the full goal remains active.

`audit_v6385_current_cpu_ring_audio_ram/report.json` and
`audit_v6387_current_cpu_ring_audio_checked/report.json` close the source-audio
gap for that same current full-hit Sonya CPU Ring sequence. One normal
physical-input run, process156164, exited naturally with no native warnings
or host transport errors. All physical/AI/RNG/HP/state/child/guard rows match
the already-qualified6378 capture exactly; no move or RNG choice was forced.

The entire639-field audio window2077..2716 contains585 consecutive sound
callbacks and561,600 exact stereo sample frames. Every sample equals the
original float32 DAC/resampler/cache plus the source-timed Sonya winner clip,
with original route/mix gain and final conversion. Actual and predicted PCM
SHA256 is9A9F68107848F6156294EA82EAC740478395BE0AD3037C5D1BED5CB1107B8F2C.
Both complete12MiB original sound-ROM startup/terminal inventories match.
There is no waveform fit, timing/gain search, callback omission or raw file.

The independent cue gate binds release5 to true native Sonya18 and her
physical Main; impact62 belongs to the independently allocated Ring child,
not the parent. Both producers' complete literal/call/helper instructions
are checked. The complete five-step hit-grunt chain uses actual Kano17 and
physical Main role1, never Liu Kang. All20 native packets,40 port stores and
40 original sound-chip reads match in order. All8,190 precise channel states
and8,946 video channel states follow the original repeated-double clock,
including the earlier Kano selection endpoint,100 consecutive Sonya winner
updates and the complete inactive tail with retained native EOF bookkeeping.

Ten actual cue/owner/victim/packet/port/delivery/winner/channel faults reject,
as do the four raw-PCM, four source-mix, four DAC and eight whole-ROM faults.
The complete native positive restores after the independent semantic faults.
The independent checker used no second emulator run. This closes Ring-hit
audio for this finite CPU/victim/arena sequence, not the current miss/mirror
branches, compound CPU leg/Square art/audio or final integrated acceptance.
No playable source, executable, ROM, build folder or ZIP changed. Raw audio,
guest and ROM carriers stayed in RAM; only compressed logs/digests and finite
results remain. Existing campaign/UI/ending passes remain valid evidence and
must be reused. The original full natural-integration goal stays active.

`audit_v6390_current_cpu_ring_mirror_render_ram/result.json` and
`audit_v6392_current_cpu_ring_mirror_render_checked/report.json` add actual
current Sonya-versus-Sonya CPU Ring block/chip rendering. One current native
run, process164876, exited naturally with no observation errors. Both physical
slots retain true18, distinct owners and native normal/alternate palettes.
The complete original physical/AI/RNG/HP/state/child/guard chronology matches
the older3467 reference; that older build is not substituted for this actual
current executable, whole guest or GFX. Three complete native leg continuations,
the earned KO and original round reset remain in the whole-match ledgers.

The Ring starts at2945 during the genuine mode7-to-live boundary, is born
at2960, makes physically blocked contact at2974 for native6-point chip,
leaves its parent ready at2995 and retires its own child at3002. All87
consecutive fields2946..3032 match the independent original continuous
CPU/DMA/shift/scanout renderer:8,839,200 exact RGB pixels,477 complete palette
checks, one initial VRAM base and no target reseeding. Independent original
donor art covers86 pieces. All five release body poses, all four cyclic
flight poses and all seven impact poses are actually visible in this branch.
The native FIFO/cache/camera/flip check covers481 publications,1,311 cache
parts and15,832 independently register-bound DMA events. All9,645 owned
compressed floor-shadow copies pass original source-row and copy-cadence
checks. This is finite scene/anchor/row evidence, not every-arena geometry.

The native last child publication precedes retirement within3002. Its actual
DMA is committed on displayed field3003; all29 following displayed fields
through3032 are empty of Ring pixels. The entire original observer window is
retained: max(parent recovery,child retirement)+30. A cross-branch assertion
requiring30 fields *after* the committed draw would miscount that original
window. The checker instead binds the last visible field to its actual DMA
and checks every remaining field through the unchanged native window end.
No capture was shortened or comparison target used as a replay anchor.

All seven actual floor/camera/cache/source/owner/late-publication/shadow faults
reject, plus an actual last publication moved after same-field retirement.
Both VRAM/RGB target mutations also reject; the complete positive restores.
No second native run was needed for the independent check. No gameplay code,
playable executable, ROM, build folder or ZIP changed. Guest/GFX/VRAM/RGB
carriers stayed in RAM, with only bounded compressed logs/digests retained.
Mirror audio, the miss branch, compound CPU leg/Square art/audio and the
broader original integration/release scope remain open. The full goal stays
active; keep and reuse these passes alongside existing UI/campaign/ending
evidence.

`audit_v6403_current_cpu_ring_mirror_audio_ram_checked/report.json` and
`audit_v6407_current_cpu_ring_mirror_audio_checked/report.json` close the
full-current-mirror source-audio gap for the6390/6392 physical sequence.
Actual native process155308 exited naturally with code0 and no transport
decode errors. The original6395 capture had already fully drained; every
subsequent qualification used that same RAM carrier, with zero native
replays, builds or raw audio/ROM files. Its complete physical/AI/RNG/HP/state
chronology matches6390, including all three legs, KO2659, reset2848 and the
blocked Ring at2974. Keep the existing finite render/shadow proof unchanged.

All1,645 consecutive50Hz sound callbacks and1,579,200 stereo sample frames
match the complete original native float32 DAC/resampler/cache and source
sample mixer. Actual and predicted PCM SHA256 is
61AFF930DE49E2F2CFB049BB91F99E3D3A677879515B47249DADD321EE140142.
The whole first-live-to-terminal window1823..3623 is retained, including
the cached first value, original last callback and complete inactive tail.
Both complete12MiB loaded original sound-ROM checkpoints match; the four
raw-PCM, four source-operation, four DAC and eight ROM counterexamples reject.
There is no gain/timing fit, offset search or omitted field/sample.

The actual first channel12 callback retains an already-playing Square Wave
launch voice:48kHz,45,512 source samples, position1,513. Native samples.cpp
assigns first-load source_num from the prior source length, so its recorded
FFFFFFFF does not itself mean silence. The full source clip reaches EOF.
The compiled source routes this channel at.70; the.30 set_volume applies to
announcer channel0, not this Square channel. Sonya's winner marker occurs at
2702 and has the original channel0.70*.30 effective gain. The entire mixed
waveform, not a correlation or enabled/disabled difference, confirms both.

Three executed host assumptions were wrong and remain preserved:6395's
idle-channel admission,6396's first-video/PCM boundary, and6398's omission of
the native60Hz owner timer's playing()/stream update. The first video at
33.32307275 precedes the first PCM callback33.34 and has source position553;
the actual first DAC header supplies preceding sound clock33.32. Later
video positions include original60Hz owner updates between50Hz PCM callbacks.
The one-source-sample start-clock interval resolves the owner-timer index
unambiguously at every recorded video field; no launch marker before the
window is invented.6400's wrong Square gain/full waveform rejection is also
preserved, as is6404's host import-reference error. Successor checkers correct
these source-model mistakes without changing the game or capture bytes.

The independent mirror gate checks all23,030 precise14-channel states and
25,214 video14-channel states, the preceding original Sonya selection EOF,
initial Square clock/EOF and100 consecutive winner updates/retirement. It
binds first-live audio to the actual CPU Square actor/Main and true18, not
the later Ring parent. Release5 belongs to the Ring parent; native blocked
impact63 belongs to its independently allocated child; block-victim cue16
belongs to the true Sonya victim. The original helper adds the block bit to
base62, and this blocked contact has no unblocked Ring-hit grunt. Every
observed packed female victim dispatch chain uses actual18, not Liu Kang or
a male/role proxy. All88 native packets,176 full-word port stores and176
original-chip firmware reads match in order. Twelve actual record faults
reject, and the complete positive restores. Saved per-channel gain snapshots
are not claimed; gains are bound by compiled source and exact PCM equality.

The retained RAM carrier was released only after the full PCM proof was
saved. No playable source, executable, ROM, build folder, launcher or ZIP
changed. This closes audio for this finite mirror/block/match branch, not
the missed Ring branch, compound CPU leg/Square art/shadow/audio, every-arena
move-phase coverage or the full integration/matched-final-release scope.
The original full natural-integration goal remains active; reuse the current
UI, campaign, ending and completed finite move evidence.

`audit_v6413_current_cpu_ring_miss_render_ram/result.json`,
`audit_v6415_current_cpu_ring_miss_render_checked/report.json` and
`audit_v6417_current_cpu_ring_miss_phase_checked/report.json` add current
native missed-Ring lifecycle, full-scene art and floor-shadow acceptance.
Actual native process175204 exited naturally with code0, empty stderr and
no observation errors. The original5324 physical jump-on-launch/close-guard
inputs are unchanged. The whole physical/AI/RNG/health/state/choice/Square
chronology matches that earlier current run exactly; no CPU choice, move,
health, position, stage, register or guest value was forced. All original
match and compound leg-to-Square-to-ordinary contracts remain in the proof,
including the separately preserved standalone-leg contract rejection.

The native Ring starts1879, creates its independent child1894, misses without
impact state or damage, and retires1908. All14 actual child fields and five
three-field cyclic flight-group publications are checked against original
source geometry, true18/physical ownership, exact fixed-point motion and
retirement. The projectile retires before the independent parent recovery
at1929; the parent retains all five release poses, holds and11 original
action/lock stores, then resumes the ordinary action with both locks cleared.
No Ring-owned health change or Ring-hit guard branch is present. Fifteen
actual parent/child/flight/birth/retirement/lock/callback faults reject, and
the complete original match/phase positive restores.

All80 consecutive displayed fields1880..1959 match the independent original
continuous CPU/DMA/shift/scanout renderer:8,128,000 exact RGB pixels and311
complete palette checks. There is one initial VRAM base; comparison targets
never seed the replay. Both real target-pixel mutations reject. The full
source-art/cache/camera/flip/FIFO gate checks315 owned publications,637 cache
parts and12,368 independently register-bound DMA events, including scenery
and shadows. All five release poses and all four actual flight poses are
visible, with no invented impact publications. The hit-specific minimum
child-draw count is not a miss contract: this short missed child has12 owned
draws. Every actual FIFO publication, source piece, projection and dispatch
is still checked; positive coverage requires all four flight poses, not an
arbitrary hit-length count. All86 original donor-art pieces are independently
checked. No physical pointer replacement occurs during the retained window.

All7,247 owned compressed floor-shadow copies pass the original source-row
and copy-cadence checks for Kano17 and Sonya18. All50 retained display fields
after retirement+1 are empty of Ring pixels. Eight real floor/camera/cache/
DMA/owner/stale-publication/shadow/retirement-order faults reject; the full
positive restores. Both independent checkers reuse the same terminal capture
and require no second game run. Guest/GFX/VRAM/RGB stay in RAM; only bounded
compressed logs, digests and results remain. No playable source, executable,
ROM, build folder, launcher or ZIP changed.

Miss source-audio, compound CPU leg/Square art/shadow/audio, broader arena
move-phase coverage and final integration/matched release remain open. This
is a finite miss-branch proof, not universal move or whole-port acceptance.
Keep all current hit/mirror/UI/campaign/ending passes and the original full
natural-integration goal active.

Storage disclosure for this miss capture:
`audit_v6421_current_miss_scratch_snapshot_retired/report.json` records one
legacy3303 Square-choice screenshot at2994, outside the accepted1880..1959
Ring render window. It wrote54,551 PNG bytes despite the collector's inherited
zero-raw-files count. That inherited count is not accurate for this run; the
executed collector/result remain unchanged, with this explicit correction.
The file was not a model input or pinned proof. Its SHA256/size/source were
recorded before precisely retiring that single scratch PNG. Every accepted
source, capture, guest, executable, payload and model hash remained unchanged.
The scratch image is not recoverable from this folder; its digest remains.
The retained evidence has no raw image/audio/guest/GFX/VRAM/ROM files. No second
native run was used to correct this storage issue. Route3303's screenshot
through the existing RAM sink in any future observer; do not edit this
executed/pinned6410 capture harness or the original physical input driver.

`audit_v6427_current_cpu_ring_miss_audio_ram/report.json` and
`audit_v6429_current_cpu_ring_miss_audio_checked/report.json` close the source
audio gap for the current missed-Ring sequence. Actual process173684 exited
naturally with code0, empty stderr and no transport errors. Its complete
physical/AI/RNG/HP/state/guard/choice/compound trace matches6413 exactly.
The original inputs and both true physical character identities remain
unchanged. All77 original physical/choice snapshots now travel through RAM;
no scratch PNG is created or retained. The snapshot label and frame come
from the actual original callback, not an invented timing value.

The750-field audio window1880..2629 and all686 consecutive50Hz sound updates
include the actual miss, parent recovery, earned KO2379, Sonya winner marker
2420, complete source-clip EOF and original round reset2566. The window ends
before the separate Bicycle launch2663; that later move's audio is not
claimed. All658,560 stereo sample frames equal the entire original float32
native DAC/resampler/cache plus original source-timed Sonya winner mix.
Actual/predicted PCM SHA256 is
43100266F973916006A5E8BCD6BD709D270D0EC31B839A4817D44D48A768F0AB.
No first/last callback, cached speaker value, winner tail or interior sample
is removed. There is no waveform fit, gain/time search or clipping workaround.
Both complete12MiB loaded original sound-ROM checkpoints match, and the
four raw-PCM, four source-operation, four DAC and eight ROM faults reject.

The independent source-cue gate binds release5 to native Sonya18 and her
actual physical actor/Main. There is no Ring impact62/63 producer, no Ring-hit
victim grunt and no hidden child-owned sound during the missed projectile's
actual lifetime. The original hit/miss/voice/queue/packet code is checked;
the port's existing impact-alignment CALLA target is separately bound to the
exact compiled FFfc2800 helper, with every other byte unchanged. The broader
stock-byte assumption in an initial host preflight was too broad for that
already-qualified authored pointer; no playable source or capture changed.

All19 actual later victim-voice chains are complete, source-owned and use
Kano17/physical male role1 or native Sonya18/female byte18, never Liu Kang.
All55 native packets,110 full-word sound-port stores and110 original-chip
firmware reads match in order. All9,604 precise channel states and10,500
video channel states follow original sample selection, repeated-double
position bits and native retirement, including the prior Kano selection EOF,
100 consecutive Sonya winner updates and complete inactive tail. No saved
per-channel gain snapshots are claimed; source gains and exact PCM are bound.
Eleven real cue/owner/proxy/false-impact/voice/packet/port/delivery/winner/
channel faults reject; the entire native positive restores afterward.

The first observer startup, process170192, actually exited3 before any live
fight or audio callback because its extracted script could not see a local
read helper. `audit_v6424_current_cpu_ring_miss_audio_ram` and its executed
6422/6423 sources remain rejected and unchanged. The6425/6426 successor passes
that local dependency explicitly, then captures a fresh actual run only
after the failed process is confirmed terminal. It is not a restart after an
observation timeout, a gameplay softlock or a patched ROM. The accepted run's
full RAM carrier was released after its complete waveform result was saved.
No playable source, executable, ROM, build folder, launcher or ZIP changed.

This closes the finite missed-Ring art/shadow/phase/audio branch alongside
the already-accepted current full-hit and mirror-block Ring branches. Compound
CPU leg/Square art/shadow/audio, CPU ball art/shadow/audio, broader stage/
victim/arena integration and final matched-release regression remain open.
Keep the full original natural-integration goal active and reuse existing
UI/campaign/ending/finisher results, not new runs solely to change labels.

`audit_v6439_current_cpu_compound_render_ram/result.json` and
`audit_v6436_current_cpu_compound_render_checked/report.json` now qualify the
current naturally selected CPU Sonya leg-grab -> Square Wave -> ordinary
attack as one uninterrupted visual/floor-shadow sequence. Native process
159440 exited naturally0 with empty stderr and no observation errors. Every
original physical input, AI/RNG choice, round, health, state and Square record
matches the existing5324 trace. Neither playable source nor guest/actor/RNG/
HP/controller policy is changed; native Kano17 and CPU Sonya18 retain their
actual physical actor/Main pointers throughout.

The third leg enters2920 and releases2976. Sonya's own leg cleanup2986 precedes
the Square entry2994; Kano's victim recovery3023 overlaps Square naturally.
Square lands3044 and regains3048; the following ordinary attack starts3049,
does26 native damage3055 and regains3093, with clean callback3094 and complete
tail through3124. The original standalone leg idle-tail rejection remains
unchanged: this is an explicitly qualified different continuation, not a
silently relaxed standalone contract.

All206 consecutive400x254 screens2919..3124 equal the unchanged3642 independent
CPU/DMA/shift/VRAM/scanout model,20,929,600 exact RGB pixels and722 whole body
palette checks. One original initial VRAM base is used; later VRAM/RGB targets
are comparisons only, never replay seeds. Both actual VRAM/RGB-bit faults
reject. The whole native FIFO inventory and every32,653 DMA command/source
bind independent live register observations. Both complete native bodies are
checked in every207 actual drawing fields2918..3124:726 pre-clip candidates,
726 publications,1,396 cached composite-part observations and726 source-bound
camera/origin/flip projections. All62 observed poses,109 original donor-piece
references/108 unique pieces retain exact original dimensions, pivots,
commands and independently decoded MK3 sprite indices.

All414 original shadow eligibility calls cover both actual physical actors
in every drawing field. All725 eligible complete source components and19,020
compressed floor-shadow copies retain original packed row stepping, duplicated
final rows, absolute world/camera/native floor geometry, original instruction
cadence and black pen. Kano134/Sonya135 floor anchors are unchanged. Ineligible
bodies generate no invented component. Eleven real actual-record ground,
camera, body-source/origin, DMA/ownership, shadow eligibility/source/position
faults reject; the complete positive restores afterward.

The earlier process157940 (`audit_v6434_current_cpu_compound_render_ram`)
also exited0 and modeled204 full screens2921..3124. Its observed leg-entry
trigger was later than that frame's native body publication, so it was not
used to claim complete entry body/shadow provenance. Its executed6432/6433
sources and actual results are retained unchanged. The6437/6438 successor
starts passive observation two fields earlier, covering the entry without
changing gameplay. This second run addresses a real evidence gap, not an
observation timeout or a new ROM build. Initial unpinned host preflights also
corrected4-digit/8-digit numeric text formatting without changing values,
and added the independent shadow-DMA source binding before qualification.

Every77 legacy physical/choice snapshot is routed through RAM. No PNG,
guest/GFX/VRAM/RGB/PCM/WAV dump, new build, ROM copy or ZIP is created. This
closes this finite chained CPU visual/ground/floor-shadow/cleanup gap; complete
source audio for the chain, CPU ball art/shadow/audio and final combined
integration/release acceptance remain open. Existing native UI, campaign,
ending and finisher passes remain reusable. The full goal stays active.

`audit_v6447_current_cpu_compound_audio_checked/report.json` now qualifies
source-exact audio for the same original5324 natural human Kano17/CPU Sonya18
match, first live1823 through unchanged physical exit3623. Native process27396
exited naturally0, with empty stderr and no host decode errors. Every original
physical input, AI/RNG choice, health, state, round and compound-Square row
equals the already accepted6439 run. All77 legacy snapshots stay RAM-only.
The complete leg -> Square -> ordinary choreography remains independently
qualified; its prior standalone idle-tail rejection is not erased or relaxed.

Every actual1,579,200 stereo frame across1,645 consecutive50Hz callbacks equals
the entire unchanged native DAC float32 resampler/cache plus independently
retained donor clips, original repeated-double interpolation/terminal-fill,
native source-port clocks and compiled speaker routes. Complete PCM SHA256:
8053B527A86A41D102DAE8B9463852583E30F1F0C1368E8E88C4A429A6AA904B.
Both Sonya winner markers2420/3605, successful Bicycle launch/cry2663 and
Square2994 are represented; no callback, first cached sample or tail is trimmed.
Battle channels12/13 retain .70 routing; announcer0 retains .70*.30. No fitted
gain, onset, correlation-only acceptance or saved gain snapshots are claimed.

All43 actual native victim-voice chains retain true Kano17/male physical role1
or Sonya18/female byte18 ownership, never a Liu proxy. All three leg startups
1954/2117/2920 use original randomized unvoiced swings; contacts1964/2127/2930
use native impacts and actual Kano victim grunts. Ordinary contact3055 uses
its own native impact. The original source has no extra cue at the leg's later
damage/release store; a host preflight stopped incorrectly assuming one there.
Entire native sound helpers and authored launch MOVI/absolute-port stores bind
actual reconstructed guest bytes. All135 packets,270 full-word port writes
and270 original-chip firmware reads match in order, including native FFxx bytes.

All23,030 precise sample states retain exact repeated-double position bits;
all25,214 video states retain native distinct channel streams,50Hz output and
60Hz owner-timer updates. The Bicycle cry stream is queried only after the
launch stream returns false, preserving the source short-circuit rather than
assuming every channel updates at every timer tick. All three battle clips
and the first winner reach source EOF and remain retired. The second winner
starts3605 and is legitimately still playing when the original test exits3623;
that clip's EOF is not observed or claimed by this finite run.

The executed6442/6443 capture and actual6445 failure remain unchanged. Its
initial host gate incorrectly required all channels idle at physical exit.
The same fully drained RAM carrier was qualified by6446 without another native
boot, forced audio flush, altered game/input state or extended physical boundary.
Twelve actual cue/ownership/voice/packet/port/DSP/winner/channel record faults,
nine raw PCM/source-operation faults, four native DAC faults and eight whole
sound-ROM faults reject; the complete positives restore afterward. Both whole
original12MiB sound-ROM images remain verified, without raw files on disk.

`audit_v6449_current_cpu_compound_audio_storage/report.json` verifies exact
lossless compression of16 finite evidence/source files:2,835,099 logical bytes,
790,415 allocated bytes,272 protected pins unchanged. The host RAM carrier is
released and the authoritative native process census is empty. No playable
source, executable, ROM, launcher, build folder or release ZIP changed. The
existing portable ZIP remains4D14CE6DD8F3D878BA02EDB112BAF43988A3E28B37EF1AC2FB7CE54F89E8670C.

This closes the finite compound CPU source-audio gap alongside6436's full
art/raster/ground/floor-shadow result. Kano CPU ball full art/shadow/audio,
remaining evidenced broader integration gaps and final combined matched-release
acceptance are still open. Reuse existing UI/campaign/ending/finisher results;
do not repeat completed runs merely to change labels. The full original goal
remains active. Previous goal turn: no progress (acknowledgement only). This
turn: progress (actual whole mixed match audio and cleanup qualified).

`audit_v6453_current_cpu_ball_render_ram/result.json` and
`audit_v6455_current_cpu_ball_render_checked/report.json` now qualify the
current naturally selected CPU Kano ball hit as one complete finite native
visual/floor-shadow branch. Native process118244 exited naturally0 with empty
stderr and no observation errors. The entire original6293 human Kano17/CPU
Kano17 physical input, AI/RNG choice, round, health, state and continuation
trace is identical. The whole6298/6299 source-derived motion contract is reused
unchanged: entry1814,24-damage contact1827,13 rolling fields,42 rebound fields,
native separation limit1851, landing1869, own regain1873 and victim regain1888.
No CPU/RNG/health/actor/game-state write or prescribed move is introduced.

Every105 consecutive400x254 screens1814..1918 matches the original3642 native
CPU/DMA/shift/VRAM/scanout algorithm:10,668,000 exact RGB pixels and334 complete
body-palette checks. Only the explicit actual Kano17/Kano17 tuple differs from
the mixed-character model; no raster kernel or palette dispatch is changed.
One initial VRAM base is used, never a later comparison target. Both actual
VRAM/RGB-bit counterexamples reject. All seven original roll poses reach
visible modeled screens; both native body masks remain visible in every screen,
minimum human1,806/CPU1,241 pixels, with no invented persistent sprite flag.

The passive window starts1813, the native precombat mode7 field immediately
before mode2/entry1814. The ball is chosen before the legacy pair observer's
first live callback1815, so214 independent read-only physical actor/Main/ID/
floor bindings cover both bodies at every107 callback1813..1919. This closes
the pre-entry provenance gap without replacing or supplementing any original
control/phase rows. Host preflights explicitly adapted the one mode7 pre-entry
field and both FIFO/DMA identity/anchor checks to the actual Kano mirror;
the accepted native capture was not rerun or modified.

All339 complete pre-clip candidates,339 publications,631 cached parts and339
source-bound camera/origin/flip projections retain native physical ownership.
All14,574 DMA commands/sources bind independent actual register observations.
All36 observed body poses/60 original donor pieces retain exact original
dimensions, pivots, command words and independently decoded MK3 pixel indices.
No component is hidden by classification or falsely clipped away.

Every212 native shadow eligibility call covers both bodies in every106 drawing
field1813..1918. All340 eligible complete components and7,638 black shadow
copies retain original compressed row stepping/duplicated last row, native
instruction cadence, world/camera/display registers and absolute floor math.
Both Kano floor anchors remain134. Every eligible composite has all components;
ineligible bodies have none. Thirteen real body/ground/camera/source/DMA/
ownership/shadow/pre-entry/visibility record faults reject, and the complete
positive restores afterward. This is actual source/geometry/raster acceptance,
not a hand-picked screenshot or generic gameplay-stability substitution.

`audit_v6457_current_cpu_ball_render_storage/report.json` verifies exact
lossless compression of18 evidence/source files:1,468,793 logical bytes,
1,072,961 allocated bytes,415 protected pins unchanged. Every42 legacy
snapshot callback remains RAM-only; no raw guest/GFX/VRAM/RGB/PCM/WAV file,
new build, ROM copy or ZIP is created. Both native and host jobs are drained;
the authoritative native process census is empty. Playable source, executable,
launcher and the existing portable release ZIP remain unchanged.

This closes the finite CPU ball full art/ground/floor-shadow/visual recovery
gap. CPU ball source audio, the remaining evidenced broader integration gaps
and final combined matched-release acceptance remain open. Existing accepted
UI/campaign/ending/finisher and compound audio results remain reusable. The
full original natural-integration goal stays active. Previous goal turn was
progress (compound audio); this turn is progress (complete native ball visual
and absolute floor-shadow qualification), not a new build or a status-only turn.

`audit_v6462_current_cpu_ball_audio_checked/report.json` now qualifies the
whole source-exact audio window for the same original6293 naturally selected
CPU Kano17 versus human Kano17 ball match. Native process169328 exited
naturally0 with empty stderr and no observation errors. The full original
physical/AI/RNG/HP/state/round chronology is unchanged from6453. Both actual
physical actor/Main roles have independent passive bindings throughout
1813..3615; no identity, health, CPU choice or game-state write is introduced.

Every1,580,160 stereo frame across1,646 consecutive50Hz callbacks equals the
entire native DAC float32 resampler/cache plus the original Kano winner clip,
source-port onset, repeated-double interpolation/terminal-fill and compiled
speaker routes. Complete PCM SHA256:
93F39FC6A8E06F8CF0E20258338F23A192B315AD4C66E964BE9E16B2DF44512F.
All79 packets,158 full-word sound-port stores and158 original ADSP firmware
reads match in order. All23,044 precise and25,242 video sample-channel states
retain exact source positions, all fourteen channels and complete cleanup.
The winner starts2418, runs100 complete sound callbacks, reaches source EOF
and remains retired through the unchanged physical terminal3615.

Ball contact1827 uses original impact19 and the actual victim's male grunt;
victim floor contact1850 uses original1F and the rolling actor's landing1869
uses original1E. Entire original reaction/landing/queue programs are bound to
the reconstructed guest, not only selected literals. All19 complete native
voice chains retain real Kano17 owners; physical roles1 and2 select their
source-defined packed bytes independently, not by the shared mirror identity.
The current authored ball has no startup sound producer. This verifies its
whole current audio path; independent MK3 startup-cue parity is not claimed.
Eleven actual cue/owner/role/packet/port/DSP/winner/channel faults, four raw
PCM faults, four source-operation faults, four DAC faults and eight whole
sound-ROM faults reject; complete positives restore afterward.

The executed6458/6459 collector and6460 failure remain unchanged. Its host
gate incorrectly required the final50Hz audio callback to be within one
video frame of exit. Native video ticks are18.27925ms, while sound ticks are
20ms: actual origin33.14028025s, all scheduled sound callbacks33.16..66.06s,
and natural exit66.07948875s. The next sound tick66.08s is after exit. The
same fully drained RAM carrier was qualified by6461 using every scheduled
sound-clock tick between origin and exit; no callback was dropped or added,
and no native replay, extended boundary or forced flush was performed.

`audit_v6464_current_cpu_ball_audio_storage/report.json` verifies exact
lossless compression of15 evidence/source files:3,105,618 logical bytes,
768,878 allocated bytes,259 protected pins unchanged. The RAM carrier is
released; both host and native jobs are terminal and the authoritative native
process census is empty. All42 legacy snapshot callbacks remained RAM-only.
No new build, ROM copy, raw media or ZIP was created. Existing portable ZIP,
playable source, executable and CMD are unchanged.

This closes current CPU ball source audio alongside6455's full finite
visual/ground/floor-shadow acceptance. A concrete remaining CPU gap is the
current Bicycle's complete released-body horizontal push, artwork and floor
shadow:5325 explicitly does not accept independent horizontal push replay.
The older3337 source-derived push and3321 full renderer are reusable models,
not current-build acceptance by themselves. Compound6447 already covers this
same Bicycle's whole source audio and should not be rerun for that purpose.
The full original integration/release scope remains open. Previous goal turn:
no progress (acknowledgement); this turn: progress (complete current ball
native audio, precise retirement and exact evidence compression qualified).

`audit_v6473_current_cpu_bicycle_render_checked/report.json` now qualifies
the current naturally chosen CPU Sonya18 Bicycle contact against human
Kano17, including complete native horizontal release push, original donor
body artwork, continuous raster, grounding and floor shadows. Native
process44916 exited naturally0, with empty stderr and no observation errors.
Every original5324 physical input, AI/RNG choice, state/health/round row and
the whole original3395 mobility contact/flags/health/code observation stream
is identical. No game bytes, input policy or CPU action were changed.

Every136 consecutive400x254 screens2662..2797 matches the entire unchanged
original3642 CPU/DMA/shift/VRAM/scanout algorithm:13,817,600 RGB pixels and433
complete palette checks, one initial VRAM base only, with both real target
bit faults rejected. All original Bicycle startup/cycling poses and all six
owned Kano victim poses actually reach visible modeled scanout. Both body
masks are visible in every screen, minimum Kano1,100/Sonya1,510 pixels.
Every57 observed body poses/90 original donor pieces retains exact original
dimensions, pivots, commands and independently decoded sprite indices.

All436 complete pre-clip candidates/publications/projections,774 cached parts
and18,559 independent DMA register bindings retain true physical ownership.
Every274 native shadow eligibility call covers both bodies in137 drawing
fields2661..2797. All435 eligible complete components and10,100 black shadow
copies preserve original compressed row stepping/duplicated final row,
instruction cadence, world/camera/display registers and absolute floor math.
All eligible bodies have all components; ineligible bodies have none. The
Kano134/Sonya135 anchors are unchanged, with no artificial sprite padding.

The entire original paired motion contract remains: start2663/contact2680,
22damage, lift/float/release2712, own landing2738/regain2742, victim landing
2744/hurt clear2749/regain2767. The whole original3337 independent native
push model checks both fixed-point horizontal integrations for30 release
fields and the victim's55 fields through its distinct regain. Actual body
cache geometry reconstructs both complete vertical envelopes. Native decay
gives two suppressed fields, two repulsions, one shared-speed publication and
25 ordinary requested-velocity fields; grounded victim velocity clears at
its own landing. No guessed constant velocity replaces these live branches.
The thirty-field tail retains the real subsequent native combat rather than
imposing an idle-state assumption. Twenty-seven actual body/ground/camera/
DMA/shadow/pre-entry/visibility/push/cache/opcode faults reject; full positives
restore afterward. This is finite current-build evidence, not all arenas or
all possible body-push branches.

The earlier6465/6466 capture and6467 missing-contact rejection remain intact.
Its native process160088 exited naturally0 without observation errors, but
the passive observer set omitted3395, whose direct branch provenance is
required by the full Bicycle contract. The6470 successor adds that entire
unchanged read-only observer, stripping only its already-installed driver
dependency. It does not invent contact rows from older results. Host
preflights also identified the exact two native mode7 pre-entry fields
2661/2662 before mode2/entry2663. Existing independent whole-round observations
bind both physical actor/Main/ID/floor roles in every138 callbacks2661..2798,
including this gap before the legacy pair observer resumes2664. Every later
drawing field is mode2; no arbitrary-mode or missing-body relaxation is used.

`audit_v6475_current_cpu_bicycle_render_storage/report.json` verifies exact
lossless compression of31 finite source/evidence files, including the
preserved incomplete capture:3,554,587 logical bytes,2,719,449 allocated bytes,
440 protected pins unchanged. Both native jobs and host checkers are terminal;
the authoritative native process census is empty. All77 legacy snapshot
callbacks remained RAM-only. No raw media, new build, ROM copy or ZIP was
created. Current playable source, executable, CMD and portable release ZIP
remain unchanged. The already accepted6447 whole Bicycle audio is reused,
not rerun or replaced by a correlation-only audio test.

This closes this finite current CPU Bicycle contact visual/ground/shadow/
horizontal-push gap. Next work should audit the original natural-integration
requirements against current evidence to identify actual remaining stage/
victim branches and final combined release checks; do not keep treating
already accepted CPU moves, four campaigns or endings as untouched groups.
The full original goal remains active. Previous goal turn: progress (whole
ball audio); this turn: progress (whole current Bicycle contact raster,
native floor shadows, independent body push and evidence compression).
