# ROM-side port status (not a release)

## Current authoritative summary

The original-spacing13HP finishing-uppercut controller now earns one native
Kintaro round: attempt31 round2, result153892, counters1-1. Its76842-row
pre-change trace matches the original close attempt; the real grounded/duck
uppercut at153692/gap95 removes the remaining8HP at153700 with player1HP.
The deciding round was lost, so this is NOT a match or campaign clear.
The bounded64-continue endurance trial completed at276392 fields. Across81
observed Kintaro rounds it earned no additional round win and no full match;
the only win is the already observed attempt31 round2. No emulator remains.
Latest unit checkpoint:465 cases. A new finite32-continue controller trial,
stock_wolf_2219_kano_finish13_stomp_refresh, completed at159868 fields,
exit0/no timeout. Its16 boss rounds yielded no wins; closest boss HP29.
It combined13HP finishing and corrected escape-Up, without game/ROM changes
or extra budget. No finishing request occurred; that positive-request audit
correctly rejects this trace. No emulator remains.
The minimal local player ZIP passes independent33-member/hash checks and
isolated exact-ROM patch reproduction; it is not a final/public release.
The official corresponding MAME source
asset is downloaded/hash-verified without extraction/execution for the eventual
release; redistribution/final acceptance are still not approved.

Latest unit checkpoint:452 cases pass. Recent vertical, recovery-only,
recovery-approach and windup-reactive controller trials all completed without
a native Kintaro round win; aborted48-field vertical timing and corrected
audit-offset assumptions are documented in KINTARO_POLICY_PROVENANCE_2219.md.
They do not establish a native game defect. No emulator is running from
those trials. Kano's earned boss clear/campaign video remains open.

The earned lethal-victim matrix is now complete:112 cases across four added
fatalities x14 selectable victims x2 player sides. The independent full-set
audit checks exact coverage and unchanged per-case proof hashes, including
native completion/current26 ROMs and600 fresh-match fields with palette RGB
restoration. See LETHAL_ROSTER_PROGRESS_2219.md and
LETHAL_ROSTER_ACCEPTANCE_2219.json. This is finite victim/side acceptance,
not every edge/interruption/audio path or full-port completion. No ROM code
changed for this expansion; checker assumptions were corrected instead.

The native program/graphics/audio are ROM-side, running on unmodified MAME
0.289 using its existing Wolf hardware definition. The development IPS ZIP
is now SHA256E7B5F63D3EA2CB3A02AF9FBE3BC51660CCE8EB961172F32BB3A2A8278A46BF51:
59 added ASM modules,40 original-source diffs,14 IPS files and12 unchanged
graphics copies reconstruct the current26 chips. This is not a final release.
The documentation refresh includes112-case lethal acceptance. All IPS/ASM
and reconstructed ROM bytes are unchanged; roundtrip archive remains
454772BC6831B6B2F672E59F23FC5456ADCEB886CBC98FE1D8DEC4559EFD0C38.

The latest complete local unittest run passed431 cases (not431 builds or
independent suites). Finite contact coverage includes136 normal/proximity
cells; side-swapped human-state stress observed29054 controlled combat fields
across12 fresh matches. These results do not prove arbitrary matchups or every
possible animation/finisher interaction.

Sonya has an earned full native campaign clear and a47:59 recording with
native audio,157503 contiguous captured frames, full decode/count checks and
sparse visual review. Both29-chapter move showcases preserve every decoded
source frame exactly. See NATIVE_VIDEO_INDEX.md and SONYA_CAMPAIGN_VIDEO_2219.md.
Exact native A/V timing and full subjective animation review remain separate
open acceptance work; encoding preservation alone is not that approval.

Kano has reached Kintaro after the human ladder, but no earned full Kintaro
match/Kahn clear/ending or full campaign video is qualified. The six-hit-queue
variety controller reached6 boss HP without a round win. Unbounded spacing
regressed to69 HP; its292-field retreat exposed a controller problem, not a
ROM defect. The48-field bounded-retreat trial completed cleanly at159411
fields: maximum logged retreat48, best boss HP17, no native round wins.
No emulator remains from that trial. All432 local unit cases pass.
The subsequent close-uppercut hybrid also terminated cleanly, with35 native
uppercut entries/18 linked damage windows but zero round wins, best boss HP47.
It is rejected as an improvement. Latest local unit checkpoint is433 cases.
Adaptive airborne timing then completed cleanly with35 earlier-timed requests,
best boss HP36 and no native round wins. It also failed to improve the result.
Latest full local unit checkpoint is434 cases. No emulator remains.
The opt-in stomp-refresh controller fixed an older-jump tracking error:12/12
observed old-air/ground/new-Up cases reached fresh airtime. Its terminal trial
still had no boss round wins, best boss HP60.438 local unit cases pass; no
native gameplay/ROM change or campaign-clear claim follows from that fix.
Do not infer a win from requests, damage windows, or individual HP minima.

Public main was verified at e602369e41d91cc5d23df4aefabdf42c55af8267 with
the canonical native source/patch snapshot plus697 developer source files.
The newest bounded-retreat experiment is local pending outcome. Remaining
deliverables include Kano's earned campaign/video, final audiovisual review,
and final minimal release ZIP/GitHub release review. No native AI, difficulty,
health, damage or result edits were made to force campaign progress.

Runtime policy: one emulator, hidden/headless and BelowNormal priority;
bounded-memory capture, single-thread encoding, no focus-taking build windows.

## Historical checkpoint log (newest first; pending claims below are historical)

388 tests pass. Postmortem ready104: all27 requests without observed entry
are followed by native Kintaro507h grabs;49 damage windows all20HP,41 other
native entries missed. No Kano/Sonya uppercut timing difference in two
normal-contact recordings:4 active107h fields,57 sitduck fields, stance61
fields after first active tag for both. Do not change native recovery.
New explicit Kintaro Knife-ready controller trial launched hidden/BelowNormal:
ROM-linked bt_stance pointers validated, grounded eligible/full-body stance
stable4 fields, proven D3/neutral3/B3/neutral3/HP3 command, same175 retreat/
48 cooldown and early-stomp escape. Other human/boss policies unchanged.
Read-only kintaro_knife_ready.csv logs command readiness. No native ASM/ROM/
AI/health/difficulty/results edits; outcome pending.

Ready104 campaign terminal exit0/timedOutfalse159494 fields,32 continues,
16 Kintaro rounds/no round or match wins, best CPUHP21. Terminal provenance/
readiness audit passes117 valid requests,90 sampled native uppercut entries,
49 linked damage windows. More linked contact than115 trial, still no
earned boss clear/ending; not full-port completion. No emulator remains.
Refreshed development patch ZIP audit passes;387 tests last pass.

387 tests pass. Refreshed development IPS ZIP documentation/source guide
to current136 normal contacts, current Sonya campaign and native audio
evidence, keeping open gates explicit. ZIP writes now validate a sibling
candidate before atomic replacement; failure/success tests pass. New ZIP
5578739 bytes,SHA256877B7537120B940E3719543230BB7EA0A2C89A77AA04E9CA65AAAF7004F316E8.
Complete package audit exit0:59 own ASM modules,40 original-source diffs,
all packaged file hashes and five current runtime bindings pass. Reconstructed
ROM ZIP remains byte-identical454772BC6831B6B2F672E59F23FC5456ADCEB886CBC98FE1D8DEC4559EFD0C38.
Whole manifest hash changed because provenanceReceipt was renamed, not ROM
bytes. Not a completed release; ready104 campaign still live at Kintaro.
One hidden/BelowNormal emulator; no native ASM/ROM changes.

Ready-counter campaign terminal exit0/timedOutfalse154689 fields,32 paid
continues,16 Kintaro rounds/no wins, best CPUHP81. Audit proves81/81 ready
requests become native uppercuts,17 linked damage windows.64 unlinked
requests all at105..115 gap; <=104 requests linked13 hits, farther4.
Added explicit104/115 controller range option, unchanged native hitboxes.
New104 trial launched hidden/BelowNormal from exact prior profile plus
range flag; result pending. Native duck readiness/minimum6 input spacing
unchanged; no native ASM/ROM/AI/health/difficulty/results edits.

383 tests pass. Added terminal ready-counter audit: verify actual campaign
provenance, every fired request's ground/flags/body/duck-dispatch/distance,
then separate requests, sampled native107h entries within8 fields, linked
HP-drop windows and native counter-based round wins. Negative tests reject
non-ready/airborne/wrong-button-table requests. Audit not run before terminal
receipt; current campaign still live on human route at last observation.
No win/result inferred. One hidden/BelowNormal emulator, no ROM/ASM edits.

382 tests pass. New explicit Kano/Kintaro-only ready-counter trial launched
hidden/BelowNormal from unchanged human/boss-guard route,32 continues.
Unlike fixed pulse or60-field prepare cooldown, HP fires only with native
duck button table/body<=96, grounded/eligible flags, grounded opponent and
distance<=115, minimum6-field input spacing. Native move recovery remains
unchanged. Read-only kintaro_ready_counter.csv logs readiness and each3-field
physical HP request. Other Kintaro options excluded; earlier human route
unchanged. No native ASM/ROM/AI/health/difficulty/results edits. Outcome pending.

381 tests pass. Normal34 video coordinator terminal exit0; all34 actual
captured-hit/two-stance/native-audio/current-ROM/decode checks pass. Full58
catalog terminal exit0,20391129 source bytes. Built two29-chapter showcases,
both terminal exit0/full decode/audio/4:3/exact frame counts: Kano4976,
Sonya4994. Sparse combined sheets viewed, not every-frame/audio-sync approval.
Links in NATIVE_VIDEO_INDEX.md. Outputs total19265234 bytes, no raw/WAV
duplicates retained after verification. No emulator/encoder remains.
These are move showcases, not earned full campaign videos. Kano boss/ending
and final release/audiovisual acceptance remain open; native ASM/ROM unchanged.

381 tests pass. Normal34 recording batch still active: all17 Kano clips,
Sonya through knee qualified so far (actual captured hit/two-stance recovery,
native audio/current-ROM/decode). Sampled sheets reviewed for both uppercuts,
Kano diagonal punch and throw; own poses, impact and recovery visible, not
all-frame review. Added58-clip catalog mode and two29-chapter showcase
builder, tested for exact coverage and exclusion of rejected Pit recordings.
Showcases not built yet; wait for normal batch and full catalog provenance
checks. No native ASM/ROM changes, one hidden/BelowNormal emulator at a time.

Fast-pulse Kano campaign terminal exit0/timedOutfalse157788 fields,
32 paid continues; stock/current-ROM/frozen-input/progression audit passes.
16 Kintaro rounds, no boss round/match won, minimum CPUHP61. No earned
Kano ending; do not repeat this policy unchanged. Recorded current move
families requalified exit0 after harness updates:16 special,8 own lethal,
14 morph/art,8 transformed lethal,16 nonlethal,16 stage/rejoin cases.
34 normal-video batch now live sequentially hidden/BelowNormal: Kano HP,
LP and HK clips pass actual captured hit, two-stance recovery, current ROM,
native audio, encoding/decode and media-hash checks so far. Remaining video
outcomes/visual review pending. No native ASM/ROM changes;380 tests last pass.

380 tests pass. Prepared34 native normal/proximity move videos (17 per
actor), not launched while fast-pulse campaign is live. Capture whitelist
allows ordinary actions only under explicit --normal-moves; normal capture
waits for both stances. Coordinator requires actual contact/damage/recovery
inside contiguous captured interval before encoding/deleting exact verified
raw/WAV intermediates, then verifies final MP4 hash/interval. No all-video
result yet. Fast-pulse campaign still live, one hidden/BelowNormal emulator,
at last observation normal human route around map9. No native ROM edits.

378 tests pass. Source confirms Choke/Leg Grab explicitly reject both bosses.
Successful Sonya Kintaro damage windows are ordinary uppercuts20HP; no boss
grapple workaround. Added explicit Kano/Kintaro-only fast-pulse controller
trial:12-tick HP pulse versus baseline24, native uppercut recovery unchanged.
Other Kintaro experimental branches excluded; earlier human/other-character
input paths unchanged. Fresh full campaign launched from boss-guard profile
after Sonya current-ROM provenance re-audit.32-continue cap unchanged.
No native ASM/ROM/AI/difficulty/health/results edits. Outcome pending.

377 tests pass. Jump32 resumed coordinator terminal exit0, including Sonya
220-gap diagonal punch16/5 with p_hitby on both sides. Aggregate checker
terminal exit0: all136 finite normal/proximity contact cells,17 actual
action types x2 actors x2 player sides x hit/block. Actual current26 ROM,
frozen no-write observers, native action/damage/guard/recovery requalified.
NORMAL_CONTACT_ACCEPTANCE_2219.json. Missed180 Sonya punch and edge100 punch
whiffs remain explicitly separate, not accepted as contact. This does not
prove arbitrary spacing/victims or every animation/audio frame. Kano boss
clear/earned ending and final release/audiovisual acceptance remain open.
No emulator remains; native ASM/ROM unchanged.

Jump32 matrix stopped on Sonya P1 diagonal punch hit: native201h activates
but0 damage/no p_hitby. Geometry shows horizontal overshoot before vertical
overlap; not accepted as contact. Existing failed180-gap run preserved.
Sonya-only diagonal-punch profiles now seek220 gap physically (walk away
if needed); fresh names include_220_. Other jump profiles remain180/70.
Resumed terminal exact-argument evidence, no overwrite; remaining outcomes
pending, hidden/BelowNormal. No native physics/hitbox/ASM/ROM changes.
136-cell aggregate remains unpassed until all real contact cases complete.

376 tests pass. Eight Kano P1 jumping pilots terminal exit0/current-ROM
qualified: vertical punch/kick and diagonal punch/kick, hit/block, native
damage/hit-by/recovery.32-cell jump matrix now live sequentially hidden/
BelowNormal, reusing8 pilots and running24 missing roles. Kano P2 all8
jump cells qualified; Sonya P1 first jump-kick hit qualified so far.
Added136-cell aggregate plan/checker spanning17 actual normal/proximity
actions x2 characters x2 sides x hit/block. Aggregate not run/passed while
remaining jump cells are missing. No native ASM/ROM changes.

374 tests pass. Ground48 matrix terminal exit0: roundhouse/sweep/uppercut/
crouch punch/highkick/lowkick, both actors/sides, hit and appropriate guard,
actual native tags/exact source damage/p_hitby/recovery all qualify.
GROUND_CONTACT_MATRIX_2219.json. Eight Kano P1 jump-contact pilots launched
hidden/BelowNormal after ground exit. Contact jumps settle20 fields, attack
at48, diagonal approach gap180 based on native4px/tick angle jump; baseline
normal schedule unchanged. Expected damage/chip checked against both native
MKSTK tables. Jump results pending, no native physics/hitbox/ASM/ROM edits.

All8 prepared crouch pilots terminal exit0, qualify uppercut40/10,
duckpunch6/2,duck-highkick12/3,duck-lowkick6/2 with native hit-by tags in
both hit/block cases. Alongside four roundhouse/sweep cases,12 Kano P1
ground pilots pass. New48-cell ground matrix reuses those12 and launches36
missing actor/side cases sequentially hidden/BelowNormal. Detailed qualifier
now requires actual p_hitby evidence whenever the new trace columns exist
(ordinary throws excluded). Outcome pending; not full normal acceptance.
No native ASM/ROM changes. Basic40 contact matrix remains passed.

369 tests pass before crouch timing follow-up. First ground pilot batch
stopped after4 qualified roundhouse/sweep hit/block cases: uppercut request
produced native elbow114h/24 damage, not107h. Trace shows walk-in action0
through age12, stance only13, HP14: controller was too early. Failed run
preserved, not accepted as uppercut. Contact-only Down preparation extended
to24 fields (baseline normal schedule unchanged);8 fresh crouch-only pilots
launched hidden/BelowNormal. No native input/game/ROM rules edited. Results
pending. Basic40 matrix remains terminal passed with corrected chip values.

Basic40 contact matrix terminal exit0, all40 cases pass corrected native
damage/chip expectations: both actors/sides, elbow/standing HP/throw/
standing LP/lowkick, hit and block. BASIC_NORMAL_CONTACT_MATRIX_2219.json.
Boundary100 punch whiffs remain separate and invalidated as contact proof.
Twelve new Kano P1 ground-family pilots launched sequentially hidden/
BelowNormal: roundhouse,sweep,uppercut,crouch punch/highkick/lowkick with
appropriate standing/low block. Added passive p_hitby fields to future
traces and explicit low-block controls; no native code/ROM changes.
Ground outcomes pending; not full normal/campaign/final acceptance.

Development ZIP audit rerun exit0: packaged own ASM modules/original-source
diffs match current native source;14 IPS/12 copied graphics reconstruct
actual26 current chips; five pinned runtime receipts match patched bytes,
including exact patched-container run. This is package provenance, not a
fresh compile or completed release. Basic contact40 coordinator still live;
Sonya P1 standing HP/LP actual hit/chip and elbow/throw cells qualified so
far, last observation low-kick hit qualified. Remaining outcomes pending.
No native ROM/ASM edits or overlapping emulator jobs;367 tests last pass.

Correction to prior punch block claims: native HP/LP chip is3/2, not0.
100-gap blocked zero-damage pilots were whiffs; invalidated explicitly in
NORMAL_CONTACT_INVALIDATIONS_2219.json.90-gap HP confirms11/3. Fixed checker
from native MKSTK packed0b03h/0802h records, without changing ROM. First
90-gap batch stopped on old incorrect zero-chip expectation. Resumed same
fresh prefix using terminal exact-argument receipts only (no overwrite),
to run missing40-cell basic contacts. Outcome pending, hidden/BelowNormal.
Both100-boundary evidence and original stopped matrix remain preserved.

Passive instruction-read tap resolves the two edge-punch outcomes:6 actual
strike_check entries each, P1 one positive overlap->11 damage, P2 zero
positive overlaps->0 damage. Tap runs' normals.csv are byte-identical to
their untapped geometry replays, actual current26 ROM verified. Thus the
end-of-field overlap appeared too late for P2's native checks; no hitbox
enlargement justified. PUNCH_STRIKE_ENTRY_2219.json pins the evidence. First
tap attempt used unsupported register_stop and failed before gameplay;
those two traces remain failed evidence, corrected entry2 runs pass.
Normal qualifiers now reject Fatal error logs as well as LUA ERROR.
Basic contact matrix still stopped, not passed; next use intentional
in-range punch spacing while retaining these boundary/whiff checks.
No native ASM/ROM changes or emulator left running.

Read-only multipart-geometry replays completed for the good P1 and missed
P2 edge-punch profiles on identical current ROMs/physical inputs. Reproduce
11 versus0 damage. Native JOY sf_squeeze shrinks each victim side by
(width>>2)+(width>>3); both first show2px positive end-of-field overlap at
combat29. Earlier HP fields have negative horizontal overlap. Exact CPU
strike-check instants not observed, so process/pose timing is an inference,
not proven cause or facing defect. PUNCH_EDGE_GEOMETRY_2219.json pins actual
geometry/traces; originals preserved. No native hitbox/code change and no
emulator remains. Basic40 matrix remains incomplete/stopped.

364 tests pass. Basic40-cell coordinator STOPPED on first player-two
standing HP hit check (exit1, not a matrix pass). Ten pilots and Kano P2
elbow hit/block qualify; `stock_wolf_2219_basic_contact_hp_17_p2_100_hit`
is terminal exit0 but actual101h punch does ZERO damage at recorded99 gap.
Comparable P1 at100 gap deals11. Failed evidence retained; no retries or
hitbox changes yet. Native own HP collision records in MKSTK are80,8,45,30
for both characters, sf_squeeze. Need inspect native collision/facing/pose
geometry to distinguish edge reach from port defect. No emulator remains;
no native ASM/ROM changes. Do NOT claim all40 basic contacts passed.

363 tests pass. Ten new Kano P1 basic-contact pilots qualify actual current
ROM/native action/exact damage/recovery: HP70 elbow24/6; HP100 standing11/0;
LP70 throw34/34; LP100 standing8/0; LK100 lowkick26/6 (hit/block). Throw is
not mislabeled low punch, zero blocked punch chip not mislabeled no hit.
Detailed qualifier extended without changing old HK expectations. All jobs
terminal; no emulator remains. Sonya/other-side basic contacts and remaining
normal families are not inferred. No native ASM/ROM changes.

Knee/high-kick contact coordinator terminal exit0: all16 finite character/
side/gap/hit-block cells qualify current26 ROM, exact20/6 knee or32/8 high-kick
damage, native action, true roles, attacker recovery and victim reaction/
guard. NORMAL_CONTACT_MATRIX_2219.json records cases.361 tests last pass.
Six fresh Kano P1 standing HP/LP/LK hit/block pilots launched sequentially
hidden/BelowNormal; outcomes pending. No native ASM/ROM edits.

361 tests pass. Added strict normal-contact qualifier: terminal stock/current
26-chip ROM, frozen read-only observer, contiguous trace, true actor roles,
120-field request window, actual knee10fh/high-kick103h, exact observed damage,
attacker recovery and victim reaction/continued guard.16-case coordinator
reuses four immutable pilots, launches12 missing actor/side/gap/hit-block
cells sequentially hidden/BelowNormal. First Kano P2 knee hit/block cells
qualify; remaining outcomes pending. No native ASM/ROM changes.

360 tests pass. Four fresh normal-contact pilots terminal/current26 checked:
Kano P1 close-HK becomes native knee10fh (20 hit/6 block); at100 gap it is
actual high kick103h (32 hit/8 block).120 action-window plus120 recovery
fields each. Unblocked pair returns stance; blocked victim intentionally
continues700h guard, attacker returns stance. No all-contact/mirror/visual
acceptance inferred. See NORMAL_CONTACT_2219_CURRENT.md. Physical approach
only, no native ROM/health/position/rules edits. No emulator remains.

359 tests pass. Mirrored normal probe terminal exit0, all28 expected
action/late-recovery cells observed with true Sonya P1/Kano P2. Original
normal recording requalified28/28 after inspector role generalization;
56 total finite actor/side/action/recovery cells. Mirrored roundhouse and
uppercut screenshots reviewed, own names/poses visible. Original filenames
and frozen observer evidence unchanged. This is not hit/block/damage,
arbitrary-facing or every-frame animation acceptance. No emulator remains;
no native ASM/ROM changes.

358 tests pass. Dedicated normal probe terminal exit0: all28 finite
actor/action cells observed expected native tag plus late stance recovery
(14 standing/back/duck/vertical-jump/forward-jump attacks for each actor).
Current26 ROM/stock/frozen read-only observer/true17+18/no missing roots
checks pass. See baseline/stock_wolf_2219_normals_01/NORMAL_MOVE_OBSERVATIONS.json.
Roundhouse/flying-kick screenshots sampled; not damage/block/all-frame art
or both-side/facing proof, so full normal acceptance remains incomplete.
Knife-midrange campaign terminal154769 fields/32 continues,16 Kintaro rounds,
no boss round/match won; best CPUHP69. Terminal/progression audit passes.
No Kahn/earned Kano ending. No emulator remains; no native ROM changes.

Audited two current campaign inventories against native MAINEQU action tags.
Kano has12/14 ordinary tag types unobserved there; Sonya9/14. These are
coverage gaps, not proof of missing/broken moves (short tags can also fall
between samples). CAMPAIGN_NORMALS_2219.json pins actual source/recordings.
Added dedicated --normal-moves input-only probe with14 explicit ordinary
attack profiles, both actors, per-field true identity/action/shape records
and sampled screenshots. Runtime not yet launched while campaign is live;
no normal-move success claimed from requested controls. No native ROM edits.

All355 tests pass. Native MKBOSS goro_slam directly takes over the victim;
can_goro_slam allows distance<=120 with airborne exclusion commented out.
Intermediate guard is not a solution. New explicit controller-only Knife
midrange trial uses retreat below175 versus earlier260 and48 versus80 shot
cooldown; baseline Knife/other routes unchanged, stomp evasion retains
priority. Full campaign launched once hidden/BelowNormal with existing32
continue cap and unchanged ROM/rules. Outcome pending. Normal-move systematic
coverage also needs review; no full-port completion inferred from specials.

Mixed-guard campaign terminal exit0/timedOutfalse at154131 fields,32 paid
continues; full stock/current-ROM/frozen-input/progression audit passes.
16 Kintaro rounds, no winning boss round/match; best CPUHP93 versus previous
mixed trial29. The added intermediate-range guard did not solve the campaign
and should not be treated as an improvement. No Kahn/earned Kano ending.
All recorded current move families requalified after the harness addition:
16 ordinary special cells,8 own lethal,14 morph/art,8 transformed lethal,
16 nonlethal eligibility and16 stage/rejoin cases. Coordinator exit0.
354 unit tests last pass; no native ASM/ROM changes. Source guide corrected
to cite current2219 earned Sonya campaign evidence. No emulator remains.

Consolidated24 current demonstration clips into a verified catalog without
copying media:10207175 bytes total. Every actual archive's26 chips, terminal
stock/no-write receipt, frozen observer, video hash/size and contiguous
capture rechecked; stage arena/Pit timing and special/morph media-binding
proofs also checked. Rejected first Pit clips excluded. Collector terminal
exit0. Not campaigns/all-normal-moves/all-frame audiovisual approval.
Mixed-guard campaign still live at last observation; result pending.

All353 tests pass. One mixed-guard Kano campaign trial launched hidden and
BelowNormal with the previous mixed profile plus its explicit guard option;
32-continue/180000-field cap unchanged. Runtime result pending. No simultaneous
emulator jobs, native ROM edits, health/difficulty/AI/result manipulation.

Both current morph sample sheets and exact final decoded frames reviewed:
own fighter/projectile, then restored Shang on both sides. Not all-frame or
audio-sync acceptance. Mixed Kano boss trace shows28 sampled40HP loss windows
with Kintaro507h; no same-attempt boss win. Added explicit default-off
mixed-guard controller option: Down+Block only at116..174, keeping existing
close actual-duck uppercut readiness. No native rules/ROM edits. Trial next.

Morph refresh terminal exit0: both552-field clips qualify actual524-field
true own identity,22-damage projectile and automatic Shang return within
capture, plus native morph/art trace/current-ROM/decode checks. Sampled visual
review pending. Current links indexed. No emulator remains from these batches.

All352 tests pass, including rejection of wrong-arena/truncated Pit clips.
Filtered Pit coordinator terminal exit0: both266-field clips pass exact
206+60 cinematic capture/current-ROM/rejoin/decode checks. Both sampled Pit
sheets viewed through launch, fall, own impact art/result. Rechecked four
Dead Pool/Tomb captures against arena rows; all pass. Six correct stage
links now indexed, with rejected first Pit captures explicitly excluded.
Morph video coordinator launched hidden/BelowNormal after Pit exit; results
pending. No native ASM/ROM changes or full-port acceptance claim.

Stage batch terminal, but capture audit REJECTS its two Pit clips: they recorded
earlier Tomb, despite native Pit gameplay/rejoin passing. Old six-case manifest
is insufficient video proof. Evidence preserved; see STAGE_VIDEO_CAPTURE_REVIEW_2219.md.
Added arena filter and exact Pit cinematic interval check before encoding.
Two fresh filtered Pit retries launched hidden/BelowNormal; outcomes pending.
Both Dead Pool/Tomb sampled sheets reviewed. Stage-plan2 tests pass; latest
whole suite350 predates the additional arena-filter test. Morph remains queued.
No native ASM/ROM changes.

All350 tests pass after stage/morph video-plan coverage additions. Current
stage capture coordinator is live hidden/BelowNormal: both Dead Pool clips
and Kano Tomb have qualified; remaining cases pending. No simultaneous
emulator jobs. Morph refresh coordinator added/tested but not launched while
stage work is active. Both Babality sampled decoded sheets reviewed: native
transformation FX, own baby art and winner poses visible. This is sampled
review, not all-frame/audio-sync acceptance. No native ASM/ROM changes.

The four current2219 Friendship/Babality clips are terminal and qualified:
earned eligibility, full active-field capture, current26 ROM bytes,
600 fresh combat fields and video/audio decode. Friendship sample sheets
reviewed; Babality visual review and whole-video/audio-sync acceptance remain
open. Current links added to NATIVE_VIDEO_INDEX.md. No native ROM change.
New six-case stage-video coordinator plan test passes; stage refresh is next.
Older progress entries below are historical, not current live-process state.

All348 tests pass. Four current Friendship/Babality demonstration runs are
active sequentially hidden/BelowNormal, using verified eligible own-victim
profiles, native audio, every active finisher field,600 fresh combat fields
and Sonya Friendship process-lifecycle checks before encoding. Later result-
screen/continuing-animation loops are explicitly not full-capture claims.
No native ASM/ROM/rules change; outcomes/visual review remain pending.

Terminal: all4 current2219 lethal demonstration clips complete coordinator
exit0. Earned KOs/native completion/current26 bytes, every active finisher
field (231/176/231/176),600 fresh-match/palette fields, encoding/decode pass.
Sampled sequence sheets individually reviewed; no all-frame/audio-sync claim.
Current links in NATIVE_VIDEO_INDEX.md; raw intermediates removed after
verification, videos/hash/trace proof retained. No emulator remains.

Current lethal video refresh is active sequentially hidden/BelowNormal:
extraction, Eye Laser, flame kiss and Death Orb. Physical earned KOs, actual
current-ROM/native completion, exact all-active-field capture and600 fresh
combat/palette fields must pass before encoding/decode validation. Only
verified raw intermediates are removed; failed evidence is not overwritten.
Capture/visual outcomes remain pending. No native ASM/ROM/rules changes.

Terminal: all8 current2219 special demonstration videos pass coordinator
exit0, move/current-ROM qualification, frame/audio decode and captured-hit
interval checks. Current links added to NATIVE_VIDEO_INDEX.md; old numbered
finisher/morph clips remain explicitly historical. First six clips have
sampled decoded-frame review; Bicycle/Square also reviewed as12-frame sheets.
No whole-video/audio-sync/campaign acceptance inferred. Verified raw BGRA/WAV
intermediates removed after encoding, MP4/hash/trace evidence retained.
No emulator remains; no native source/ROM/rule changes.

All346 tests pass. Mixed Knife/uppercut campaign154497 fields normally,
stock/current-ROM/frozen audit passes, no Kintaro match clear. Current video
coordinator is active after that terminal run; recorded move-family refresh
completed exit0. No native ROM/rules/AI edits, no parallel emulator.

Eight current2219 special demonstration clips queued behind the exact mixed
campaign wrapper. Sequential hidden/BelowNormal recording, native audio,
bounded150-field minimum/400 maximum capture, move/current-ROM qualification,
encode/decode and captured-hit checks before next run. Encoder deletes only
its exact verified raw BGRA/WAV intermediates, keeping video/hash/trace proof.
No large AVI accumulation. Old video index now explicitly historical, not
current2219 proof. Video outcomes/visual review remain pending.

Active: `stock_wolf_2219_kano_kintaro_mixed`, hidden/BelowNormal stock MAME,
32-continue budget. Explicit boss-only mixed controller fires existing Knife
plan from>=175 spacing; closer pressure uses actual grounded/duck-height/
button-table readiness for<=115 HP requests,24-field spacing/3-field hold.
Native projectile guard and early stomp evasion remain. Other failed boss
options excluded; human/Kahn policy unchanged. All345 tests pass. No ASM/
ROM/difficulty/AI/damage edits; pending terminal native-result/current-ROM audit.

Terminal: long-range Knife trial155684 fields normally, current-ROM/stock/
frozen-input audit passes.16 Kintaro rounds/no win/bestCPUHP128,16 sampled
Knife action entry episodes. The260 retreat threshold permits too few firing
windows; this is not a native move-failure or boss-clear claim. No emulator
remains. Development package and no-launch stock-MAME/ROM launcher pin checks
also pass without changing package, ROMs or opening a window.

Development ZIP audit rerun passes all actual file hashes,40 original-source
diffs and59 own ASM modules against the native build, plus five matching-
patched-chip runtime cases. Checked launcher verifies exact stock MAME and
patcher ROM archive pins without launching a window. No package/ROM change;
final release acceptance remains incomplete. Knife campaign remains active.

All344 unit tests pass. Four in-memory cursor regression fixtures verify
that the pixel checker detects a one-pixel shift, thinner border, wrong
number placement/color, while accepting translated native geometry and
dim/bright palette phases. No game image/art/ROM was edited. Knife campaign
remains active; read-only move-family refresh completed exit0, no second emulator.

Active: `stock_wolf_2219_kano_kintaro_knife`, hidden/BelowNormal stock MAME,
original32-continue budget. Explicit Kano/Kintaro-only controller retreats
below260 without Block, guards native projectiles, releases crouch/guard to
actual standing readiness and starts the existing D,B,HP plan with80-field
spacing. Early stomp evasion retains priority. Other failed boss options
excluded; human/Kahn policies untouched. All340 tests pass. No native
ASM/ROM/difficulty/AI/health/damage/range edits. Outcome pending terminal audit.

Terminal: corrected P2 UI captures and pixel qualifier pass.19 Kano and31
Sonya samples match the unobscured native Liu P2 red border and centered
61-pixel numeral2, with18/30 sampled dim/bright transitions. True own first-
combat identities and existing native special checks pass with all26 actual
ROMs verified. Earlier Cage reference was occluded by adjacent P1 border;
Reptile join frame lacked a drawn cursor. Neither is used as a full reference.
P1 pixel qualifier also reruns successfully. These finite UI proofs do not
accept every transient/navigation edge. No emulator remains. See
SELECTION_P2_2219_QUALIFICATION.json and SELECTION_UI_2219_QUALIFICATION.json.

Terminal: corrected Blade-retreat trial151331 fields normally; current-ROM/
stock/frozen-input audit passes.16 Kintaro rounds/no win/bestCPUHP148.
Guard action is no longer among main sampled states, but strategy still
fails; do not promote it. Frozen unsuccessful traces remain separate.

First P2 UI recordings finish normally but MISS cursor phase (window began
after lock). They are not highlight evidence. Corrected observer starts3000
for explicit special profiles, retains3500 for campaigns, ends4500 in both.
Two observer tests pass; `selection2_p2` recordings are running sequentially
hidden/BelowNormal. No ROM/gameplay-input changes for capture correction.

Player2 UI captures queued after the exact active Blade-retreat wrapper:
existing tested special profiles select P2Kano via mirror and P2Sonya via
Square profile. Observer remains read-only/default-off, now explicitly
allowed with campaign OR special profiles. Two observer tests pass. Sequential
hidden/BelowNormal; no overlapping emulator. P1 pixel proof is not P2 proof;
new capture outcomes remain pending. Wrapper-option proof pins need final
refresh after this harness-only extension.

Read-only clean-build verification rerun passes: regenerated-source130-object
independent program outputs and independently compressed/linked sound ROMs
still match current native build byte-for-byte. No compiler launch/source
edit required. JOY.ASM confirms Block is checked before left/right walking;
the active Blade-retreat test releases Block for that physical walk request.

Active: `stock_wolf_2219_kano_kintaro_blade_retreat`, hidden/BelowNormal.
Controller correction releases Block while asking to walk away below175;
prior Blade policy held both Back+Block and mostly guarded in place.339
tests pass. No native ASM/ROM/AI/range/rule edit. Frozen old controller is
preserved in its failed run, not overwritten.

Terminal: first Blade trial150767 fields normally, current-ROM/stock audit
passes,16 Kintaro rounds/no round win/bestCPUHP135.35 sampled Blade entry
tag episodes (not35 proven hits). All26 chips match baseline; compared
gameplay fields first diverge130356 at the intended boss-policy boundary.
No earlier-human regression established by that comparison.

Current UI qualifier passes both completed recordings after full actual-ROM/
stock/frozen-input audits.31 Kano and16 Sonya samples exactly match original
Liu border geometry plus the centered63-pixel player1 glyph.30/16 sampled
dim/bright transitions and18/17 preview-region pixel variants observed.
These are finite matching samples, not acceptance of every transient frame;
the remaining samples include transitions/fades and are not silently counted
as exact matches. First combat keeps true own IDs. See
SELECTION_UI_2219_QUALIFICATION.json with all captures/source/runtime pins.

Active: `stock_wolf_2219_kano_kintaro_blade`, hidden/BelowNormal stock MAME,
32-continue original budget. Explicit Kano/Kintaro-only spacing controller
starts the already-tested native D,F,HP Blade plan at175..240 center gap
from actual ready standing state, retreats below175 and guards beyond240.
Original boss can_slam gate is120; repeated close uppercuts enter that gate.
Early stomp evasion still has priority; human/Kahn policies unchanged.
All339 tests pass. No native ASM/ROM/range/AI/rule edits. Outcome pending.
Earlier experimental boss flags are excluded; future proof refresh required.

Terminal: both current selection-ui recordings exit0 and pass actual-ROM/
stock/frozen-input/identity audits. Individually reviewed native borders,
centered player1 numerals, changing own previews and clean ladder screenshots
with Kano/Sonya ladder entries. Highlight rim alternates green123/255 in
sampled four-field captures for BOTH actors (39 Kano/24 Sonya select samples).
Further finite UI analysis remains separate; no every-transition claim.

Terminal: Kano endurance298470 fields normally,64 paid continues audited.
Eight individual earned Kintaro rounds across separate attempts, no match
clear. No Kahn/earned ending. No native ROM/rule/AI changes or emulator
remains. Further repeating this identical policy is not justified by a new
native defect; spacing/unblockable slam policy needs a different approach.

All338 tests pass. Explicit selection-ui observer captures bounded startup
fields3500..4500 (4-field selection/10-field later cadence), guarded object
reads and no inputs/guest writes. Separate Kano17/Sonya18 UI recordings are
queued behind the exact live endurance wrapper, sequential hidden/
BelowNormal. These are pending captures, not blink/cleanup acceptance.
Endurance-era recorded move-family requalification completed exit0; the new
observer option is default-off and does not change native ROM or gameplay.

Current Kintaro reaction coverage: read-only completed-campaign qualifier
passes after full current-ROM/stock/frozen-input and linked-script audits.
1562 Kano and1400 Sonya sampled507h opponent-action fields retain own body
descriptors; all3 script-referenced poses observed for each. Player1 victim
only; six-step timing/coordinates and mirrored visual choreography remain
unproven. See generated_roster_roots/KINTARO_CAMPAIGN_REACTIONS.json.
No ROM change or emulator launch was needed for this analysis.

All336 tests pass. Campaign audit now independently validates explicit
continue/field budgets, rejects negative/duplicate/excess limits, and
records the declared budget. Earned-clear/uppercut proofs pin that helper.
Sonya's current earned-clear and two-page ending requalification still pass
under the stricter auditor (32 continues/180000 fields, no endurance flag).
Active Kano endurance run remains hidden/BelowNormal; native ROM/rules/AI
unchanged. Endurance outcome still requires terminal native-result audit.

Current: `stock_wolf_2219_kano_boss_endurance`, hidden/BelowNormal stock MAME.
Uses the better original evasion/uppercut controller, NOT either readiness
or jumpkick experiment. Explicit endurance option allows64 paid continues,
300000 observed fields and720-second host bound. Native difficulty/AI/health/
damage/positions/results unchanged;333 tests pass, previous default32 cap
retained without the explicit option. Pending terminal earned-clear audit.

Terminal: wide-readiness trial159019 fields normally, audit passes.106 boss
requests/72 native activations/44 observed20HP windows, one earned Kintaro
round139070 on attempt27, no match clear. Earlier baseline remains better.
Move-family pins require refresh after the endurance harness change.

Current activity: `stock_wolf_2219_kano_kintaro_wide` is running hidden/
BelowNormal.331 tests pass; explicit105 boss-only HP request range retains
human84 thresholds/native-readiness gates. Diagnostics derive that range
only from the recorded wide-policy argument. No ROM/rule/AI changes.
Move-family requalification completed exit0 read-only without another emulator.

Package audit rerun passes: all packaged file hashes,40 applied original-
source diffs and59 own ASM modules match current native build. Five torso
runtime cases match patched chip bytes, including exact patcher archive.
No complete ROM/emulator/custom driver is included; this remains development.

Entries below are cumulative historical run snapshots. Their active/no-
emulator wording describes those checkpoints, not the current activity above.

Terminal: mirrored2219 track3 audio closes the missing uninterrupted variant;
9/9 independent tails exceed0.98, all four variants observed. Across isolated
diagnostics41/41 evaluable tails exceed0.98. Production track-sum check gives
correlation0.999902873/residual RMS0.888119 PCM16/max12 with no fitted
parameters and bounded chunks. Finite mix evidence, not exact/all-audio
acceptance. No emulator remains. See AUDIO_2219_CURRENT.md.

Terminal: three current2219 isolated audio tracks and bounded analyses exit0.
32/32 evaluable independent pre-command tails correlate>0.98 with native
codec references (10/13/9 by track). Tracks1/2 cover all four uninterrupted
variants; track3 variant1 remains for mirrored coverage. Production overlap
mix/preempted tails remain unaccepted. No emulator remains. See
AUDIO_2219_CURRENT.md. Native source/ROM/rules unchanged.

Terminal: current2219 native/muted-control Friendship audio pair exits0.
39 matching native DCS cues/all four variants/cadence/cleanup qualify.
Fixed240000-sample post-cue window is bit-identical and non-silent. This
does not certify full individual tails/overlap mix. No emulator remains.
See AUDIO_2219_CURRENT.md; no native code/rule change.

Terminal: all four current2219 earned Jax clap victim/fresh-match cases
qualify, coordinator exit0. Each verifies600 fresh combat/palette fields,
reset correct identities/state and real damage. See CLAP_2219_CURRENT.md.
Active: current2219 native/control Friendship audio pair, sequential hidden/
BelowNormal stock MAME. Control is explicitly diagnostic muted-playlist
sound bank, not release data. Pending audio analysis; no mix claim yet.

Terminal: all four current2219 Liu bicycle victim cases qualify, family
exit0. Five own reaction poses, actual damage and99-field paired stance
recovery checked; four impact images individually reviewed. See
LIU_BIKE_2219_CURRENT.md. Four earned Jax clap/fresh-match cases are now
active hidden/BelowNormal and sequential, no parallel emulator.

Terminal: four current2219 Raiden tackle victim cases qualify, tackleExit0.
30 damage, paired200-pixel travel/72 spacing, own art and both recoveries
verified; four impact samples individually reviewed. See
TACKLE_2219_CURRENT.md. Liu bicycle family remains active sequentially.

Terminal: Kano forward-jumpkick experiment rejected:151769 fields normally,
current-ROM/stock/frozen-input audit passes; no Kintaro round win in16 rounds,
bestCPUHP110. Earlier simple evasion/uppercut policy remains better. No native
game change. The queued tackle/bicycle batch is now running sequentially.
Linked ladder/ending/cast tables reverified and independent ending-art
rebuild matches current packed graphics byte-for-byte.

Four current close-shock impact images individually reviewed: retained own
Kano/Sonya art, native blue palette and mirrored contact. Finite visual
review in SHOCK_2219_REVIEW.md; no all-field/audio claim. Eight flying-tackle/
Liu bicycle victim refreshes are queued behind the exact active Kano
jumpkick campaign wrapper, sequential hidden/BelowNormal, stop on failure.

Active: `stock_wolf_2219_kano_kintaro_jumpkick`, hidden/BelowNormal, one
stock emulator. Explicit boss-only physical jumpkick trial, prior failed
readiness flag excluded; all330 tests pass. Native ROM/rules/AI unchanged.
Human route and Kahn policy preserved. See KANO_BOSS_CAMPAIGN.md. No
campaign-clear claim before terminal native-result/current-ROM audit.

Terminal: close-shock family exits0; the entire12-case spear/lightning/shock
batch is complete and no emulator remains. Four close-shock actor/side cases
each observe32 damage,99 attacker-active fields,48 palette-flash fields,
retained own body and both fighters recovered to stance. Machine behavior
proof is current; whole electrical-animation visual/audio acceptance is not
implied. See SHOCKER_VICTIM_QUALIFICATION.json for actual ROM/runtime pins.

Terminal: all four current2219 spear and four lightning victim cases qualify
(both actors/both sides), coordinator family exits0. Own art, native damage,
palette/recovery gates pass; sampled spear impacts and lightning recovery
captures individually viewed. See SPEAR_2219_CURRENT.md and
LIGHTNING_2219_CURRENT.md. Close-shock family remains active sequentially.

Terminal: Kano Kintaro-readiness experiment REJECTED as a strategy. Normal
153740-field completion; current-ROM/stock/frozen audit passes. Six Kintaro
HP requests/four native uppercuts, no40HP window, no round wins in16 rounds,
bestCPUHP141. The previous policy performed better. No ROM defect inferred
and no native change. Ordinary spear/lightning/shock refresh batch is active
hidden/BelowNormal, sequential only. See KANO_BOSS_CAMPAIGN.md.

Current source/linked-ROM structural checks rerun successfully: all146 own
roster animation dispatch entries,16 listed drone dispatch tables and5
extended scalar reaction tables. Reports remain explicitly not all-animation
behavior/art or complete CPU-gameplay certificates. No ASM/ROM edits.

All329 unit tests pass. Recorded current2219 move families requalify exit0
after the explicit Kintaro readiness flag: ordinary16, own lethal8, morph14,
transformed lethal8, nonlethal16 and stage16. No frozen recording/ROM edits.
Twelve fresh ordinary victim cases are queued behind the exact active Kano
campaign wrapper: spear4, lightning4, close shock4. Sequential hidden/
BelowNormal; stop on any failure. Results remain pending, not accepted.

Active: `stock_wolf_2219_kano_kintaro_prepare`, hidden/BelowNormal physical
Kintaro readiness trial. Requires explicit Kano boss flag; earlier human
policy/Kahn counters/native ROM/AI/rules unchanged. Pending terminal audit;
do not overlap an emulator. See KANO_BOSS_CAMPAIGN.md. Last whole suite328
passed;9 targeted evidence tests pass after the added gating test.

Current Sonya ending review: both story pages, dedicated cast pair, original
cast samples, credits and gameover viewed individually. Two distinct nonblack
story pages pass12-consecutive-field stability/state checks. This is finite
visual evidence, not every-field/audio acceptance. See
SONYA_ENDING_2219_REVIEW.md. No ROM change or emulator launch was needed.

Terminal: current2219 freeze/shadow coordinator exits0. All four fresh
actor/side freeze/thaw cases qualify;36 bank/control cases and2507 bounded
current floor-shadow fix pixels match. No emulator remains. See
FREEZE_SHADOW_2219_CURRENT.md for scope and proof hashes.

Terminal: `stock_wolf_2219_sonya_campaign` exits0/not timed out. Full current
26-ROM/stock-emulator/frozen-input/identity audit and earned-clear qualifier
pass: all14 human opponents and Kintaro cleared, Shao Kahn2–0 on attempt24,
native winning frames151506/152720,17HP at clear, attract return161165.
All12 Kahn counter requests enter native uppercut within8 fields and have
linked opponent-health drops. No game-memory writes or native-rule changes.
Current captures individually reviewed at ending ages300/1140/1980 show
native Kahn defeat, SONYA WINS congratulations, and own photo/story page1.
Story page2/cast/credits full visual review remains open. Freeze/shadow
refresh has started sequentially after the completed campaign.

The active/queued description below is historical; see the terminal result
above and the live freeze coordinator for current process state.

Active: `stock_wolf_2219_sonya_campaign`, hidden/BelowNormal, reuses the
historical successful Sonya787 physical-input flags on current2219 ROMs.
No native ROM/rule changes. Terminal current-ROM campaign/ending audit is
still required; no overlapping emulator should be started.327 unit tests pass.
The current freeze/shadow refresh is queued behind that exact campaign
wrapper process. It will run four fresh `stock_wolf_2219_freeze` cases
sequentially and invoke the bank-shadow pixel qualifier only if all four
freeze cases qualify. Hidden/BelowNormal; no parallel emulator. Pending
results are not acceptance evidence.

Terminal: `stock_wolf_2219_kano_boss_guard` finishes164920 fields normally,
exit0/not timed out; current26/stock/frozen-controller audit passes. All14
humans cleared again. Two earned Kintaro round wins (attempt27/frame141002,
attempt31/frame157298), neither deciding-round win;32-continue cap exhausted.
34 recorded stomp-escape episodes all observe Kano airborne, not proof every
stomp was avoided. Kahn/earned ending remain open. All recorded move-family
proofs requalified successfully. See KANO_BOSS_CAMPAIGN.md. Earlier human
policies and native ROM/rules/AI are unchanged.

Terminal: `stock_wolf_2219_kano_human_prepare` completes156420 normally,
current26/stock/frozen audit passes. ALL14 human opponents have earned native
same-attempt match wins, including real Kano/Sonya. Reaches Kintaro/map15;
no Kintaro round win, bestCPUHP21 across16 rounds.325 tests pass; native
ROM/AI/rules unchanged, no emulator remains. Bosses/earned ending/final
acceptance remain open. See KANO_HUMAN_CAMPAIGN.md for exact evidence pins.

Terminal: `stock_wolf_2219_kano_mileena_prepare` earns Mileena2–0 on attempt18,
results83590/84832, player63/89HP; reaches Cage/map8. Current26/stock/frozen
audit passes,120000 fields normally.41282 pre-Mileena rows unchanged,
preserving Sub2–0. No Cage match/full campaign clear.324 tests pass; no
native ROM/AI changes or remaining emulator. See KANO_MILEENA_CAMPAIGN.md.
All recorded main move/finisher families requalified after this harness flag.

Terminal: `stock_wolf_2219_kano_early_prepare` earns Sub-Zero2–0 on attempt18,
native results80660/82256 with98/34 playerHP.8/8 uppercuts/40HP hits and4/4
Knives activate; two Knives remove final1HP. Current26/stock audit passes;
39776 pre-Sub rows unchanged. Run leaves campaign normally at119110 after
32-continue cap, on Mileena/map7. No emulator remains; Mileena/campaign open.
See NEUTRAL_UPPERCUT_CAMPAIGN.md. Development ZIP refreshed in place with
input tip/current status; ROM bytes unchanged, package/source audit passes.

Terminal: `stock_wolf_2219_kano_standing_knife`,120000 fields normally,
stock/current26 audit passes. Spaced Knife103120 activates211h and removes
the final1HP; earned round103340 (attempt25/round1,1–0), no match/map advance.
47/47 uppercuts activate.39776 pre-Sub rows byte-identical to prior trial.
Native ROM/AI/rules unchanged; no emulator remains. See
NEUTRAL_UPPERCUT_CAMPAIGN.md. Current Kintaro reaction scripts also pass
source/linked-byte checks; that is not runtime choreography acceptance.

Terminal: `stock_wolf_2219_kano_knife_finish` completes120000 fields normally,
current26/stock/frozen audit passes.47/47 uppercuts activate;35 have40HP/hit
tag evidence. One Sub round win103388 (attempt25/round1,1–0), no completed
match/map advance. The one physical Knife sequence does NOT activate211h,
so the round is not credited to a Knife hit. No emulator remains. Nonlethal16
and stage16 recordings requalify against current harness/source pins.

Terminal: `stock_wolf_2219_kano_uppercut_hold` completes120000 fields normally,
actual current26-ROM/stock/frozen-controller audit passes.43/43 requests
activate native uppercut;33 show victim-hit tag plus40HP loss in the same
round. No Sub round/match win; two rounds reach1CPUHP. Five evidence tests
pass. See NEUTRAL_UPPERCUT_CAMPAIGN.md. Native ROM/rules/AI unchanged;
no emulator remains. Near-finish strategy/campaign completion is still open.

Terminal: `stock_wolf_2219_kano_neutral_uppercut` completed120000 fields
normally, current stock/26-ROM audit passes, but zero uppercut requests and
no Sub round/match win. Preparation windows last only1..5 fields and reset
before duck readiness. See NEUTRAL_UPPERCUT_CAMPAIGN.md. No emulator remains.
All16 special/side cells requalified against updated harness/source pins.
The harness wrapper changed for its explicit opt-in flag; prior evidence
pin freshness must be rechecked normally, not silently ignored.

All four `stock_wolf_2219_raidenburst` cases qualify, coordinator exit0:
166 native fields, one true-own late head, seven head frames, measured
trajectory/floor settlement.24 scheduled captures were individually reviewed;
tested visuals accepted separately from machine-only gates. See
RAIDEN_BURST_2219_REVIEW.md for pins and exclusions. No physics/ROM/art
change was needed; no emulator remains after the completed batch.

All six `stock_wolf_2219_split` cases now qualify, coordinator exit0:
four own roles and original Liu/Kitana controls. Cleanup also independently
qualifies all six object-list traces through9000.40 own pose scenes and eight
transition samples were individually reviewed. See SPLIT_2219_REVIEW.md for
pins, scoped visual acceptance and framebuffer-vs-object-removal distinction.
No emulator remains live after this batch.

Latest runtime batch: `stock_wolf_2219_inflation_{17,18}_p{1,2}` completed.
All four emulator runs exited0 without timeout. The original coordinator
failed its early-log-only phase check; the corrected qualifier independently
passes unchanged early+late recordings (exit0). No emulator remains live.
See INFLATION_2219_REVIEW.md for the distinction and scoped visual review.

Current program is `221919459A4129FFDB37C8A3E9EC7F9AA6210D99AED00A35BC3256842C5E1F5A`.
The development IPS ZIP/checked launcher already target this build. Native
ASM and ROM patches run on unmodified stock MAME; no custom driver is needed.

Current-build completed runtime evidence includes all eight specials on both
player sides, all four own lethal fatalities on both sides with fresh-match
recovery, and all four transformed lethal fatalities on both sides with
fresh-Shang recovery. Morph projectiles, timed returns and paired throws
overlapping expiry also pass both sides. See MOVES_2219_CURRENT.md.

All ten transformed-special runs `stock_wolf_2219_morphall` qualified and
the coordinator exited 0: all eight specials on both player sides, including
paired grapples, recovery, timed return, morph-art cadence and grounding.
All 16 `stock_wolf_2219_nonlethal` cases qualified and coordinator exit is 0:
eight positive Friendship/Babality/recovery cases and eight punch-ineligible
rejections. All 16 `stock_wolf_2219_stage` cases also qualified; coordinator
exit 0. Dead Pool/Tomb, missing-chord rejection, and Pit/fresh-match recovery
cover both own characters on both player sides.
323 local unit tests passed at the latest full-suite run. All four `stock_wolf_2219_ingestion` cases now
qualify; coordinator exit 0. All32 pose PNGs were individually inspected;
tested mouth alignment is visually accepted separately from machine-only
gates. See INGESTION_VISUAL_REVIEW_CURRENT.md for scope and pinned report.
No emulator remains running after this batch.

Four current Jax arm-rip victim runs also qualify: both added characters and
both sides,147 native fields, all five own body/arm phases and two detached
arm objects.28 inspected PNGs support scoped grip/shoulder-blood/collapse
placement acceptance. See ARM_RIP_REMAINING.md for report pin and exclusions.
No native ROM/art change was needed; two additional plan tests pass.

The inflation verifier now requires explicit current roles/all26 ROMs and
source/runtime/capture pins. Its former automatic visual-observation booleans
were corrected to false: visual acceptance requires actual image review.
Six ingestion/arm/inflation plan tests pass. Inflation runtime and scoped
visual review now pass as documented above; no source/ROM/art change was made
to obtain a passing result.

Remaining acceptance work includes campaign progression (Kano has not earned a
complete campaign clear), remaining victim-interaction/visual/audio review,
and final package verification. Previous 6AE0 results are historical, not
automatically current-build runtime proof. A controller's failure to beat
an opponent is not itself proof of a native game defect.

## Historical progress log (newest first)

The entries below describe earlier checkpoints. Their process-state claims,
test counts and "still needs refresh" statements apply to those checkpoints,
not necessarily the current summary above.

Four original-Liu controls now pass on2219: earned Cage/Scorpion fatalities
on both sides, original leg/torso data and stable leg anchors, native completion,
600 fresh combat fields and76800 hardware palette comparisons each. Actual26
ROM/frozen observer/source/runtime/capture pins verified.304 local tests pass.
See ORIGINAL_LEG_CONTROLS_2219.md. This is finite original-ID coverage, not
all-original/Goro/edge acceptance. Native ROM/ZIP unchanged; no emulator live.

Local development IPS ZIP and checked CMD now target2219. ZIP5577970 bytes,
SHA256 EC067104ADA2FCD1EEDA2D1E24439D6E61E120BEEF7E54CDD6A79649AB66A634;
patched archive454772BC6831B6B2F672E59F23FC5456ADCEB886CBC98FE1D8DEC4559EFD0C38.
Both independent decoders/all26 roundtrip/source diff/59 own ASM checks pass.
Exact patcher-produced archive boots stock MAME and passes earned torso-rip/
grounding/fresh-combat tests. CMD no-launch hash check and300 tests pass.
Replaced old development ZIP in place; no emulator/compiler remains. See
NATIVE_PACKAGE_2219_CURRENT.md. Broader/final acceptance remains unfinished.

Native grounding fix now built as221919459A4129FFDB37C8A3E9EC7F9AA6210D99AED00A35BC3256842C5E1F5A:
MKDEATH grounds only actual17/18 detached leg objects at four consumer sites;
shared art/upper pivots/original IDs/game rules/driver unchanged.12 fresh
Cage/Scorpion/Sub cases qualify with opaque feet exactly on the ground plane.
Independent130-object clean rebuild is byte-identical, all26 chips match
fresh runtime, and300 local tests pass. See DETACHED_LEGS_2219_CURRENT.md.
Development IPS/checked archive still6AE0 and needs refresh; Goro/original
controls and broader acceptance remain. No emulator/compiler remains live.

Actual remaining rendering defect found during fresh Cage torso-rip QA:
both own lower-leg opaque bounds extend5 world pixels below the recorded
ground plane (94-high image, yOffset-47, native spawn ground-136). Four
earned torso-rip cases pass state/completion/600-field rejoin/palette gates,
but foot-placement acceptance remainsfalse. Shared consumers traced before
editing: Goro-family rip, Scorpion swipe, Cage rip and own Sub shatter.
See TORSO_GROUNDING_CURRENT.md.297 tests pass; native grounding fix/rebuild
and affected runtime regressions are still required. ROM unchanged; no
emulator/compiler remains running. Do not mark full port complete.

Four fresh earned Jax head-clap victim/reselection cases qualify on current
stock26-ROM set, both own victims/both sides:seven ordered corpse poses,
same-field grounding, native completion,600 fresh combat fields/full initial
health/live damage/reset and77400 hardware palette comparisons per case.
Explicit finite matrix/current source-runtime-capture pins pass.292 tests
pass; one late corpse PNG inspected. See CLAP_6AE0_CURRENT.md. No ROM change
or emulator/compiler remains. All-effect cleanup/whole-port acceptance open.

Current player-two audio pairs complete:39 native/muted cluck events match,
fixed five-second post-cue PCM is identical, and all9 independent isolated
track3 tails exceed0.98. All four variants occur, filling P1's missing track3/
variant1 observation. Distinct mirrored proof names prevent overwrites; six
paired event proofs and four isolated diagnostics refreshed with current
source pins.290 tests pass. See CHICKEN_P2_CURRENT.md. No ROM changes or
remaining emulator/compiler; whole-game audiovisual/campaign acceptance open.

Normal-throw campaign completes120000 fields normally with exact earlier-route
prefix, but2111 approach fields produce zero throw requests, no Sub round win
and no advance. Closest eligible separation71 exceeds the controller gate60;
native player throw range64 versus CPU70..80 source rules explain why widening
only to64 is not a demonstrated solution. No game-range/AI change was made.

Current floor-shadow regression now passes2507 corrected pixels across four
current6AE0 captures, using explicit historical delta baselines and verified
current26-ROM/frozen-controller/position/source evidence. See
SHADOW_6AE0_CURRENT.md and NORMAL_THROW_SUB_CURRENT.md.287 tests pass. No
emulator/compiler remains; full campaign/final audiovisual acceptance open.

Current Kano normal throws against original Sub-Zero qualify both sides:
28 action fields, seven own poses,34 damage and221 grounded paired recovery
observations. Actual26-ROM/frozen observer/evidence checks added to the throw
verifier. New physical-only normal-throw campaign profile is pending under
stock_wolf_6ae0_kano_normal_throw, one hidden BelowNormal emulator.285 tests
pass. See NORMAL_THROW_SUB_CURRENT.md. Native ROM/AI/package unchanged;
no campaign win or whole-port completion is claimed.

Four fresh current6AE0 deep-freeze/shatter victim cases pass on stock MAME,
both own identities/both sides after two physical KOs:143 frozen fields,
65 native fatality fields, own legs and native completion. Explicit current
profiles/all26 ROMs/source/runtime/capture pins checked. One completion PNG
sampled visually; final ice art/audio/edge acceptance not inferred.280 tests
pass. See SHATTER_6AE0_CURRENT.md. No ROM change or remaining emulator.

All146 own linked dispatch cells now independently qualify against current6AE0
ROM bytes and compiled/generated ASM:132 main and14 special entries, with no
missing-root targets. Actual native getter immediates and true identity17/18
table entries checked; no proxy substitution.278 local tests pass. See
ALL_ROOTS_6AE0_CURRENT.md. This proves wiring, not every root's runtime/art.
No ROM changes or emulator/compiler runs; final port acceptance remains open.

Four fresh current6AE0 Liu bicycle-kick victim runs complete and qualify,
both own identities/both sides:68 action fields, five own poses, linked
reaction pointer, damage and99 paired-stance recovery fields. Verifier now
checks actual26 ROMs/stock pin/frozen observer and complete evidence hashes.
Cancelled an inefficient verifier only after all gameplay finished; hoisted
the repeated symbol lookup and successfully requalified unchanged evidence.
276 tests pass. See LIU_BIKE_6AE0_CURRENT.md. ROM unchanged; no emulator live.

Four fresh current6AE0 Raiden-tackle victim cases pass on stock MAME, both
own identities/both sides:30HP damage, paired drag distance/travel, own bodies
and native recovery. Historical dive fixture is Raiden, not Kung Lao.
Actual26-ROM/current source/runtime/capture pins pass; two contact PNGs
sampled visually.274 tests pass. See TACKLE_6AE0_CURRENT.md. ROM unchanged;
no emulator/compiler remains. Final port acceptance still open.

Four fresh current6AE0 close-shock victim cases pass on stock MAME, both
own identities/both sides:32 damage,99 attacker fields,48 palette flashes,
own bodies and paired recovery. Linked19-entry table checked; verifier now
uses explicit current runs/all26 ROMs/source/runtime/capture pins. Two PNGs
sampled visually.272 local tests pass. See SHOCK_6AE0_CURRENT.md. Production
ROM unchanged; no emulator/compiler remains running. Final acceptance open.

Four fresh current6AE0 Raiden-lightning victim cases pass on stock MAME,
both own characters/both sides:22HP damage,10 palette-flash fields, own body
identities, palette-selector restoration and stance recovery. Verifier now
requires explicit full coverage, actual26-ROM/current prerequisite hashes
and source/runtime/capture pins.270 local tests pass. See
LIGHTNING_6AE0_CURRENT.md. No native ROM changes or remaining emulator.

Four fresh current6AE0 ordinary freeze/thaw cases pass on stock MAME, both
own victims/both sides:160 frozen fields, own body shapes, changed/restored
palette selectors and native stance recovery. Verifier now requires explicit
complete actor/side coverage and checks all26 actual ROMs, current source/
runtime evidence and sampled PNG hashes. Three individual frozen/thaw PNGs
visually inspected; hardware RGB/whole-animation acceptance not inferred.
268 local tests pass. See FREEZE_6AE0_CURRENT.md. No emulator/compiler remains.

Eight transformed nonlethal recordings requalify with current source/ROM pins.
Four new current6AE0 spear victim tests also pass on stock MAME, both own
characters/both sides:8HP damage, own bodies, native pull/stun/recovery and
actual26-ROM checks. Spear verifier no longer silently uses165-era builds.
266 local tests pass. No game ROM/AI changes; no emulator/compiler remains
running. Other older interaction reports and final acceptance remain open.

Stage/morph source-pin refresh completes:36 explicit existing current6AE0
recordings requalify, including all16 stage/chord/Pit cases,4 base morph/
late-throw cases,8 extended special cases and8 transformed lethal/rejoin
cases. Stage, morph-art and transformed-finisher matrices pass. No runtime
traces, frozen controllers or receipts were modified and no emulator/compiler
was launched. See CURRENT_EVIDENCE_REFRESH.md. Remaining audiovisual,
interaction/other-report freshness and earned Kano campaign gates stay open.

Current evidence refresh: all16 special/side cells and24 recorded finisher
cases requalify against current source pins without launching an emulator or
altering runtime evidence. Ordinary lethal/positive-nonlethal matrices now
also verify every recovery-report evidence pin and current verifier code,
not merely that report's file hash.264 local tests pass. See
CURRENT_EVIDENCE_REFRESH.md for exact finite scope and remaining freshness
work. Native program/development ZIP unchanged; full-port acceptance open.

Post-Ball guard trial has completed normally at120000 fields. All123 Ball
releases and3 recovery uppercuts activate;7772 guarded post-release fields
are independently checked.39776 earlier-route rows exactly match799. No
Sub round win/map advance, so Kano's earned campaign remains open.262 local
tests pass; no emulator/compiler remains running. The completed result
supersedes the pending trial note below. Native ROM and ZIP unchanged.

Latest checkpoint supersedes historical pending entries below: all three native
cluck tracks now have isolated stock-MAME recordings. Corrected independent
validation excludes the entire alignment search;32 evaluable pre-command tails
all correlate above0.98. Production-minus-muted versus the three isolated sums
uses no fitted parameters:500755 samples, correlation0.99990287, residualRMS
0.88812 PCM units. See CHICKEN_THREE_TRACK_CURRENT.md; whole-game audio is not
accepted from this finite check. Program and development ZIP remain unchanged.

Kano post-Ball guard controller trial is pending.799 left all8793 released-phase
fields without Block/Away; the optional new physical-only profile requests
standing Block/Away after the first eight release fields, preserving charge,
activation-window and ROM/AI behavior.88 targeted tests pass. One hidden,
BelowNormal stock MAME runs; no compile or additional emulator is scheduled.

Current checkpoint: six transformed extract/kiss/laser -> freshShang cases
pass both detailed finisher and rejoin checks on stock MAME/current6AE0.
Each verifies600 live fresh-combat fields, selected AND actualShang6,
full starting health/live damage/reset state, no tracked old effects and
77400 hardware palette color comparisons. Transformed Babality positive
Kano/negative Sonya native-eligibility cases also pass both sides; source
confirms original victory-animation morph return. See MORPH_6AE0_CURRENT.md.
No emulator/compiler remains running. Campaign799 ends without a Sub round
win; Kano's earned campaign remains open. Native ROM/package unchanged6AE0.

The observation-end test no longer uses stale691-era source-pinned receipts:
five current ordinary rejoin proofs refreshed and three current morphed cases
now cover that gate. The deliberate receipt-corruption test first verifies
the untouched receipt, preventing a stale-source false positive. Native
runtime traces were not changed and no verifier hash gate was relaxed.

Refreshed-package launcher check passes the exact stock executable and
unchanged patched-archive SHA pins without opening an emulator. Fourteen
launcher/runtime-ROM-verifier/campaign-clear tests pass. The executable is
not bundled or modified; the checked local CMD still targets stock mk3 Wolf
hardware with native patched ROMs and -nocheat, never the withdrawn driver.
Campaign795 remains the single hidden/BelowNormal live emulator.

Latest checkpoint:240 local tests pass. Current6AE0 stock-MAME finite
two-sided transformed coverage includes all eight specials and four lethal
fatalities, with native nonlethal punch-history rejection independently
observed for Sonya's LP morph. See MORPH_6AE0_CURRENT.md. Campaign794 earns
one Sub round (not match);795 recovery-counter trial is running hidden and
BelowNormal. No native gameplay/AI/ROM changes.

Development IPS ZIP refreshed in place with current movelist/coverage notes:
5,572,368 bytes, SHA256868796E05D117948A6C4835B3A227C28F770EF134ED9DBCF8951C4143ED29414.
Both independent decoders,26-chip roundtrip,40 original-source diffs,59 own
ASM modules and actual787 runtime chip match pass. Patched archive remains
07A786ABBC86F1BF3625E325E8F92A016E6EDEEA5F15D4D61AD09CC65DF6F178.
No complete ROM/emulator/custom driver included; releaseReady remainsfalse.
Previous generated ZIP replaced, not archived. Final campaign/audio/broader
acceptance and source-pin freshness remain open. Entries below are historical.

Latest checkpoint supersedes historical pending notes below:791/792 both
completed and audited; Ball release activation100/100 and45/45 respectively,
but neither clears Sub-Zero.793 adaptive charge is currently running hidden/
BelowNormal. See SUB_ZERO_CAMPAIGN_CURRENT.md. Current6AE0 matched native/
control Friendship recordings complete,39 event timings match, fixed five-
second post-cue PCM window identical; overlapping early tails remain open.
See CHICKEN_REFERENCE_MODEL_CHECK.md. Native program/package unchanged6AE0.

791 is the pending unchanged6AE0 Kano/Sub charge-under-guard Ball trial;
see SUB_ZERO_CAMPAIGN_CURRENT.md. Full local discovery passes223 tests.
This harness edit can stale mutable-wrapper source pins in prior detailed
reports; their frozen runtime controllers/actual ROM/trace evidence remain,
but final source-pinned qualification freshness must be refreshed explicitly.
No native program, development IPS package, game balance or AI changed.

Current6AE0 morph refresh completes: special_p1/special_p2 and late_p1/
late_p2 all qualify on stock MAME at9000 fields. Actual current26 chips,
frozen physical controls, own identities/poses, native temporary returns,
tested Knife/Ring contact and paired-throw expiry handling pass. Both art
traces verify intermediate pose order, four-field cadence and measured
grounding. See MORPH_6AE0_CURRENT.md. No all-transformed-move/finisher,
edge/interruption/audio or whole-port acceptance follows from four cases.
No emulator or compiler remains running. The program/package remain6AE0.

Current6AE0 stage refresh completes all16 explicit cases: four Dead Pool
positives, four Tomb positives, four missing-chord negatives and four
Pit/rejoin cases. All defined native KO/command/completion/art/recovery
gates pass; Pit cases verify601 fresh combat fields with full starting
health, live damage and no retained Pit drawing shapes. This does not
certify every victim/chord/edge/allocator/audio path. No ROM changes.

Full local discovery runs222 tests with zero failures/errors/skips after
fixing test_runtime_rom_verifier.py's stale hardcoded684 archive. The test
now uses the explicit independently rebuilt current runtime reference and
verifies its unmodified archive before every deliberate corruption. This
prevents a negative sound/graphics test passing due to unrelated stale
program bytes. No production ROM verifier gate was weakened.

The current6AE0 morph refresh now runs under stock_wolf_6ae0_morph_special_p1,
special_p2, late_p1 and late_p2. Actual identity/projectile/reversion and
paired-throw expiry gates are unchanged. Art trace verification now requires
two explicit current run names instead of silently using323/324. One
hidden BelowNormal MAME at a time, no compiler; morph results pending.

Current6AE0 nonlethal refresh completes: pos_01..08 and neg_01..08 all
qualify. Positives verify native completion/reselection,600 fresh combat
fields, own identity/health/damage/reset and78000 palette comparisons;
Sonya Friendship verifies context/cue retirement. Negatives verify native
commands after punch use, two natural KOs and no nonlethal activation or
completion. Explicit current matrices pass8 positive and8 negative cells.
Full sound tails/mix, every invalid input boundary and arbitrary victims
remain outside this finite scope.120 targeted local tests pass.

Current6AE0 stage refresh now runs under stock_wolf_6ae0_stage_*: four
Dead Pool positives, four Tomb positives, four missing-chord negatives and
four Pit/rejoin cases. Both actors and player sides are required. The
matrix now takes16 explicit distinct current runs instead of hardcoded
historical indices. One hidden BelowNormal MAME at a time; no compiler,
native game/ROM, difficulty, AI or release-package changes. Results pending.

Current6AE0 nonlethal refresh started under stock_wolf_6ae0_nonlethal_pos_01
through08 and neg_01 through08. Positives require native completion,
physical reselection,600 fresh combat fields and78000 hardware palette
comparisons; Sonya Friendship also checks dance/completion-context and cue
retirement. Negatives require actual native command history and punch use,
not merely absence of activation. Both matrix verifiers now require8
explicit distinct current runs and exact kind/actor/side coverage instead
of fixed historical folder numbers.11 profile/plan tests pass. One hidden
BelowNormal MAME at a time, no ROM/AI/health/input-rule changes. Full audio,
all-invalid-boundary and full-port acceptance are not claimed. Results pending.

Current6AE0 own-fatality refresh completes: all8
stock_wolf_6ae0_fatality_01..08 cases qualify. Each verifies actual current26
ROMs, native completion, physical reselection,600 fresh combat fields,
own identities/full health/live damage/winner-death reset and78000 hardware
palette comparisons. Extraction/kiss231 action fields, laser/orb176; tracked
laser/orb effect object/process retirement also passes. Explicit matrix
checks8 distinct kind/side cells. See CURRENT_FINISHER_MATRIX.md and
OWN_FATALITY_MATRIX_QUALIFICATION.json. These are other-own-victim fixtures,
not arbitrary-victim/all-interruption/audio or full-port acceptance.
All16 finite special cells also pass on6AE0. No emulator/compiler remains
running. Nonlethal/stage/morph refresh, remaining audio/interaction checks,
Kano's earned campaign/ending and final release gates are still open.

Current6AE0 special refresh completes successfully: all14 named
stock_wolf_6ae0_special_01..14 runs qualify, covering16 distinct move/side
cells. Current26-chip verification, frozen physical controls and each
fixture's defined positive/negative/recovery gates pass. See
CURRENT_SPECIAL_MATRIX.md and SPECIAL_MATRIX_QUALIFICATION.json.
114 targeted unit tests pass. This is finite fixture coverage, not every
victim/edge/interaction/audio acceptance or completion of the full port.

The own-fatality refresh has started under stock_wolf_6ae0_fatality_01..08.
The sequential runner refuses existing MAME processes and overwrites,
requires native completion plus600 fresh combat fields, current ROMs,
own identities and78000 hardware palette comparisons. Its matrix also
requires8 explicit distinct runs, not old hardcoded folder numbers.
Only one hidden BelowNormal MAME runs at a time. No compiler is running;
development package/ROM remain unchanged6AE0. Fatality results are pending.

Current6AE0 special regression is refreshing under stock_wolf_6ae0_special_01
through14. refresh_special_regression.py checks no existing MAME before
each hidden BelowNormal launch, never overwrites evidence, qualifies each
fixture, then requires all16 move/side combinations. The matrix verifier
now requires14 explicit distinct current-run names instead of silently
reading hardcoded034F folders; ambiguous/missing fixture families reject.
New mapping/plan tests pass. No ROM, package or native acceptance flag
changed by this harness work. The old special matrix is historical until
the refreshed runtime fixtures and their source pins all qualify.

## Development package/launcher now6AE0; final release still open

The real ending-display fix and current native static presenter are now in
the development IPS ZIP. All26 independently rebuilt/copied chips match
completed stock-MAME run787. Ladder/cast/ending linked proofs are current.
ZIP5,572,129bytes, SHA256:
3532C29D0CA69AA79171E234DA9414E42C612472C04DC7291F895F33828ABD73.
14IPS/two independent decoders/full26-chip archive roundtrip pass. Actual
ZIP qualification applies40 original-source diffs and matches59 own ASM
modules; no full ROMs, custom emulator, host samples or compiler included.
The previous hash-verified generated ZIP/roundtrip were replaced, not
archived. Their contents remain reproducible from source/patch tooling.
Checked launcher now pins patched archive07A786ABBC86F1BF3625E325E8F92A016E6EDEEA5F15D4D61AD09CC65DF6F178;
stock MAME pin is unchanged. --check passes without opening the game.
The launcher test derives the expected ROM pin from verified packaging
metadata instead of retaining a stale literal across legitimate refreshes.
README/source guide distinguish observed Sonya progress from remaining
Kano/audio/broad regression/final-release gates. No final GitHub publication.

## Correction: PNG data disproves the post-restore disappearing-page diagnosis

ENDING_PIXEL_HISTORY_AUDIT.json independently decodes70 named saved PNGs.
034F/783 story intervals really are all black (null nonblack bounds).
273B/784 and785 show identical complete first/second story pixels at all
named interval samples;785's24 consecutive captures are also identical per
page despite native flipping. The partial images seen in preview output did
NOT represent the actual PNG data. The post-restore disappearance/flicker
diagnosis in historical notes below is retracted, not a remaining game bug.

787 finishes normally and exactly reproduces786's complete campaign CSV.
Its12 late captures at2574..2585 are identical to the complete second page;
both old786 and new787 sparse2580 PNGs have that same decoded pixel hash.
The120-field sample log has one VRAM-sample hash and one palette-sample hash;
video-control values1880/1884 vary. These sparse samples do not prove every
pixel or explain all control bits, and no such claim is needed to correct
the actual PNG comparison. See ENDING_LATE_DIAGNOSTIC.json in787.

Current6AE0 retains the original-style fixed-page/grab_screen presentation,
but it is not described as a necessary flicker fix. Earned Sonya story pages,
the added Kano/Sonya cast pair, sampled credits and attract return have been
observed. Kano's earned campaign/ending, final audio/interaction regression,
current package refresh and final release still remain open. No emulator or
compiler is running; the development ZIP/checked launcher are unchanged.

787 pending keeps the6AE0 ROM and earned-route inputs unchanged. The ending
state observer adds twelve consecutive late captures at ages2574..2585,
covering the troublesome sparse2580 sample. It also records120 fields
(ages2520..2639) of video-control reads, sparse VRAM grid FNV and sparse
palette-sample FNV. These are bounded read-only samples, not whole-image
hashes or proof that unsampled pixels/colors cannot change. Maximum ending
PNGs is now116; no video stream or full-match arrays are allocated.
68 coordinate/capture unit tests pass. A single hidden BelowNormal stock
MAME is running; no compiler or publication is active. The purpose is to
reconcile capture behavior before any further native rendering change.

## 6AE0 completed786: finite stability passes, sparse capture discrepancy open

786 naturally clears Kahn2–0 on attempt24, Sonya17HP, clear152720,
and returns to attract161165. qualify_ending_capture.py re-runs the current
ROM/progression audit, then verifies two distinct nonblack400x254 pages,
each pixel-identical across12 consecutive fields at ages1734..1745 and
2454..2465. All24 rows have noflip65535, autoerase0, empty object lists,
displayon1 and fixed page/clipping state. It rejects the old785 window.
Observed first/second pages show the correct Sonya photos and complete
story text; native Kano/Sonya cast and credits are visible in later captures.

Do not broaden this into full ending acceptance: sparse age2580 capture
still shows a partial photo despite unchanged static-page state. It is
not explained yet whether this is raster/capture timing or an actual
displayed-frame problem. No further ROM change was made on that inference.
ENDING_CAPTURE_QUALIFICATION.json explicitly leaves whole-ending-field,
story visual-acceptance and full-port flags false. Next investigation must
reconcile sparse/consecutive capture behavior, not merely ignore2580.

105 targeted unit tests pass. Independent clean compile73.50s/669
no-window checks rebuilds130 objects; all four ROM parts match6AE0.
Only135 hash-verified generated clean outputs (about2.8MiB) were removed
and regenerated; sources/tools preserved. No emulator/compiler remains
running. Development ZIP/checked launcher remain034F, not6AE0.

## Working static-page fix6AE0: earned replay pending

785 completed the273B earned clear normally. Consecutive ending captures
alternate complete/partial pages within1–3 fields, rather than proving
permanent disappearance after a particular age. Logged dlists, displayon,
clipping bounds and objlst2 head remain stable; pageaddr alternates and
autoerase remains1. The columns named photoX/photoY describe the list HEAD,
which can be a text glyph (225,19), not necessarily the photo. photoShape
is the raw1d0 field, not proof of the single-image record pointer.

Native MKAMODE::one_story_screen instead uses a fixed page, waits for DMA,
and grab_screen freezes the composed story during its viewing interval.
The own presenter now calls page_0_setup_no_init before composition, then
display_on/sleep4/display_off/sync_wait_dma_q/grab_screen/display_on before
the768-tick view. Generator and working UNZIP match; original ending tables
remain unchanged. Hidden build19.41s/176 no-window checks succeeds. Linked
ROM inspection verifies the new native call sequence and page records.
Working program SHA256:
6AE0A069BDFCF4AB2E2F2A1E3B0B7481735AC2654E0036D9331280037BB8BAF9.
786 pending replays the earned route with the same bounded captures/state
observer. Stable rendered pages and a new independent clean build are still
required. No package/checked launcher was changed or final success claimed.

785 pending replays273B's earned route with --campaign-ending-state,
requiring ending capture. During mode11 it records at most9600 fields of
display-list/page/autoerase/clipping pointers and first photo object state.
All inspected pointers are linked-map RAM addresses; the photo pointer is
range-checked before reads. Two12-field consecutive screenshot windows
(ages1734..1745 and2454..2465) supplement the existing maximum80 interval
captures, for at most104 ending PNGs. No inputs or guest writes are added.
This specifically investigates the partial-photo/missing-text samples;
it is not an accepted fix or a claim that capture timing is the cause.
65 campaign-coordinate/source-contract tests pass. One hidden BelowNormal
MAME is running; no compiler is running and no package was replaced.

## 273B replay and independent rebuild: pages visible but unstable

784 completes the same naturally earned Sonya Kahn2–0 clear at152720,
17HP, attempt24, and returns to attract161158. Captures at ending ages
1500/1620 show complete first photo/story;2220/2340 show complete second
photo/story. This confirms dlists restoration fixes the all-black problem.
However later samples1740..2100 and2460/2580 show only a narrow photo
strip and missing text. This remains a real presentation/observation issue
to diagnose, not visual acceptance. Do not ship or claim stable endings.
The next diagnostic should distinguish native object/display state from
capture/page timing using bounded consecutive-frame observation.
Independent clean compilation rebuilt130 objects in71.81 seconds with
654 no-window checks; all four program parts match273B byte-for-byte.
No current development ZIP/checked launcher was replaced. No emulator or
compiler remains running. Kano and final acceptance remain open.

## Working ending fix: program273B; runtime replay pending

783 reproduces782's complete campaign CSV byte-for-byte, but earned-ending
screens reveal a real defect: both own story-page intervals are black.
Winner text, the added Kano/Sonya cast pair and credits render. The root
cause is native oinit clearing dlists; the own object-based story presenter
never restored it. ending_source.py and UNZIP.ASM now restore dlists_bogus
after each page reset, before inserting photo/text objects. Source tests
and linked image/palette/page records pass. Hidden compilation completed
in23.26 seconds,211 no-window checks. Working program SHA256:
273B9BD9BA1BA7B190612A7757C4723F0E7FE0806103042B6888A3DA309E1B51.
784 is the pending earned-route replay with bounded ending captures.
Prior034F runtime proofs/package/checked launcher remain historical and
unchanged; they do not qualify273B. Clean rebuild and runtime/regression/
package refresh remain required. No final release or visual success claimed.

## Current checkpoint: program034F; final acceptance remains open

Sonya782 now has a verified earned full-ladder Kahn2–0 clear on stock MAME,
same attempt24, native two-win gameover transition152720 and attract return
161157. See KINTARO_CAMPAIGN_DIAGNOSTIC.md and that run's
CAMPAIGN_CLEAR_QUALIFICATION.json. Actual own ending-page rendering, cast
choreography and credits are still unverified; Kano's campaign remains
open at Sub-Zero. Older campaign checkpoints below are historical, not a
contradiction of this newer earned-clear result. No final release is claimed.

The entries below this checkpoint are chronological development history;
their “Latest” headings do not describe the current build. Current native
program SHA256 is
034F1179440C024A041A330F349A5F8F6C1EF3B919DC1FB701115223C15CB4F7.
The implementation is native ASM/ROM data tested with stock MAME0.289,
using its existing MK3 Wolf hardware/socket definition, not custom drivers.

Current-build finite evidence and its explicit limits are documented in:

- SPECIALS_034F_CURRENT.md: all eight specials on both player sides.
- OWN_FATALITIES_034F_CURRENT.md: four lethal finishers on both sides.
- NONLETHAL_034F_CURRENT.md: friendships/babalities and no-punch rejection.
- STAGES_034F_CURRENT.md: Dead Pool, Tomb and Pit with named cleanup gates.
- MORPH_034F_CURRENT.md: added identities, projectile and late-throw return.
- CLAPPED_LINEUPS_CURRENT.md: native Jax head-clap alignment/table fix.
- OWN_NPC_CAMPAIGN_CURRENT.md: true Kano/Sonya CPU and mirror progression.
- SHANG_CAMPAIGN_DIAGNOSTIC.md: Sonya's naturally advanced Shang2–1 win758.
- KINTARO_CAMPAIGN_DIAGNOSTIC.md: next boss trial, not a verified boss clear.

Both full campaigns, Kahn and earned endings/cast/credits remain
unverified. Finite movement/finisher fixtures are not a substitute for them.
Current Kano773 adds one naturally earned Sub-Zero round win on attempt22,
but no completed Sub-Zero match; Sonya's Shang win remains the furthest
verified naturally advanced campaign. See the per-opponent current notes.
Sonya774 now also has two verified Kintaro round wins on separate paid
attempts, not a match clear. Its first120000 fields exactly reproduce758;
the bounded extension ends150000 without Kahn or an earned ending.
Sonya776 supersedes that partial Kintaro checkpoint: a native same-attempt
2–1 win advances to Kahn's map16. Actual jump execution and unchanged
earlier trace are verified.777 extends the same strategy's observation
window for Kahn; no full clear or earned ending is claimed yet.
777 now verifies actual native Kahn combat after the exact150000-field
replay.18 rounds are lost; Kahn and earned endings remain open. That is
a controller-strategy failure, not a demonstrated native game softlock.
Broader audiovisual/edge acceptance and final release verification remain
open. Per-run controllers/receipts/ROM hashes are immutable evidence;
source-pinned report freshness must be rechecked after harness edits.

The development IPS package contains rebuildable own ASM and original-
source patches; it is not promoted as a final release. Do not infer current
acceptance from old reports or the withdrawn custom-driver release.
Compiles/tests run hidden, below normal priority, one emulator at a time.

Launcher correction: the top-level PLAY_CURRENT_NATIVE_CHECKED.cmd used
to launch the withdrawn mkport_candidate.exe/mk2ks path. It now forwards
only to romhack/port/PLAY_CURRENT_NATIVE.cmd, so both everyday workspace
CMD entry points reach stock MAME/mk3 and the native patched archive.
check_native_launcher.ps1 verifies the stock executable and exact patched
archive SHA256 before either play or --check. Both workspace --check
routes pass without opening a game window. No legacy custom fallback is
used. All70 selected campaign/launcher tests pass. The development package
has not been republished or promoted to a final release by this correction.

## Latest: both-side freezing and native lightning victim checks pass

Windowless below-normal tests160/161 place Kano/Sonya on P1 against P2
Sub-Zero. Together with158/159, both actors now pass physical ice hits on
both sides:160 frozen fields, true body/identity retained, palette restored,
stance recovered. FROZEN_VICTIM_QUALIFICATION.json records all four cases.
Tests162/163 physically select Raiden and perform native D,F+LP lightning
against each added fighter. Both run9,000 fields with zero missing markers
or illegal-opcode recovery, take22 damage, flash their dedicated palettes
for10 fields, restore normal palettes and return to stance. This exercises
the separate r_lightning use of ochar_froze_pals, not only the freeze path.
LIGHTNING_VICTIM_QUALIFICATION.json pins current program and exact scope.
Mirrored lightning, other short-table candidates and broader gameplay/
campaign acceptance remain open. No gameplay ASM or ROM changed this turn.

## Latest gameplay fix: native banked shadow reads remove floor stripes

Kano's stripes remained after thaw. Both added fighters' shadow CPU reads
were outside the stock Wolf graphics window, although body DMA rendered
correctly. Native MKDISP shad7 now selects the proper8MiB graphics CPU bank,
normalizes the address and restores all system-control bits/registers after
each header byte. The original T-unit branch stays intact. Enlarging the
loop required DSJ instead of short DSJS; hidden compile passed20.73s.
Runs158/159 pass9,000-field freeze/thaw behavior and show proper floor shadows
without stripes. Identical-controller before/after captures differ only in
the added fighter's shadow region, with zero changed pixels aboveY190.
Thirty-six bank translation/control-preservation model cases pass. See
SHADOW_BANK_FIX.md and SHADOW_BANK_QUALIFICATION.json for primary hardware
references and exact scope. Runs156/157 used the previous ROM after the first
build failed and do not count. No emulator was changed; all-pose/arena/side
coverage remains open. New program link makes older current-link reports
historical; release ZIP remains unchanged.

## Latest gameplay fix: own frozen/lightning palette lookup covers real IDs

Current-source helper audit found22 short-table candidates among80 helper
calls (45 capacity-covered,13 unresolved); these are manual-review candidates,
not an exhaustive safety proof. A concrete unguarded gap was ochar_froze_pals:
17 entries, used by normal freezing and lightning with true victim ochar.
Added dedicated65-color own frozen palettes generated from each fighter's
native primary palette, with index/transparent preservation and a blue-luma
ramp. Native MKGUYS lookup now has19 entries. frozen_palette_source.py and
prepare_game_candidate.py reproduce it; KSICEPAL.ASM joins the native link
and PBUILD. Hidden compilation passed in18.02s without a window.
Physical tests154/155 select Sub-Zero against Kano/Sonya, hit with native
ice, observe160 frozen fields each, retain true identity/own body, then restore
normal palette and stance. Compiled table entries resolve to dedicated
ffc97020/ffc97440 palettes; FROZEN_VICTIM_QUALIFICATION.json pins source/ROMs.
Trials152/153 used a20-field command exceeding the native16-field window;
they activated only normal LP and are NOT freeze passes. Controller timing
was corrected, with no state forcing. Captures inspected: blue tint visible;
Kano also shows horizontal black lines near his legs, so final visual tint/
render acceptance stays false and needs investigation. Lightning and mirrored
sides remain untested. Current source-preparation structural differences are
zero; the20 remaining short candidates need manual reachability review.
New program link invalidates previous current-link/clean-build gameplay
claims; earlier rebuild reports remain historical snapshot evidence. The
release ZIP was not replaced. Full port/gameplay/release acceptance is open.

## Latest campaign diagnosis: physical strategy also loses with original fighter

Run150 tests physical held-LK charge/release plus blocking for Kano against
Reptile, using uppercuts against Baraka. Kano beats Baraka twice; one actual
020Bh Ball activates against Reptile and produces blocked damage5, but the
attempt loses. Plans now stop waiting once a released command returns to
stance instead of always idling85 fields. No game code changed.
Explicit original-character control151 uses original Liu Kang (actor1,
originalCharacterControl=true), never a proxy for Kano/Sonya. It also beats
Baraka twice and loses to Reptile with the uppercut strategy. This shows
the current physical strategy is not sufficient even for an original fighter;
it does NOT establish complete port/CPU correctness or campaign completion.
Campaign audit now verifies all26 actual chip inputs (program, original and
added graphics, sound), checks observer code for memory/register writes, and
labels original controls separately. Both attempts have zero missing roots
and no illegal-opcode recovery. Full campaigns and ending videos remain open.

## Latest campaign checks: current-ROM natural attempts remain incomplete

Current-link Kano uppercut run146 naturally beats Baraka twice (135 and71HP
remaining), advances to Reptile, then loses. The campaign auditor previously
missed healthy-win round changes because it required an80HP refill. It now
uses native map/round counters via campaign_rounds.py, without splitting on
mid-KO score updates; all three synthetic segmentation tests pass.
Physical jump-kick exploration147 loses to Baraka; opponent-adaptive148 beats
Baraka then loses to Reptile. Sonya grapple149 loses to Baraka. All runs exit
normally with own character identity retained, zero missing roots and no
illegal-opcode recovery. These are finite loss traces, NOT campaign completion
or proof of complete CPU compatibility. No health, AI, stage or ROM writes
were used. Future windowless MAME tests now use below-normal process priority
as well as CREATE_NO_WINDOW. Need a stronger physical-input strategy and
continued native gameplay audits; full campaigns/ending videos remain open.

## Latest: all26 native runtime chips reproduced and compared byte-for-byte

Final torso/nut/impale graphics stages pass source regeneration. Torso uses
original-archive-verified native animation data plus regenerated templates;
nut/impale rebuild their indexed images from pinned draft assets in isolated
source-output directories. The palette program input is verified against
original MK3 ROM lanes. All ASM/image/socket bytes match. The final added
bank is1,856,309 bytes, SHA256 FF426E130F4F127C91B04C5DA951C4634D2B029E1600D50D354931A1CBE1C9AD.
FINAL_GRAPHICS_REBUILD.json records the complete added-bank chain.
qualify_rebuilt_rom_set.py combines independent clean program/sound output,
the regenerated eight graphics sockets and twelve unchanged original MK2
graphics sockets, then compares all26 bytestrings directly to the actual
stock-MAME test144 input archive and its receipt: every chip matches.
That test archive has six unused nested alternate-revision chips; the audit
explicitly checks the26 actual root sockets and identifies those extras.
REBUILT_ROM_SET_QUALIFICATION.json pins every chip. This closes native output
reproduction for this snapshot, NOT complete gameplay, campaigns, asset
license review, clean release packaging or release readiness. No active ROM
or release ZIP was replaced; intermediate socket copies were not written.

## Latest: clean graphics chain reproduces head, decapitation and drain stages

build_head_assets.main now accepts explicit mode/prefix/output parameters
and an option to omit intermediate socket files while preserving its default
CLI behavior. qualify_head_chain_rebuild.py validates the prior backbreaker
receipt and actual source bytes, then runs head, decap and drain builds in
sequence from the regenerated bank. All three ASM files, packed images and
all recomputed native socket bytes match current outputs exactly. The builder
also independently decodes every packed pixel index back to its readable PGM
source. HEAD_CHAIN_REBUILD.json records the scope; socket copies are not
written (18MiB of duplicate intermediate files avoided). Torso/nut/impale
closure and full visual/gameplay/campaign/release gates remain open.
No active art, program ROM, sound ROM or release ZIP changed.

## Latest: clean graphics chain reproduces authored Pit/backbreaker stages

build_pit_assets.build now accepts an explicit regenerated prefix; its
standalone source/manifest checks are unchanged. rebuild_backbreak_data.py
is a pure, side-effect-free PGM/data builder for the same six authored
backbreaker frames and native script; it explicitly fixes the established
CRLF ASM output format and checks native socket reassembly.
qualify_pit_backbreak_rebuild.py validates the prior friendship receipt and
actual prefix bytes, regenerates both stages, and compares all ASM/image/
socket bytes against current outputs. Both pass. Only packed images, ASM
and metadata are persisted in the same clean chain; socket comparisons stay
in memory, avoiding another12MiB of intermediate copies. This is source/data
reproduction, not expanded runtime/edge/victim acceptance. Head/decap/drain/
torso/nut/impale closure and full gameplay/campaign/release gates remain open.
No active program, graphics ROM, sound ROM or release ZIP changed.

## Latest: clean graphics chain also reproduces babality, HUD names and friendship

Extended qualify_finisher_graphics_rebuild.py through generate_baby_data,
generate_hud_names and generate_friendship_data. All five downstream stages
(finisher/kiss/baby/names/friendship) now reproduce their packed images,
six ASM files and every native socket byte-for-byte. HUD palette input comes
from the independently regenerated clean program source, not a new ROM dump.
The names retain the original SCORE_P palette indices and shadow pixels.
Generators can omit intermediate socket files; comparison remains byte-level
in memory, avoiding18MiB of duplicate socket files for these three stages.
Remaining pit/backbreak/head/decap/drain/torso/nut/impale stages are still open.
This proves rebuilding of these assets only, not visual/gameplay acceptance.
No active ROM, source-linked gameplay ASM or release ZIP changed.

## Latest: regenerated graphics chain reaches finisher and flame-kiss stages

qualify_finisher_graphics_rebuild.py validates the independent fighter and
portrait receipts and their actual bytes, hard-links those prefixes into one
small graphics_chain root, then re-executes generate_finisher_assets and
generate_kiss_data using native_art_records and original MK3 art inputs.
All three generated ASM files, both extended graphics images, and every
recomputed native socket match their current stage outputs byte-for-byte.
Intermediate socket files are compared in memory, not written as duplicate
6MiB sets. The first run exposed missing readonly SONYA_SPECIAL art-table
metadata in the standalone parser; added that address, verified the incomplete
scratch bytes against current outputs, and resumed in the same directory.
FINISHER_GRAPHICS_REBUILD.json records both stages. Remaining baby/name/
friendship/pit/reaction/head/torso/nut/impale stages are not yet certified by
this chain. No active graphics, gameplay code, ROM or release ZIP changed.

## Latest: native fighter-art import no longer loads the old driver builder

Replaced import_character_art.py's dynamic execution of the legacy
tools/build_mk2ks_mk3.py with native_art_records.py: a small readonly parser
for original MK3 image descriptors, composite lists and aligned art pointers.
It contains no executable relocation or driver/donor-code generation.
qualify_fighter_source_rebuild.py reimports user-supplied MK3 art in the clean
root: KANOART.ASM, SONYAART.ASM, fighter_graphics.bin and all eight stage
sockets are byte-identical. It checks the legacy module was not imported.
Six synthetic tests cover pointer alignment, signed coordinates, native
full/skip records, invalid descriptors, composite references and bounds;
all pass. Complete downstream graphics regeneration remains open. This
changes the build dependency only, not artwork, gameplay ASM or live ROMs.

## Latest graphics-source closure: portraits no longer need the old release ZIP

Losslessly exported the two54x72 indexed portrait sources and original
RGB15 palettes to assets/selector_source (PGM plus SOURCE.json). This is
data migration, not changed artwork. The old UI container had additional
data; the manifest separately pins the exact8040-byte portrait prefix,
not a false claim to reconstruct the entire242495-byte legacy container.
import_selector_art.py now reads the explicit indexed source files and
reconstructs/validates that prefix without reading a player release ZIP.
qualify_selector_source_rebuild.py rebuilt in isolated graphics_ui: KSUI.ASM,
the portrait-extended graphics image and all eight native sockets match
existing portrait-stage outputs byte-for-byte. It reuses the existing fighter
prefix, so full graphics closure remains false. No active ROM changed.
The first check stopped on an overbroad whole-container hash assertion;
it was corrected to the portrait-prefix hash. The incomplete scratch outputs
were verified against existing outputs and reused, not accumulated in another
build directory. Other graphics stages/source dependencies still need auditing.

## Latest: clean own-WAV-to-DCS-ROM sound rebuild is byte-identical

prepare_clean_sound_check.py replays all four authored staging stages in the
isolated clean root. It verifies439 original CMPs and tool/config inputs
against the pinned supplied archive, regenerates ten added PCM clips from
their WAVs, reconstructs byte-identical playlists, and imports neither own
compressed samples nor candidate sound ROMs. Original CMPs/tools use hard
links, avoiding a duplicate input bank. The working SoundW MK2.LOC differed
because it is generated placement metadata; the clean input starts with the
archive's original LOC and lets original PLBUILD regenerate it.
The hidden sound-clean target passes in17.67s with no window. All ten PCM
inputs and all four1MiB sound ROMs match current outputs byte-for-byte;
CLEAN_SOUND_INPUTS.json / CLEAN_SOUND_QUALIFICATION.json pin evidence.
Combined with the earlier program proof, program and own-sound build paths
are now independently reproduced. Graphics closure, final mix/provenance,
campaigns and full gameplay/release acceptance remain open. No live ROM or
development release ZIP was changed by these isolated checks.

## Latest: clean regenerated-source program rebuild is byte-identical

`prepare_clean_program_check.py` generated241 source/config files in isolated
baseline/clean_program, importing no objects or linked program outputs.
Original tools were hard-linked, not duplicated; only the small split config
and IRW input were copied. The hidden below-normal clean target compiled all
123 linked objects, linked and split ROMs in69.14s, creating no window.
`qualify_clean_program.py` verifies input/source hashes, success marker and
all required objects: all four262,144-byte P12F8/FC parts match current ROMs
byte-for-byte. CLEAN_PROGRAM_INPUTS.json and CLEAN_PROGRAM_QUALIFICATION.json
record evidence. This closes program-source compilation equivalence despite
textual declaration/comment differences. It does NOT prove clean graphics
or sound rebuilding, complete gameplay acceptance, or release readiness.

## Latest: in-memory preparation audit found and repaired rebuild drift

- prepare_game_candidate.main(audit=True) generates241 source/config files
  entirely in memory; it does not overwrite srcp or create another source tree.
  audit_source_reproduction.py saves exact source diffs and a separate token
  triage.212 files match after line-ending normalization;29 differ textually.
- Fixed the generator's missing Sonya char_hik_open route to ks_sonya_block
  (already present in tested srcp). Added explicit52-module object order in
  native_module_order.txt, checked against the full generated module set,
  replacing filesystem/glob iteration order that would change the program link.
- After these repairs, structural token differences are zero. Remaining
  textual differences include comments, ref/def grouping/placement, data-row
  wrapping and DOS EOF newline. This is NOT compiled byte-equivalence proof:
  exact source reproduction remains false, cleanRebuildVerified remains false.
  Next gate is independent assembly/link comparison from regenerated sources.
  Current gameplay ASM/ROM and development patch ZIP were not changed here.

## Latest: flame-kiss fire loss is a proven native flawless-tone replacement

At frame5438 the game emits call579; the original playlist explicitly plays
flawtone on track2, the same track as fire2025. This replaces fire before
its3.85s source finishes. An independent4096-sample fire fit after the entire
victim reference and before that command matches .99693. After separating
the paired voices, full kiss matches .98889, full victim .98211, and fire
through50ms before replacement .98603. Sound output latency remains under
0.1s. A later isolated win window confirms/removes its voice independently.
The diagnostic now asserts those bounds, waveform scores, playlist routing,
ROM hashes and the two natural-KO gameplay receipt. It labels fire as a
verified native interruption, NOT a full-file match. Final mix/other victims
and full audio acceptance remain open; audioQualified stays false. No ROM
change was necessary in this investigation.

## Latest flame-kiss audio measurements: cue start proven, late fire unresolved

`inspect_dcs_kiss_audio.py` pins current game/sound ROMs and identical readonly
controllers in144/145, and reads only one six-second recording window.
Original codec correlations are .98836 kiss/.98646 fire/.98256 victim.
The actual kiss prefix matches .99506 with30ms latency. The new win voice
matches .99742 in a later isolated window, but removing it does not recover
the fire's final section: fire reference3.0–3.5s correlates only .0307.
Mixed fire windows0–2.75s retain expected negative gain, with2.5–2.75s
correlation .956; victim windows also show expected gain but are mixed.
The late fire loss/mismatch remains unexplained; do not claim complete
fire or victim playback qualification from commands or these partial fits.
The diagnostic saves all measurements with audioQualified=false. Next:
separate paired burn voices and trace the late loss against actual DCS
track events before choosing a source fix. No ROM changed this turn.

## Latest: own flame-kiss DCS cues built and phase-triggered

- `extend_dcs_kiss.py` stages pinned existing kiss/fire/victim WAVs through
  original HENRY/PLBUILD into own playlists2021..2029. Authored dcs_source.py
  and staged MKSOUND.ASM add main-table slots101h/102h/103h with priorities
  sp_attkv1/sp_effect/sp_reacv1 and duration86/234/168. SoundW stays unchanged.
- Authored and staged KSKISS.ASM use own kiss at orb launch and own fire/victim
  calls at burn contact instead of generic projectile/fire/death sounds.
  Hidden game/sound builds passed without creating windows.
- Current-link tests144/145 both pass the natural two-KO flame-kiss gameplay
  qualification:231 action fields,60 orb fields,116 burn fields, native
  completion, no missing roots. Passive sound observation records kiss2021
  at5221 and fire2025/victim2029 at5281. These calls are NOT yet waveform
  playback proof; paired fire/victim mix and full tails still need checking.
- Earlier audio reports pin the previous link/bank and are historical again.
  The development patch ZIP remains unchanged and unpromoted.

## Latest Square audio resolution: exact silent padding contaminated the metric

The later music-only comparison is bit-identical (zero difference norm),
so no persistent sample drift was observed. At frame5761, every nonzero
sample of the resampled Square reference (bounds1461..43905 inclusive)
matches at .994516. Unrelated audio in its exact trailing zero padding
caused the .80944 whole-file score. The verifier retains that failed score
and labels this outcome separately; it does not call it a full-file match
or discard quiet-but-nonzero voice samples. Current result:10 full-file
matches,1 complete-nonzero-waveform match,1 proven Finish Him pre-emption.
No threshold reduction and no ROM changes. Native cue proof is current;
final mix and complete-port/release acceptance remain open.

## Latest Square audio investigation: win-overlap hypothesis rejected

Independent fitting/removal of Sonya's win voice after the Square launch
leaves the frame5761 full-clip score exactly .8094434646350254. The win
overlap does NOT explain this failure. Both runs send original end-music
call24 at frame5771; music timing/divergence remains a candidate, not a proven
cause. Direct native-only waveform correlation is .16514 because the voice
is embedded in the native mix, so that is not a valid clean-reference bypass.
The qualifier continues failing rather than relaxing its threshold. See
generated_dcs/SQUARE_OVERLAP_INVESTIGATION.json. No ROM changed here.

## Latest checks: Sonya win passes; Square audio overlap needs investigation

- Current-link runs140/141 pass complete selection names and Sonya-win
  waveform matching (Sonya-win .98958), plus all eight full Bicycle cries
  above .98 after independent launch subtraction. Bicycle gameplay passes.
- Current-link runs142/143 pass the12-activation Square gameplay regression.
  The stricter full audio checker FAILS at launch frame5761 (.80944 full
  correlation), with no matching native Finish Him pre-emption. Both runs
  issue new Sonya-win call2018 at frame5811,50 fields after this launch;
  the candidate contains that extra voice and the original-bank control does
  not. This is a concrete overlapping-signal candidate, not a proven cause
  or accepted Square audio result. Do not reuse the older pass as current.
- Next: isolate the concurrent announcement in this bounded recording,
  distinguish mixing from genuine truncation, then rerun strict audio checks.
  No game/sound ROM changed in this check batch. Release remains unpromoted.

## Latest: selection speech spacing and complete Kano-win audio checked

- Own selection speech processes now wait72 fields instead of48; original
  roster speech keeps48. Sonya-name to Kano-name command spacing increases
  from0.877s to1.316s, enough for the1.15s name clips, without blocking selection.
  Both the authored integration and staged MKSEL.ASM contain this change.
- Hidden native compile passed. Current-link runs138/139 each complete9,000
  fields and pass the physical Kano Ball command/hit/recovery regression.
- Full announcement waveform matching passes both names(.9936/.9912) and
  two actual Kano wins(.9922/.9806). One win's short prefix scored only.8543;
  full mode requires the complete waveform score instead of asserting a
  clean prefix in a mixed recording. All complete references fit the capture.
- Sonya win had prefix proof on the previous link; her full tail and the
  latest-link Square/Bicycle audio regressions remain open, as do final mix,
  campaigns and wider port/release gates. Development IPS ZIP is unchanged.

## Latest: own native announcer routes implemented and partially waveform-tested

- `announcer_source.py` appends four boss-voice slots5Bh..5Eh to the second
  native sound table, explicitly routes IDs17/18 in selection, and fills
  their winner_speech entries. Fresh preparation invokes this same integration.
- `extend_dcs_announcer.py` stages four pinned existing voice clips through
  native PCM/resampling and playlists2009..2020. Original HENRY/PLBUILD sound
  build and native game assembly/link both pass hidden with no windows.
- Runs134/135 each completed9180 fields and passed the Bicycle behavior
  regression. Captured native audio prefixes match Sonya name(.99986),
  Kano name(.99066), Sonya wins(.99223), all below0.1s output latency.
- Kano win runtime proof, complete announcement tails, selection speech
  spacing/mix, and other release gates remain open. New link invalidates old
  current-link claims; earlier Square/Bicycle waveform receipts are historical
  until rerun against the newest bank. Existing IPS ZIP stays unpromoted.

## Historical: announcer routing defect before the implementation above

`audit_announcer_routes.py` pins current source and the four available
selection/win voice clips. Native select_speech adds1Ch to the selected ID:
Kano17 reaches triple_sndtab2 index2Dh (cursor flash), Sonya18 reaches2Eh
(player joins). Both winner_speech entries are zero. The existing move-sound
extension uses triple_sndtab, NOT triple_sndtab2. Correct implementation must
append own boss-voice entries to the second table, explicitly map the two
selection IDs and winner entries, and compile the four own DCS playlists.
`generated_dcs/ANNOUNCER_ROUTE_AUDIT.json` records exact entries and hashes;
this is source-level diagnosis, not a voice playback acceptance claim.

## Latest: native Bicycle launch and caught-move cry observed

- Expanded isolated SoundP with own KSBL/KSBC playlists using original tools;
  native KSBIKE.ASM emits entry/catch calls, no emulator-side samples or hacks.
- Current-link stock-MAME tests128/129 passed both 9,000-field gameplay
  regressions (11 activations, 352 paired fields, hit/block/miss/recovery).
- Bounded A/B waveform diagnostic pins program/sound ROMs and observer;
  all 11 launch prefixes match above .98 and eight caught-move cry half-second
  segments match above .99 after independently removing overlapping launch.
  Event counts align with real action entries; no extra cry on blocks/misses.
- Square regression on the expanded bank now passes: runs130/131 each have
  12 physical activations, with 11 complete launch waveform matches and one
  prefix match followed by the observed native Finish Him interruption.
  The audio verifier pins the expanded playlist and all three sound-table rows.
- Complete Bicycle cry recordings now pass in extended runs132/133: eight
  full waveform matches above .98 after independent launch subtraction.
  Capture extends180 fields with neutral controls; original behavior checks
  remain on the first9,000 fields. No game code or sound bank changed here.
- Final mix, remaining
  move audio, full campaigns and the wider release gates remain open.
  Existing IPS development ZIP remains the prior, unpromoted snapshot.

## Latest: first own ROM-native DCS cue built and waveform-qualified

- Added isolated soundp candidate using original HENRY/PLBUILD, not custom MAME
  samples. prepare_dcs_candidate.py stages Sonya Square launch WAV hash540AB92C...
  via pinned polyphase resampling to31,250Hz PCM16, explicit peak normalization
  from1000 to16384, and439 hard-linked original CMP inputs. Existing soundw and
  the prior IPS ZIP remain unchanged. Final gain/mix and voice provenance open.
- HENRY raw-PCM input verified experimentally against original reference decode.
  Own KSSQ.CMP compiles124 codec frames; native region123 frames/2822bytes.
  PLBUILD generates four real1MiB DCS ROMs with new calls2000/2001/2002 on native
  tracks1/2/3. Original-tool masked and EPROM passes require MSK/LOC inputs;
  staging includes them. Hidden sound build20.82s/no window succeeds.
- dcs_source.py extends native triple_sndtab with indexFE,priority sp_attkv1,
  duration59,basecall07d0h. SONYAMOV.ASM invokes tsoundFE after init_special_act;
  fresh candidate preparer includes the source extension. Hidden game build
 23.20s passes/no window. Current lanesE04067B89C4D983BD4730D30183612F91C0D2BDB4B1D7E6118744A896850BFEF
  /262064DCD8004DA33F6FDBBE4BB3A6D73F2F70DB2FF3C615DD97B79DD24641B4.
- Native126 (--sound-candidate) and control127 (original soundw) each complete
 9,000 stock-MAME fields/12 actual Square launches and pass command/hit/recovery
  checks. Passive port observer returns no value and never alters guest writes.
  Both receive identical native commands; only four sound ROMs differ.
- qualify_dcs_square_audio.py pins source/codecs/program/graphics/sound/emulator/
  frozen controller/WAV hashes. HENRY source->decode correlation0.98752 at16sample
  delay. Native-minus-control WAV matches11 full launch clips at>0.95 correlation.
  Last launch has physicalKO and native FinishHim on same track at+0.18s;
  pre-interruption prefix correlation0.99785 proves audible onset, not fullplay.
  Checker requires actual KO/announcer event for that exception. No host samples.
- Analysis reads at most1.36s per WAV at once. No giant full-match float arrays.
  NATIVE_DCS_AUDIO.md documents commands, original tools, reference docs and scope.
  -Target sound-info and -Target sound retain all hidden/priority/runtime bounds.
- This is one qualified audio cue, not full sound acceptance. Native soundp is
  still explicitly selected with --sound-candidate; default/control soundw and
  previous ZIP/local launcher remain frozen pre-audio artifacts. All other audio,
  final mix/provenance, broader gameplay/campaign/AI/visual and clean release
  gates remain open. Older program-link receipts are historical, not current.

## Latest: native IPS development package round-trips and runs in stock MAME

- package_native_patches.py produces one4.8MiB development ZIP (not final/public
  release):14 IPS patches (2program,8added-graphics,4DCS),12 original MKII graphics
  copy mappings,26 target chip hashes,52 linked own ASM modules,34-file native
  source diff, PBUILD/link configuration, patch/play scripts and instructions.
  No complete ROMs, custom emulator, host samples or proprietary tools included.
- ips_codec.py strict bounded IPS encoder/decoder has5 synthetic tests passing:
  literal/RLE limits, truncation/extension, reservedEOF address, randomized edits,
  malformed/truncated/trailing/overflow records. test_patch_native_roms.py has8
  passing safety tests for hashes, bad patches/results, unsafe/duplicate names,
  missing chips, overwrite refusal, deterministic ZIPs and untouched inputs.
- patch_native_roms.py validates all required source chips, patch hashes and
  resulting bytes before output creation; never overwrites an existing output.
  Source ROM archives remain read-only. Both own strict decoder and independent
  prior generic IPS decoder reproduce every target patch exactly.
- Actual patched26-chip ROM set equals current compiled/tested chips byte-for-byte.
  Runner's explicit --prepatched-rom verifies and uses that existing archive, not
  a silently reconstructed one. Projectiles124 and SonyaDeadPool125 each complete
  9,000 stock-MAME fields and pass behavior qualifiers on the patcher output.
- qualify_native_patch_package.py validates the ZIP's exact file/hash inventory,
 52ASM snapshots, absence of complete ROM/emulator payloads, and applies the
  byte-preserving native source diff to the supplied archive in a temporary test
  directory. All34 patched files match current native sources apart from CRLF.
  Fixed an initial encoding issue rather than accepting a text-only comparison.
- ZIP:development_patches/MK2KS_NATIVE_DEVELOPMENT_IPS.zip,5,068,236bytes,
  SHA875C61F55CED7C79CACB1406F9CD723F678C048DEE45BB7939854EA695748218.
  PACKAGE_QUALIFICATION.json pins this artifact and both patched-ROM runtime
  receipts. PLAY_CURRENT_NATIVE.cmd launches the local tested copy on demand;
  no interactive emulator window launched by packaging/tests.
- Clean full rebuild/source dependency closure and remaining gameplay/campaign,
  audio/visual/AI acceptance are still open. This development candidate does NOT
  mark the goal complete, replace final-release gates or get published to GitHub.

## Latest: Dead Pool native Wolf gate/timer fixed and physically qualified

- Found actual inherited T-unit input read in MOVES.do_uppercut: Wolf LP/LK
  are bits16/17(P1),20/21(P2) of switch, not switch2/DIP. deadpool_source.py
  applies an explicit .if wunit main-word read/shift before unchanged P1/P2
  mask. Original T-unit else branch and all other native stage gates retained.
- After chord fix, both added victims and original Liu control were cut off
  before skeleton appearance. Read-only Timer114 confirms master countdown6..1,
  f_thatsall0, heldChord3, hidden victim, f_death0. Existing136-field allowance
  expires12 fields before native completion. Wolf-only BGND.r_fall_in_slime
  allowance now256; T-unit136 unchanged. No forced flag or replacement sequence.
- Reproducible source helpers wired into prepare_game_candidate.py. Two hidden
  builds19.88/21.67s pass/no windows. Latest program lanes
  69CA39DA295AEDB5FE4537988350FEA962B437F7352BBB42C7CD6AAC35DFF6B0
  /1922BDBC20B512FD6C2944AD3471F632A557078870DE0F09BAFAF36633DF32E6.
- DeadPool115Kano/116Sonya/117P2Kano/118P2Sonya/120originalLiu control and
  visual122P2Sonya complete9,000-frame runs. qualify_deadpool_runtime.py pins
  current full ROM/emulator/controller; verifies actual linked Wolf read,
  other gate/source preservation, two natural KOs, correct own victim identity,
  chord3, slime50ah action, own visible poses, disappearance and skeleton's
  native f_deathffff. No guest writes/missing/recovery markers. Final122 capture
  deferred2 fields to avoid framebuffer lag; inspected separately.
- NoChord119 physical negative passes: actual uppercut, chord0, no slime action
  and no native completion flag. Initial109..114 failed fixtures/controls retained
  as diagnostic evidence, not accepted gameplay passes. Controller holdsLP+LK
  BEFORE KO; fresh LP duringFinishHim would finish normally. Approach70 avoids
  native repel blocking the earlier overly-close55 target.
- LateCapture123 passes the same current-ROM qualifier. Captures20/40/80 fields
  after completion; inspected20/80, including native skeleton rising from acid
  at80. Initial2-field completion capture was too early to show the emergence,
  not a missing skeleton. Full pixel/alternate-costume acceptance remains open.
- TombRegression121 passes18,000 fields, four natural KOs, native rematch,
  own Sonya performer/Kano victim,64-field spike sequence/completion. Original
  Tomb gate still rejects its command on Dead Pool. Updated qualifier pins current
  sockets instead of stale friendship generation. DEADPOOL_NOTES.txt documents
  inputs/source rationale/evidence and open scope. No release/full-port claim.
- Earlier special/campaign receipts are historical after this program relink.
  Full campaign, broad edges/victims/AI/audio/visual and ROM-patch release gates
  remain open. Special-root actual14-cell static check passes current link.

## Latest: both actors naturally beat first CPU and advance ladder; campaign open

- Reworked campaign_probe.lua navigation to BFS over actual KSNAV directions,
  replacing guessed horizontal presses. Added grapple/uppercut controller styles,
  read-only state-guided inputs, round-reset handling and exact terminal-row plus
  campaign_end.txt capture. Runner exposes --campaign-uppercut. No ROM changes.
- First grappling/rushing cases104..106 lost to CPU Baraka. Kept failed receipts;
  did not classify process exit0 as a gameplay pass. Stationary crouch/uppercut
  defense107Kano/108Sonya wins Baraka's two rounds, then naturally advances0->1
  and enters a match against Reptile with the true selected IDs17/18 preserved.
- audit_campaign_run.py pins stock emulator, frozen controller, current program
  lanes and full sockets; verifies true actor IDs and0 missing/recovery markers.
  Ladder advance additionally requires two observed CPU health0 winning rounds
  with player health remaining. Both107/108 pass that finite progression check.
- Kano107 first CPU winning-round minimum HP57/11; Sonya108 57/57. Both then
  lose to Reptile. maxMapPosition1 is NOT full campaign completion, and
  fullCampaignVerified/fullPortVerified remain false. No health/stage/AI writes,
  cheats, continues, forced wins or fixture injection. All tests windowless.
- Current gameplay ROM unchanged from special-root link7D91F6.../EE629F...;
  earlier thirteen special/finisher regression cases remain current-program
  evidence. Need stronger physical controller tactics or independent full-run
  evidence for later CPU opponents and bosses; other release gates stay open.

## Latest: native own special-root dispatch wired; thirteen current-link cases pass

- special_root_contract.py documents seven actor-specific anitab2 slots:
  travelling/strike/grab special, fatality1/fatality2, friendship intro and
  projectile impact. No Liu slot semantics or donor body pointers substituted.
  Existing exact own scripts now fetched through native get_char_ani2 in all14
  callers; subsequent multi-phase scripts and consumers remain unchanged.
- generate_roster_roots.py links all66 main and7 own special entries per actor.
  complete now describes root coverage only; playable/fullPortVerified remain
  false. qualify_special_roots.py verifies actual getter MOVI operand, original
  nineteen-character table IDs17/18, all14 actual linked dispatch cells and
  exact staged caller sources. Projectile allocator preserves thrower ochar.
- Hidden dummy-video/audio/below-normal build21.84s passes/no window. Current
  lanes7D91F61431AA47103139DFC3B74523C964FDB071588841A881B31347EA192B60
  /EE629F40986551D72D897B16DA6144ABD1D8FF3A33A65DA122B0B304A0ED48E4.
- Thirteen physical stock-MAME9,000-frame cases91..103 complete: projectiles,
  ball,square,blade,bike,choke,leg,extraction,kiss,laser,orb,Kano/Sonya friendships.
  Existing specific behavior qualifiers pass after full-current-program/socket
  pinning in qualify_special_root_regressions.py (projectiles separately).
  Checks include own art/IDs, finite hit/block/whiff/interruption where each
  fixture covers them, paired grip/damage/recovery, four fatality completion and
  two friendship completion/owned-effects retirement. No guest writes.
- Updated old finisher/friendship qualifiers to pin authoritative current socket
  hashes rather than obsolete partial graphics generations. Removed stale
  cross-feature implementation booleans; each receipt states only its own scope.
- Original special-root caller inventory captured in SPECIAL_ROOT_QUALIFICATION;
  originalCallerReachabilityFullyAudited remains false. Mirrored current-link
  regression, broader victims/edges/AI/campaign, audio, visual and clean ROM-patch
  release acceptance remain open. Earlier program-link receipts are historical.

## Latest: own impalement linked and four physical stock-MAME cases pass

- build_impale_assets.py converts hash-pinned three-pose drafts per actor using
  one scale per actor, original body palettes, readable PGM sources and typed
  KSIMART.ASM image/composite records. Preserves exact native21-long two-part
  script and native XY lift adjustments, separate native Baraka weapon.
- Appends38,914 bytes after unchanged1,817,395-byte nut prefix. Eight stock
  socket images round-trip; qualify_impale_assets.py independently reassembles
  sockets, verifies zero padding, exact PGM/6bpp decode, six actual-ROM headers,
  own palettes, both3bh dispatch cells and native scripts. Preview inspected.
- Hidden dummy-video/audio/below-normal compile passes24.94s/no window.
  Current lanes:00233FE5E9AD30A7D401B895A51681D8E4F77914A34DEF05E131B1E8106E35AE
  /B7D25FA498D682924394A03370CE8860B7E5A3EDA5BAB2E3C95C51A8161ACC95.
- KanoArt87/SonyaArt88/KanoMirror89/SonyaMirror90 complete stock-MAME runs;
  qualify_impale_runtime.py pins current lanes/sockets/emulator/controller and
  verifies correct IDs17/18, all3 own poses,80/84/557 observations, exact native
  Y lift92,68,44,20 and final slide20..34, native completion,0 missing markers,
  no guest writes. Initial/lifted Kano/Sonya and mirrored Kano captures inspected.
- Both actors now66/66 main roots; seven special roots remain explicitly marked
  missing pending native caller/ABI audit. Full pixel/alternate-costume and broad
  gameplay/release acceptance remain false. Earlier-link receipts are historical.
- Current runner/graphics_metadata now use generated_impale. Fixed nut asset
  qualifier to read component metadata separately; nut asset regression passes.

## Latest: own impalement source drafts created, not yet linked

- Used built-in image_gen under imagegen skill to create three new suspended
  suffering poses per actor. Costume/identity references are existing own Kano
  nut and Sonya backbreak drafts; no weapon is painted into victim artwork.
- assets/impale_draft contains both versioned transparent PNG atlases, exact
  KANO_PROMPT.txt/SONYA_PROMPT.txt and DRAFT_MANIFEST.json with source/prompt
  hashes and per-cell alpha128 bounds. inspect_impale_drafts.py validates RGBA
  and reports all six poses have no opaque cell-edge contact. Inspected output.
- These are source drafts only: no ROM or dispatch changes, no runtime claim.
  Next encode with one uniform scale per actor, native body palette and original
  21-long impalement grammar, append after unchanged nut graphics, then hidden
  compile and physical-controller own-victim/mirrored stock-MAME qualification.
- Compile launcher verified hidden/dummy video+audio/below-normal priority with
  explicit refusal if a compiler window appears. No compile run this step.

## Latest: original impalement reference captured and ABI audited

- Added --impale-victim --stock-victim controller using physical Baraka3/Liu1
  selection,2 naturally won rounds,B,F,D,F+LP at<=136 native range. Read-only
  object observer follows actual native3bh composites; no guest writes.
- LiuReference86 completes9,000 stock-MAME fields. Three pose captures inspected:
  weapon is separate native Baraka art; body lifted high before final slide.
  audit_impale_reference.py pins current program/sockets/emulator and verifies
  exact21-long two-part native script, component counts1/2/1 and completion.
- IMPALE_REFERENCE_AUDIT.json records actual geometry/control and observations:
  phase0 80fields/Y92,68,44,20; phase1 84fields/Y20; phase2 557fields/Y20..34.
  Original images have optional palette tails, so audit reads only fixed14-byte
  headers rather than treating next-image data as palette pointers.
- Own3bh remains missing. Next author3 full-body suffering poses per actor with
  separate weapon excluded, preserve this exact grammar and native origins,
  then hidden compile and actual own-victim/mirrored tests. No stand-in mapping.

## Latest: mirrored Kano nut reaction and current Sonya immunity pass

- KanoMirror84 and SonyaRegression85 each complete9,000 stock-MAME fields and
  qualify:46 split-action fields/34 damage for Kano versus34 fields/0 damage for
  Sonya,221 grounded idle recovery observations,0 markers/no guest writes.
- qualify_nut_assets.py independently reassembles8 sockets, checkszero padding,
  decodes actual graphics back to exact readablePGM hashes, verifies actual-ROM
  geometry/SAG/palette pointers, both131px ground pivots and5-long two-part script.
  Both poses use identical source scale. Full visual/alternate-costume acceptance
  remains explicitly false; this does not close the full gameplay/release gate.
- Final missing main3bh audit: native LK impalement uses3 full-body poses with
  component counts1/2/1, first pose143px high; first phase4 pose0 records with
  XY adjustments(-96,16),(0,-24),(0,-24),(16,-24), then0. Second suffering phase
  [0,1,2,1,0,1,2,0]. MKDEATH stores phase2, matches victim with Baraka, lifts via
  native double_mframew, repeatedly suffers at2/4/6/8 rates, then slides victim
  down and completes. Need original-victim reference capture and own3-pose art
  per actor before integration; do not reuse nut/stumble as impalement art.

## Latest: Kano own nut-punch sprites linked and first physical test passes

- build_nut_assets.py converts the hash-pinned two-pose draft to readable native
  palette-index PGMs using one uniform scale, own feet-center pivots and131px
  ground plane. Preview inspected. KSNUTART.ASM preserves native two-part script
  [pose0,pose1,0,pose0,0]. Independent6bpp decode/8 socket round-trip checks pass.
- Appends14,242 bytes after unchanged1,803,153-byte torso prefix, no driver hooks.
  Current/fresh sources link Kano main36h; both actors now65/66 main entries.
  Main3bh impalement and7 special-root caller audit remain pending.
- Hidden compile20.15 seconds succeeds/no window. KanoArt83 completes9,000
  stock-MAME fields/no guest writes; qualifier verifies actual5-long root script,
  both own poses during406h reaction,34 damage,46 Cage10ah fields,221 grounded
  native idle recovery observations,0 missing markers. Capture inspected.
- Added current_graphics.py so runtime qualifiers pin current nut sockets and
  byte-identical torso prefix rather than stale graphics generations. Earlier
  test receipts are historical after relink. Mirrored Kano, current-link Sonya
  immunity, detailed geometry/color/alternate-costume acceptance still open.

## Latest: Sonya immunity qualified; Kano nut-punch draft generated

- qualify_nut_immunity.py pins current ROM lanes/sockets/stock emulator, checks
  Sonya's native female root36h==37h own alias, and requires actual Cage10ah move,
  no406h male reaction,0 damage and221 grounded idle recovery observations.
  Sonya80/Mirror81 pass9,000 fields/34 split-action observations. LiuControl82
  uses the same physical LP+Block fixture:46 action observations,34 damage,
  actual406h reaction and221 grounded recovery. Thus immunity isn't a missed input.
- Used built-in image_gen under imagegen skill for TWO new Kano nut-punch poses,
  referenced authored back-break costume/style. Preserved generated PNG and exact
  prompt in assets/nut_draft; SHA777E2840EC67B422754F5D8BB36D06BB893C86FE4212C47FF1F1F61AC1BFE028.
- inspect_nut_draft.py verifies RGBA, hash and two non-edge-touching alpha128 bounds:
  first[490,9,951,686],second local[170,136,612,686]. Apparent top-edge red noise
  is below cutoff; opaque silhouette is not clipped. Draft visually inspected.
  Not encoded or linked yet, visual/runtime acceptance=false. Next uniform-scale
  palette-index conversion, own ground pivots and native two-part36h script.

## Latest: Sonya follows native female nut-punch immunity

- Source MOVES do_jc_split explicitly rejects Kitana/Mileena/Jade via useless_splits.
  Added Sonya18 to that same branch in current source and fresh prep. No changes
  to male damage/reaction paths. Original MKFN a_nutcrunched is an empty label
  aliasing a_bike_kicked; Sonya main36h now explicitly aliases her own bike-victim
  root, preserving native female behavior instead of inventing a male reaction.
- Hidden compile21.93 seconds succeeds/no window. NutSonyaImmune80 uses physical
  Cage selection/approach/LP+Block;9,000 stock-MAME fields,34 native10ah split-punch
  action observations, victim HP stays161,0 markers. Formal immunity/recovery
  qualifier and mirrored case still next; not a full move-set acceptance claim.
- Mirrored blade-fury Kano78/Sonya79 on preceding link also qualify:all3 own
  victim poses,40 damage,221 grounded recovery observations,0 markers; native
  attacker action durations62/52 respectively. Those receipts predate immunity relink.
- Remaining main state:Kano36h nutcrunch plus both3bh impalement;7 special-root
  audit and broader audio/AI/campaign/visual/source-patch release gates remain open.

## Latest: physical blade-fury reactions pass for Kano and Sonya

- Added --shred-victim [--sonya] [--mirror] controller using real Baraka3 selection,
  approach and B,B,B+LP (native MOVES scom_shred34-field window). No guest writes.
- Kano76/Sonya77 each complete9,000 stock-MAME fields and qualify_shred_runtime.py
  passes:49 native11dh action fields,all3 own victim poses,40 damage,221 subsequent
  observations with both fighters grounded and native303h idle,0 missing markers.
- Qualifier pins exact current program lanes,8 sockets and stock emulator SHA.
  Kano mid-shred framebuffer inspected. Mirrored/edge/block/interruption and final
  visual acceptance remain open; this finite test does not certify full gameplay.
- Remaining main36h nutcrunch/main3bh impalement and7 special-root audit still
  pending, along with all-move audio, CPU/campaign and final source/patch release.

## Latest: actual native blade-fury reaction grammar integrated

- Source audit confirms main25h a_shredded is Baraka blade-fury's shaking victim
  loop, NOT a dismemberment asset and NOT a generic short stumble. Native loop
  uses LKSTUMBLE1/2/3 with alternating(+6,+6)/(-6,-6) adjustments and ani_jump.
- generate_shred_reactions.py derives explicit one-to-one own pose mapping from
  already-translated native a_lkstumble/main23 five-pose family, preserving exact
  native shake grammar instead of aliasing that ordinary terminated animation.
  KSSHRED.ASM linked through current and fresh build paths;64/66 main each now.
- Hidden compile17.42 seconds succeeds/no window. qualify_shred_link.py verifies
  both actual-ROM root cells and exact14-long sequences, signed packedXY fields,
  own pose pointers and self-loop targets. This is linkage, not physical proof.
- Next physical Baraka shred victim tests; main36h nutcrunch/main3bh impalement
  remain missing,7 special-root caller audit remains open. Sonya immunity still
  under investigation; no speculative female-rule patch has been made.

## Latest: native projectile roots integrated and physical regressions pass

- Main26h/27h now bind own release/effect scripts,63/66 main entries per actor.
  KSPROJ actual actions fetch main26 via get_char_ani and main27 for effect object
  allocation. Sonya charge callback/restoration is in native animation source;
  full charge/release timing unchanged. Fresh prep includes generated KSPJROOT.
- Hidden native compile22.73 seconds succeeds/no window. Actual-ROM qualifier
  verifies4 dispatch cells,26 effect-palette image aliases, own composite lists,
  two terminated effect phases and body release/charge-restoration scripts.
- ProjectileRoots74/Mirror75 each pass9,000-field physical hit/block/cleanup tests:
  19 activations per actor,3-field knife/15-field ring spawn latency,22 unblocked
  damage/5 blocked damage, correct own IDs/art, wrong-direction rejection,
  recovery/no duplicate live projectiles/0 markers. Qualifier now pins current
  program lanes and torso graphics sockets rather than accepting stale receipts.
- No custom emulator hooks or extra graphics bytes. Remaining main25h shredded,
  36h nutcrunch,3bh impaled and7 special roots still open. Native launch audio,
  all interrupt/spacing cases, full AI/campaign/visual/release gates remain open.

## Latest: typed own projectile-root source prepared, not yet linked

- generate_projectile_roots.py reads existing typed own art/animation sources,
  emits generated_projectiles/KSPJROOT.ASM plus PROJECTILE_ROOTS.json. Main26
  body scripts use actual own release poses; Sonya includes charge-palette callback,
  own4 charge frames, native palette restore and own release frame.
- Main27 has two explicitly terminated effect phases per actor, not flight-loop
  aliases.26 typed image-header aliases reuse original graphics/geometry/control
  but point to knife/ring effect palettes; composite wrappers remain explicit.
  Kano phases6intro/10flight; Sonya4intro/4flight. No new pixel bytes/driver hooks.
- These sources are NOT staged/linked yet, and root missing markers remain active.
  Next bind native26/27 roots and adapt actual own projectile release actions to
  consume main26 so physical move tests exercise the new roots. Then hidden build,
  actual-ROM descriptor/phase/callback validation and real projectile regressions.

## Latest: mirrored swipe and landed pixel captures pass finite checks

- KanoMirror72/SonyaMirror73 each pass9,000-field torso qualifier:all7 own phases,
 455 stationary legs,406 grounded final-upper observations, fatality2 completion,
 0 markers/no guest writes. Added readonly settled-pose capture two fields after
  descriptor/position reaches stage ground; inspected both mirrored landed images.
- These close finite player-side cases, not lower-foot/style/alternate-costume
  or full port acceptance. Current-link Cage71 and historical pre-anchor
  61/63/64/65 remain distinct evidence sets.
- Remaining projectile-root audit: native main26h is body release composite list;
  main27h has TWO terminated phases (intro then flight), not an ani_jump loop.
  Existing own ks_knife_release / ks_ring_charge/release are body-compatible,
  but binding ks_*_flight directly to main27h would violate phase grammar.
  MKZAP also dereferences first composite descriptor icmap for projectile palette,
  whereas own direct projectile actions explicitly switch effect palettes.
  Need typed projectile-palette descriptor aliases plus two-phase source scripts
  and caller audit before declaring these slots implemented; leave markers active.

## Latest: separate Scorpion final-anchor fix passes Kano/Sonya runtime

- build_torso_assets.py emits two extra final-frame descriptors plus one composite
  per actor for main41h only. Same pixels/SAG/palette, yOffset-16 accounts for
  Scorpion's+64 process ground versus Cage's+80. Main39h retains original own
  final anchor; packed graphics/socket hashes unchanged.
- Hidden native compile19.44 seconds succeeds/no window. qualify_torso_link.py
  verifies all32 descriptors,16 composites and4 own script/root bytes including
  explicit Scorpion16px final delta. No MAME driver code or guest writes.
- Current-link KanoSwipe69/SonyaSwipe70 each pass9,000-field qualifier:all7 own
  phases,454 stationary leg observations,405 final-upper observations exactly on
  native ground, fatality2 completion/0 markers. KanoCage71 regression also passes:
  547 stationary legs,456 grounded final-upper observations, fatality1 completion.
- Mirrored swipe cases, final landing pixel capture/opaque-leg placement and
  alternate costumes still open; numeric ground proof is not full visual acceptance.

## Latest: mirrored Cage passes; Scorpion swipe activates and exposes anchor split

- KanoMirror64/SonyaMirror65 each pass9,000-field Cage qualifier:547 stationary
  own-leg observations,457 final-upper grounded observations, required6 own phases,
  completion/0 markers. Thus finite Cage cases cover both actors/player sides.
- Added physical --swipe-victim controller: Scorpion10, charge HP>=40 fields,
  D,F,F,F then release atclose<=69, verified MOVES sc_hp_open/scom_sc_db2.
  First66 pressed HP after Finish Him and ended normally;67 carried HP across
  round reset and stopped attacking. Controller68 now holds through KO but resets
  when next round restores health. No game code or guest-state writes involved.
- KanoCharge68 completes9,000 fields: native fatality2 active96 observations then
 65535,0 markers, own upper/leg objects. Native Scorpion adds64 to p_ganiy, while
  Cage torso_bounce adds80. Shared own final-upper descriptor was calibrated for
  Cage: swipe finalY149+ownbottom51=200 vs native floor216,16px high. NEXT make
  a state-specific final-upper descriptor/composite for main41h with bottom67,
  keeping Cage root/art/pixels unchanged, then test both actors and mirrored.
  Scorpion detached legsY85 also differ from CageY80; retain separate visual gate.

## Latest: original Cage reference and finite Kano/Sonya torso tests qualify

- LiuReference62 uses real selection/command; readonly observer follows native
  main39h offsets to track its original upper/leg composites. Native detached legs
  remainY80 too. Original LKDEADLEG1A/B descriptor bottom143 extends below216;
  screenshot inspected. A bounding-box bottom alone does not prove bad placement.
  Own bottom141 retained pending opaque-foot visual comparison, not blanket-shifted.
- Native MKREACT torso_bounce explicitly adds80 to p_ganiy, then ground_player and
  torso_flat before native bounce. Own final upper bottom51/52 correctly meets216
  atY165/164; detached legs remain fixed at ground-136 throughout.
- qualify_torso_runtime.py pins current program/sockets/stock emulator/no writes,
  requires the6 actual Cage-consumed own phases0/1/2/3/5/6, simultaneous own legs
  and upper, native completion and0 markers. Kano61/Sonya63 each pass9,000 fields:
  547 stationary-leg observations and456 final-upper grounded observations.
  Lower opaque-foot placement explicitly unaccepted; mirrored Cage and Scorpion
  main41h remain next. No full visual or port acceptance claimed.

## Latest: linked torso ABI checks and first physical Cage case complete

- qualify_torso_link.py reads actual interleaved ROM: verifies4 own dispatch
  pointers, exact generated typed script bytes (including adjust/callback tokens),
  28 image header/SAG/palette records and14 composite lists/terminators.
- --torso-victim physically selects Cage2, wins2 rounds and performs native
  D,D,F,F+LP at<=68px (MOVES jc_lo_punch/scom_jc_db1 source verified).
  Kano61 completes9,000 stock-MAME fields/no guest writes, fatality1 active185
  observations then65535,0 missing markers. Own upper/lower composites observed.
- Detached own legs are objectY80, stage216: provisional descriptor bottom141
  extends to221, five below native floor. Need calibrate against original stock
  stump/capture before finalizing lower pivot; final own upper settlesY165 with
  own bottom51 =>216, so do not apply a blanket vertical shift to both sections.
  First detached-leg screenshot inspected; no full runtime/visual qualifier yet.
  Sonya, mirrored Cage and Scorpion secondary/raw consumers remain pending.

## Latest: native multipart torso data/scripts linked

- build_torso_assets.py emits28 native image headers across14 own composites,
  preserving counts2,3,1,2,2,2,2 per actor. Independent6bpp tile decode/reassembly
  proves every source pose exactly; all8 stock sockets round-trip and previous
  1,760,020-byte prefix unchanged. Appended43,133 bytes; total1,803,153.
- KSTRART.ASM translates native MKLK main39h/main41h typed source, preserving
  adjustment tokens, callbacks and phase terminators while replacing composites
  with own upper/lower art and own initial high-hit recoil. No Liu image refs.
- Main39h/41h now linked:61/66 main entries each; remaining main25h,26h,27h,36h,3bh
  and7 special roots still pending. Fresh prep/current runner stage torso data.
  Hidden native compile18.24 seconds succeeds/no window. This is linkage only.
- Need actual-ROM multipart/script qualification and physical Cage/Scorpion
  fatalities, including all native secondary/raw component consumers, floor
  pivots and costume colors. No torso runtime acceptance claimed. Historical
  runtime receipts predate this relink; qualifiers now pin current torso sockets.

## Latest: own torso frames encoded as readable palette sources

- generate_torso_sources.py emits14 standalone PGM frames from hash-pinned
  preserved source art:6 uppers plus1 lower stump per actor. Palette-index preview
  inspected. TORSO_SOURCE.json records crops/scales/geometry/component counts,
  PGM/index hashes and explicit runtime/pivot acceptance=false.
- Kano wound guide classifies only cyan-guided authored-red pixels; these map to
  original native pens48/46/63, verified RGB-identical in both original costumes.
  All non-wound pixels use nearest own primary colors, transparent0/colors1..63.
  No palette edits, invented pixels, old driver payload or executable words.
- Native component counts2,3,1,2,2,2,2 retained as encoder requirements, not yet
  tiled/linked. Lower pivot141 and final-upper own ground-80 remain provisional
  until actual native caller coordinate observations. Main39h/41h still missing.
- NEXT: multipart tile builder plus typed raw descriptor list/own composite root
  source for native main39h and41h, hidden compile and real Cage/Scorpion tests.

## Latest: remaining reaction audit; authored torso inputs preserved

- No verified own nut-punch pose mapping found in existing MK3 translation data;
  main36h remains missing rather than aliasing an unrelated crouch/stumble pose.
- recover_torso_sources.py preserves5 hash-pinned standalone authored images in
  assets/torso_sources: two six-pose upper atlases, two lower stumps in one atlas,
  and Kano wound-classification guides. All3 sprite sheets visually inspected.
  No legacy runtime payload, opcode array or driver mutation is consumed.
- TORSO_INPUTS.json records source paths/hashes/cell geometry and explicitly says
  generatedROMData/runtimeVerified=false. These inputs can supply both Cage
  main39h torso-rip and Scorpion main41h swipe; neither root is implemented yet.
- Native main39h has multiple adjustment/terminated phases plus standing legs;
  main41h is six upper composite poses then0. Encoder must preserve typed raw
  component consumers/part counts, with separate own wound/costume colors,
  before native integration/runtime qualification. Main36h still needs own art.

## Latest: both drain victims pass finite native tests on both player sides

- qualify_drain_runtime.py pins actual program lanes,8 sockets and stock MAME/no
  guest writes, verifies own drain_table/alternate_suck_pals entries, exact9-long
  shrink scripts and6 native image headers/pivots/palette/SAG pointers.
- Sonya57/Kano58 and mirrored Kano59/Sonya60 each pass9,000-field physical tests:
  exact compressed pose sequence0,1,2,1,0,1,2,skeleton; own phase counts14/22/24;
  shared skeleton479 observations; native lifted originY66; completion/0 markers.
  Both code paths for right-side palette selection execute across these cases.
- Mirrored Kano final-shrink screenshot inspected. This proves finite native
  choreography, not full visual acceptance or alternate-costume correctness.
  Remaining seven main roots, special-root caller audit, all-move/AI/campaign,
  detailed visuals and final source/ROM-patch/release qualification still open.

## Latest: original drain reference establishes intentional lift; own pivots fixed

- Added readonly tracking of native drain_table poses and shared a_final_drain
  composite; --drain-victim --stock-victim physically selects Liu1 for comparison.
- LiuReference55 completes9,000 fields. Original shrinking frames stay at objectY66
  and shared skeleton likewise; original screenshot confirms deliberate levitation.
  MKFX.TBL SOULSUCKHO1/2/3 dimensions49x125,50x119,50x113 have origins(-2,5),
  (-2,3),(-3,1). CORPSE1A is52x108 at(-3,-1). Do not reset object to standing floor.
- Corrected own same-height drain descriptors to native lifted origins rather than
  standing131/132 bottom anchors. Pixels/socket hashes unchanged; ASM header pivots
  changed. Hidden native compile21.41 seconds and linked geometry checks pass.
- SonyaPivot57 completes9,000 fields: own three shrinking frames14/22/24 observations,
  shared skeleton479 observations, all at nativeY66. Final own shrink framebuffer
  inspected. Formal current-ROM drain qualifier, Kano repeat and both mirrored
  palette paths still pending; no full visual/gameplay acceptance claimed.

## Latest: physical Shang drain activates against Kano; positioning under review

- --drain-victim controller selects Shang6 and own victim17/18 via native KSNAV,
  physically wins two rounds, holds Block for Up,Down,Up+LK. Command/range<=80
  verified directly from MOVES st_lo_kick/scom_st_db1; no guest writes.
- stock_drain_kano54 completes9,000 stock-MAME fields, fatality1 active203 fields
  then65535,0 missing markers. Own shrinking composites observed in object trace.
  No full drain qualification yet: final skeleton, both palette paths, Sonya and
  mirrored cases still require specific observations and screenshots.
- Native main38 lead-in adjustment sum leaves own victim originY66; new art's
  own131px ground plane renders bottom197 vs stage216. Need compare original
  victim's native pose/final-skeleton choreography before changing vertical
  offsets: body-only origin reset could misalign the shared skeleton handoff.
  Do not mistake fatality completion/zero markers for accepted position/style.

## Latest: native soul-drain lead-in/shrink data linked

- generate_drain_reaction.py emits own main38h reaction with typed native
  ani_adjustxy grammar, own recoil and dizzy composites, no Liu composite refs.
  Root coverage59/66 main each; seven main/seven special roots still pending.
- MKFX drain_table16->19 and alternate_suck_pals12->19 include explicit own
  shrink scripts/body palettes. Original rows unchanged; intervening alternate
  rows use native TMG_SK development defaults, not accepted hidden-victim art.
  Fresh prep includes tables and both KSDRAIN/KSDRART source modules.
- Hidden native compile18.27 seconds passes/no window. qualify_head_link.py
  verifies actual-ROM main38h root,17-long reaction structure, both9-long shrink
  loops,6 image headers and both19-row source tables, alongside head/body checks.
  Runner uses generated_drain sockets; qualifiers pin that new graphics set.
- This is NOT drain runtime acceptance. Need physical Shang command controller,
  own shrink-frame/position/palette/skeleton observations and mirrored tests;
  inherited native lead-in adjustments are explicitly pending own calibration.

## Latest: drain caller grammar audited; own shrinking graphics encoded

- Native MKDEATH do_drain first consumes main38h lead-in, then MKFX drain_table
  supplies a separate two-section shrinking script, then shared a_final_drain
  skeleton. drain_table has16 pointers and alternate_suck_pals has12: both must
  gain explicit own entries before runtime testing. Do not close root38h merely
  by installing the shrinking loop.
- build_head_assets.py --drain emits generated_drain/KSDRART.ASM:6 own image
  descriptors/composite wrappers and own scripts matching native MKFX sequence
  [0,1,2,0terminator] / [1,0,1,2,0terminator]. Appends25,622 bytes after unchanged
  1,734,398-byte decap prefix; total1,760,020. Independent6bpp pixel decode and
  all8 stock socket round-trips pass. No executable driver code imported.
- Not yet linked: main38h reaction/own lead-in choreography,16/12-row table
  extensions, native build integration and physical Shang tests remain next.
  Current game/test runner still correctly uses previous generated_decap set.

## Latest: current Kano tongue passes; standalone soul-drain art recovered

- KanoCurrent52 passes current-link9,000-field physical tongue qualifier:7 body
  poses, own head, completion,488 grounded observations,26 head-path observations,
  0 missing markers/no guest writes. Four current normal/mirrored tongue cases
  are now recorded (Kano52/51,Sonya49/50); visual contact acceptance remains open.
- Found existing hash-pinned authored soul-drain drafts. generate_drain_sources.py
  consumes only those two PNGs and original palette data, producing6 readable
  native-index PGMs, provenance/geometry hashes and inspected palette preview in
  assets/drain. Uniform per-frame downsampling; transparent0/colors1..63; own
  foot-center pivots and131/132 ground plane. No legacy driver payload imported.
- Source preparation only: main38h still missing. Next audit native drain caller
  grammar/adjustments, append these own three-phase frames as typed ASM/stock
  sockets, integrate source roots and test physical Shang fatality. Do not count
  recovered art as an implemented or runtime-accepted state.

## Latest: mirrored tongue runtime and native head lifecycle checks pass

- SonyaMirror50 and KanoMirror51 each complete9,000 stock-MAME fields on current
  ground-corrected link:7 own body poses, own upright head, native completion,
  489 body observations grounded216,0 missing markers/no guest writes.
- Strengthened tongue qualifier checks26 own-head observations:20 observations
  retracting monotonically toward Reptile, then6 at native mouth placement, and
  head removal while body remains. Source tproc9 explicitly repositions the head
  with match_ani_points/adjust_xy_a5 after deleting tongue; this is a separate
  phase, not a retraction reversal bug. Sonya49/50 and mirrored Kano51 pass.
- Sonya normal/mirrored contact screenshots inspected. Detailed contact alignment
  remains visually unaccepted; functional observations do not close that gate.
  Kano normal47 is historical pre-Sonya-ground-change; current-link normal Kano
  and alternate palettes still need fresh verification, alongside remaining states.

## Latest: Sonya tongue grounding corrected from physical runtime evidence

- Tongue-specific qualifier now requires the one upright head actually consumed
  by native Reptile (not seven rolling-head frames), all7 own body poses in order,
  correct identity, fatality1/completion, preserved original16 source lineup rows,
  explicit19-row typed table and current-ROM/socket hashes.
- Kano47 passes on its historical link. Sonya48 exposed a real one-pixel vertical
  error: victim objectY85+own132=217 vs native stage ground216. Fixed Sonya lineup
  deltaY=-1 to account for Reptile131 vs own132 offsets, in current source and prep.
- Hidden native rebuild17.11 seconds succeeds/no window. SonyaGround49 passes
  9,000-field physical stock-MAME test:7 own body poses, own upright head, native
  completion,488 body observations grounded at216,0 missing markers/no guest writes.
  Mirrored tongue cases and detailed contact-point visual calibration remain open.

## Latest: Reptile tongue victim table extended; Kano runtime activates

- MKDEATH head_lineups now has19 explicit eight-byte rows; original16 unchanged,
  Jade plus own Kano/Sonya main10 second-pose records appended. Own(-187,0)
  alignment is provisional and still requires visual calibration, not a final
  acceptance claim. Fresh native-source preparation includes these entries.
- Hidden compile17.95 seconds succeeds/no window. --tongue-victim uses physical
  Reptile selection and native B,B,D+LP at160..224 range, verified from MOVES.
- stock_tongue_kano47 completes9,000 stock-MAME fields/no guest writes; native
  fatality1 observed187 fields then completion65535,0 missing markers. Own head
  and final body objects observed; first head-separation screenshot inspected.
  Sonya, mirrored cases, formal tongue-specific qualifier and alignment pixel
  acceptance remain pending. Existing fan qualifier must not be applied unchanged
  because tongue consumes only upright head, not the seven-frame rolling loop.

## Latest: both decapitation victims pass both sides on palette-fixed link

- Current-link KanoPalette43, SonyaPalette44, SonyaMirror45, KanoMirrorPalette46
  each pass9,000-field physical Kitana decapitation verification:7 own body poses,
  7 own head rotations, native completion,0 missing markers, no guest writes.
  Sonya's final framebuffer inspected: own green costume/skin/head colors correct.
- Strengthened qualifier requires each body observation to preserve the actual
  fatality-stage ground plane, from native ground_y at first own body frame:
  objectY+131(Kano)/132(Sonya)==216 for all486/487 body observations per case.
  Do not compare with next stage's232 ground_y after transition.
- Native selector alternate palette is conditional on same-character P1/P2, not
  a generic Start modifier. Kitana-versus-added-victim tests do not exercise it;
  alternate death colors remain source/ROM verified only, not runtime accepted.
- Reptile16-row head_lineups extension/calibration and other missing victim states,
  all-move/CPU/campaign and final release/patch acceptance remain open.

## Latest: native bloody-palette bounds fixed; Kano colors corrected

- Extended MKGUYS bloody_palettes15 to19 rows, preserving original15 verbatim.
  Added Noob/Jade valid native palettes for intervening IDs and own primary/alt
  palettes for17/18. Authored neck wounds already use own body indices, so normal
  costume colors are the correct mapping for these sprites. Fresh prep includes it.
- Hidden compile22.62 seconds passes/no window. qualify_bloody_palettes.py checks
  source length/original preservation and relocated native ADDI table pointer,
  all4 own pointers, Noob original-pair equality and valid Jade palette header.
- Current-link stock_fan_kano_palette43 passes9,000-field decap qualifier: all7 body
  poses, all7 head rotations, completion, no missing markers. Final collapse
  framebuffer inspected: previous red/yellow corruption gone, own costume/skin
  and head colors visible. Sonya/alternate-palette captures remain to repeat;
  broad visual/fatality/campaign acceptance is still not complete.

## Latest: complete body/head runtime observations; bloody palette defect found

- Added read-only object-list observations for fan fatality, independent of
  selected-player globals after native death_blow_complete. Later collapse
  sections were not absent: the old fighter-state filter stopped observing them.
- qualify_decap_runtime.py pins current program lanes,8 graphics sockets, stock
  emulator SHA/no guest writes; requires all7 own body poses in first-seen order,
  all7 own head rotations, correct victim identity, native completion and0 missing
  markers. Sonya40, mirrored Kano41 and KanoCapture42 each pass9,000-field runs.
- Deferred two-field captures now cover all14 first-seen descriptors/poses.
  Inspected final Kano collapse capture: geometry/head objects present, but colors
  are visibly wrong (bright red/yellow). Thus fullVisualAcceptance remains false.
- Confirmed MKGUYS change_to_bloody_pal directly indexes bloody_palettes by ID;
  table has only15 two-long rows and no extension in fresh prep. IDs17/18 read
  palette words as pointers. NEXT: explicit own primary/alternate bloody palette
  entries and safe intervening rows, source+ROM table checks, hidden relink and
  repeat pixel inspection. Also Reptile head_lineups16-row extension remains.

## Latest: physical Kitana decapitation against Kano activates

- Added --fan-victim [--sonya] [--mirror] to the real-controller runner using
  canonical KSNAV directional maps and native Block,Block,Block,HK. Command and
  72px native range verified against MOVES fn1_hi_kick/bcom_fn1_db2 source.
- First stock_fan_kano38 did not activate: controller tried to reach55px despite
  normal collision spacing. Corrected controller target70px, no game-code change.
- stock_fan_kano39 completed9,000 fields on unchanged stock MAME, no guest writes,
  native fatality2 active120 observations then death65535. Actual own main3ch
  pose0/1/2 pointers observed48/6/1 fields, zero missing markers in fatality trace.
  Remaining body sections and loose-head object animation still require explicit
  observations and pixel checks; not yet a complete fatality-victim acceptance.
  Sonya/mirrored cases and16-row Reptile alignment-table fix remain open.

## Latest: own decapitated-body scripts linked; Sonya regression passes

- Recovered three hash-pinned authored PNGs into assets/decap; fourteen readable
  palette-index PGM body frames and provenance/geometry manifest. Preview inspected.
  First Kano sheet's connected final pair deliberately excluded in favor of the
  separately authored last-two sheet. Body pivots use131/132 own ground planes;
  native gameplay calibration remains required.
- build_head_assets.py --decap appends42,569 bytes after the unchanged head prefix,
  total1,734,398. Independent pixel decode and8 stock socket round-trips pass.
  KSDCART.ASM preserves the original three-section main3ch grammar exactly:
  0,1,2 / 3,2,3,2,3,2 / 3,4,5,6, each terminated separately.
- Main3ch now binds own bodies:58/66 main entries each. Fresh prep/current runner
  include data. Hidden compile20.54 seconds succeeds without a window.
  qualify_head_link.py verifies actual-ROM root3ch/3dh cells, all body scripts,
  composite terminators, image headers and palette/SAG geometry.
- stock_decap_link_sonya37 passes current-link9,000-field physical Jax vs Sonya
  regression:3 poses,58 action fields,32 damage,221 grounded recovery observations,
  0 missing markers. This is not a decapitation runtime test.
- Caller audit found native MKDEATH head_lineups has only16 eight-byte rows;
  Reptile tongue fatality indexes directly by victim ID, so17/18 are unsafe there
  despite linked own art. Extend using measured own victim alignment before
  claiming tongue/decapitation compatibility. Full fatality/campaign acceptance
  remains open; no custom driver or guest writes used.

## Latest: native head data linked; current-link back-break regression passes

- build_head_assets.py appends6,906 bytes after the byte-identical1,684,923-byte
  back-break prefix. All14 frames independently decode to source indices; all8
  stock sockets round-trip. Total packed graphics1,691,829 bytes.
- KSHDART.ASM contains typed image headers and two direct seven-frame ani_jump
  loops, not multipart wrappers. Main3dh now binds the own head roots:57/66 main
  entries per actor. Fresh-candidate preparation and current runner include them.
- Hidden native compile succeeded27.95 seconds, dummy video, no window.
  qualify_head_link.py verifies both linked root cells, exact loop longs and all14
  descriptor geometry/SAG/control/palette fields from actual interleaved ROMs.
- stock_head_link_backbreak36 passes the current-link9,000-field physical Jax vs
  Kano regression:3 own poses,58 action fields,32 damage,221 grounded recovery
  observations,0 missing markers. Stock MAME/no guest writes. This regression
  does NOT exercise severed heads: native decapitation gameplay and missing
  main3ch body art remain open, as do broader port acceptance gates.

## Latest: standalone authored head sources recovered

- generate_head_sources.py consumes only three hash-pinned authored PNGs and
  original body palette data; no legacy driver payload or executable blobs.
- assets/heads now contains preserved source PNGs, fourteen readable palette-index
  PGM frames, provenance/geometry hashes in HEAD_SOURCE.json and an inspected
  palette preview. Seven native rotation phases per actor; Sonya's three corrected
  diagonal source images are included. Transparent0, body colors1..63.
- This is source preparation only. Main3dh is still unbound: the next step is a
  direct-descriptor seven-frame native loop (not multipart pose pointers), packed
  graphics append/independent decode checks, native relink and real-input victim
  tests. Decapitated-body main3ch remains a separate missing state. No gameplay
  completion or visual acceptance is claimed by the source manifest.

## Latest: mirrored and front-boundary native back-break cases pass

- Current-link P2 Jax versus Kano32 and Sonya33 each pass9,000-field finite
  native back-break verification. All3 own poses,58 native action fields,32 damage,
  completion/recovery and221 grounded observations, zero missing/recovery faults.
  Qualifier now records the actual Jax player side; CSV columns remain normalized
  actor/victim roles rather than physical P1/P2. Mirrored Kano arch capture inspected.
- Front-edge fixture physically walks to the boundary, observes30 stationary
  fields while away is held, releases it, then schedules the simultaneous jumps
  and native Block command. Kano34 reaches rightX1098 (Jax1035), and mirrored
  Sonya35 reaches leftX60 (Jax122). Both pass the same9,000-field native checks;
  recovered victim remains inside the observed front boundary and both fighters
  are grounded throughout the221-observation recovery window. No guest writes.
- qualify_backbreak_assets.py independently decodes all6 packed6bpp payloads
  back to the exact PGM indices/hashes, re-interleaves all8 stock sockets, verifies
  zero padding and byte-identical preservation of the earlier graphics prefix.
  BACKBREAK_ASSET_QUALIFICATION.json records this source/format proof, not visual
  acceptance or full gameplay acceptance. No new program link this turn.
- Finite normal, mirrored and front-edge cases now cover both added back-break
  victims. Interruption, broad CPU/ladder/campaign behavior, remaining animation
  states and final visual/rebuild/patch/release acceptance still remain open.

## Latest: native back-break art/scripts integrated and finite runtime passes

- Six draft-derived sprites now compile into readable palette-index PGM sources
  under assets/backbreak and typed generated_backbreak/KSBKART.ASM descriptors.
  Native1..63 body-color indices and transparent0 are used; no MAME hooks.
  Original low-alpha noise inflated initial bounds; the compiler now applies
  the same128 alpha cutoff before measuring/cropping. Corrected preview inspected.
- Packed graphics preserve the previous1,656,943-byte Pit prefix exactly, append
 27,980 bytes, total1,684,923. All eight unchanged stock Wolf sockets round-trip.
  Runner uses this new graphics set; prior component receipts are historical.
- Main3fh now binds each actor's own three-pose script, preserving all native
  a_back_broke control items: repeated pose0, adjustY10/48, pose1/pose2, terminator,
  and reverse second phase. Root coverage56/66 main per actor;10 main and7 special
  roots still pending. This closes a state, not the full port/release gate.
- Hidden native compile passes20.46 seconds. Kano Art27/Capture29 and Sonya
  Art28/Capture30/Display31 each pass9,000-field qualify_backbreak_runtime.py:
  actual P1 Jax109h action58 fields, all3 new own poses,32 damage, completion,
 221 settled grounded observations, no missing/recovery/out-of-ROM execution.
  Verifier pins program/gfx hashes, main3fh pointer, exact13 linked control longs,
  frame geometry/SAG/control/primary-palette pointers and actual runtime state.
- Early pose snapshots led pixels by two fields; observer now queues captures
  two fields after descriptor changes, including short poses that already advance.
  Sonya Display31 confirms the extended arch actually renders, not just its
  pointer. Full digitized-style/pivot acceptance, mirrored Jax, stage/edge,
  interruption and CPU/campaign coverage remain open; finite pass is not release.

## Latest: dedicated back-break art drafts prepared, not ROM-enabled

- review_backbreak_parts.py renders the actual native Liu three-pose back-break
  and each added actor's original digitized composite candidates. Own generic
  fall poses do not provide the complete compact/recline/extended-arch sequence;
  they were not relabeled as a completed back-break reaction.
- Used the built-in image_gen skill/tool (no API/CLI fallback) to draft exactly
  three own-character poses each, following native pose silhouettes and original
  Kano/Sonya costume references. Kano received a targeted face/belt refinement;
  the original oversized hardware was not accepted as final identity styling.
- Selected draft PNGs, exact final prompts and DRAFT_MANIFEST.json are saved in
  assets/backbreak_draft. record_backbreak_drafts.py verifies genuine RGBA
  transparency and three separated sprite bands per asset, recording hashes,
  bounding boxes and partial-alpha counts. Original reference component metadata
  is retained in backbreak_part_review for subsequent pivot authoring.
- Drafts are NOT in graphics ROM or main3fh. Native palette conversion, scale,
  edge cleanup, explicit three-pose descriptors, native control grammar, paired
  pivot calibration and complete physical runtime/visual qualification remain
  required. Digitized-style acceptance and gameplay acceptance remain false;
  existing missing-state markers and release gates are unchanged.

## Latest: native Jax back-break reproduced; alignment overread eliminated

- Physical Jax Block-in-air tests22/23 activate act_backbreak109h against
  actual Kano17/Sonya18. Both stop on the first missing main3fh marker at fight174.
  Original17-slot alignment lookup reads instruction data for added IDs and
  sends victimX to47622/48486. These are reproduced failures, not passing games.
- throw_source.py now reproducibly appends explicit Kano/Sonya alignment slots,
  preserving all17 original entries. Initial offset10,-75 matches the common
  standing-size class; final bent-body knee alignment still needs real own art
  and visual calibration. No actor ID substitution or missing-marker removal.
- Native hidden compile passes20.94 seconds, no created window. Bounds24/25
  replay the same physical action; victim now stays at relative10,-75 instead
  of reading beyond the table. qualify_backbreak_bounds.py checks19 source/ROM
  slots, unchanged original entries, exact executed ROM hashes and runtime
  coordinates. Both still report missing3fh, explicitly NOT gameplay-qualified.
- Current-link P2 Sonya ThrowBoundsRegression26 against Liu passes9,000 fields,
  all6 own body poses,34 damage, recovery and221 grounded observations. Earlier
  throw results are historical evidence from prior program links, not this one.
- Proper three-pose back-break art/control, final paired alignment, full native
  completion and victim recovery remain mandatory. The bounds fix alone does
  not make this move playable. Original MK3 late-root inspection did not reveal
  a dedicated own back-break pose family; no generic tumble was relabeled as one.

## Latest: more original victims, leaner test archives, helper gaps recorded

- Kano Lao20 and Sonya Scorpion21 pass9,000-field ordinary-throw verification
  on the unchanged current program: correct identities, all7/6 own body poses,
 34 damage, normal recovery,221 settled grounded observations and no missing
  marker/recovery-PC/out-of-ROM execution. This does not complete victim coverage.
- Test runner now uses a content-keyed archive cache (base ZIP SHA256 plus every
  replacement-chip SHA256). Each run gets a hard link where supported, keeping
  its independent Lua/log/cfg/nvram/snapshots. Cache content is verified before
  reuse; corruption rejects the run. Unsupported filesystems use an exclusive
  copy fallback. No existing historical run archives were deleted.
- Both synthetic cache unit tests pass: reuse/content isolation and corruption
  rejection. Lao20 creates the current14-MiB archive once; Scorpion21 reuses it.
  os.path.samefile confirms both real runs use the same physical archive, and
  both native game tests pass with their own execution receipts. Future tests
  on this build no longer require another physical ROM-ZIP copy each time.
- THROW_HELPER_AUDIT.json records source hashes and typed bounds: back_break_adjusts
  and flip_damage_table still have17 entries; own back-break root3fh is missing.
  Own ground throws bypass their incompatible native dispatch/release path, but
  that is not general safety for air throws or Jax's back-break against added
  victims. These real remaining character-state gaps require proper art/control
  integration and runtime testing; no guessed pose or pointer alias was added.

## Latest: original-roster throw cases and grounded recovery checks

- Throw diagnostics support explicit non-boss victim IDs and physical shortest
  selection paths from the actual KSNAV neighbor maps. Upper/lower-row input
  releases are explicit. First Kitana16 attempt exposed retained Down input in
  the controller and never entered a match; it is NOT game-failure evidence.
  The controller was fixed before accepted reruns. No ROM gameplay change.
- Current-link Kano Kitana17, P2 Sonya Jax18, and Kano Raiden19 pass9,000-field
  finite throw verification. Correct identities, all7/6 own owner poses, actual
 226h victim state, exactly34 damage, recovery and no missing/recovery/out-of-ROM
  execution. These expand original-victim coverage beyond the existing Liu case.
- Verifier now requires221 post-release observations with both objectY values
  equal to their own native ground origins whenever those columns are captured.
  All three original-roster cases pass. Kitana lift and Jax roll captures were
  inspected, but the finite screenshots do not qualify the entire animation,
  all original victims, full visual style or per-frame hand-contact alignment.
- Original-victim matrix calibration, interruption, back-edge rejection, actual
  added CPU continuation and complete campaign testing remain unfinished.

## Latest: physical front-edge throw cases pass on both sides

- Inspected native reaction_exit before changing interruption handling: it
  already branches airborne actors into fall_on_my_back. No speculative patch
  was made to that path. Actual projectile interruption remains unverified.
- The physical throw controller can now walk the defender away while following,
  observe30 stationary fields at the movement boundary, release away, then
  attempt the ordinary throw. No guest position, state, health or flags writes.
  Additional trace columns record each actual objectY and native p_ganiy.
- Current-ROM Kano FrontEdge14 reaches right boundary1098, owner1035 at
  fight312. Mirrored P2 Sonya FrontEdge15 reaches left boundary60, owner122 at
  fight298. Both pass9,000-field throw tests: own body phases,226h paired state,
 34 damage, recovery and no missing/recovery/out-of-ROM execution.
- Each case additionally checks221 consecutive post-release observations with
  both objectYs equal to their respective native ground origins. Victim returns
  within the observed front boundary. These are front-edge cases only, not all
  corner geometries or pixel-level grounding/shadow acceptance. Same native
  program link as Root10/11; no game-code change was needed for these cases.
- Back-edge eligibility, original-roster victim calibration, real interruption,
  actual added-CPU continuation and complete campaign coverage remain open.

## Latest: main24 own throw root binding corrected and P2 cases reverified

- generate_roster_roots.py now binds main24h directly to each actor's actual
  ks_*_throw_phase0. The superseded Liu-template main24 is no longer exposed
  as their ordinary throw-animation root. Count remains55/66 implemented main
  entries per actor; this corrects an existing entry, not a new covered state.
- Hidden native rebuild passes in18.77 seconds. qualify_own_throw.py now also
  reads each tested ROM's main24 pointer and checks the actual own phase root.
- Current-link P2 Kano10 against Sonya and P2 Sonya11 against Liu each pass
  9,000 fields, all7/6 own body poses,226h victim pairing, exactly34 damage,
  recovery, no missing/recovery/out-of-ROM execution. All earlier throw receipts
  remain historical evidence from their respective links, not current hashes.
- Random CPU Long12 records42,000 fields but hits the60-second host limit;
  it is not a passing run. Shorter Late13 acknowledges startup physically later
  and completes30,000 fields with exit0/no timeout, zero markers/fault capture.
  Neither run actually selects an added CPU object: both remain inconclusive
  for Kano/Sonya CPU gameplay. No fixture forced character IDs, health or state.
- Actual added-CPU continuation, original-victim visual calibration, corners,
  interruption cleanup and complete campaigns remain open. Ordinary air throws
  and all remaining character-indexed helpers still need separate caller audit.

## Latest: dedicated ordinary throw actions execute without the old bad lookup

- Canonical KSTHROW.ASM is now linked. Native do_body_slam routes only IDs17/18
  to dedicated own actions before body_slam_init's incompatible2ah+ID victim
  lookup and17-cell body_slam_jumps. All original character paths remain below
  the explicit guard, not remapped to another fighter.
- Own body phases are2/3/2 for Kano and1/5/2 for Sonya. Throw phase advances3/5
  explicit own-victim records. Kano explicitly turns after release; Sonya runs
  her own backward-getup animation. Native flight,34 damage, and own landing
  handle the released victim. Generated matrices cover17 non-boss victim IDs;
  original-roster XY adaptations are still awaiting broader visual acceptance.
- KSPAIR boundary exception recognizes only a real226h thrown victim linked
  to an actual507h owner with identity17/18. Other boundary paths stay active.
  Grab alignment is applied after drawing the owner's first grab pose, with
  the record index reset before the throw phase; initial captures exposed this
  ordering issue and it was fixed before the accepted finite tests.
- Current-link cases Sonya07 against Kano, Kano08 against Sonya, and P2 Sonya09
  against Liu pass qualify_own_throw.py:9,000 fields each, all6/7 own body poses,
  actual226h paired state, exactly34 throw damage and later recovery, zero
  missing markers or recovery-PC/out-of-ROM execution. P2 Sonya versus Liu is
  the original fault pairing, now tested through physical human inputs. Selected
  grab/roll/flight captures inspected; this is not full visual/edge acceptance.
- Latest hidden compile16.19 seconds, no created window. The earlier30,000-field
  CPU Throw04 run was clean but randomly selected neither added CPU, so it does
  NOT prove CPU throw recovery. Fresh actual CPU coverage, all victims/sides,
  edge/interrupt cases, and main24 root binding to the new phase data remain
  pending. The older translated main24 is bypassed by this dedicated entry but
  must not be mistaken for the final correct own throw-animation root.

## Latest: researched native own throw phases and paired-victim art data

- `review_throw_poses.py` renders the original own composite sequences and
  component pivots in a bounded small sheet. Actual unique body poses are7 for
  Kano and6 for Sonya (not7 for both). Both sheets were visually inspected.
- `generate_throw_phase_data.py` now authors typed `generated_throw/KSTHANI.ASM`
  from the verified MK3 art data: Kano2/3/2 pose phases, Sonya1/5/2 phases
  including the actual two-pose reverse recovery. The current main24 translation
  incorrectly forces both through native Liu1/5/getup grammar and omits Kano's
  fourth unique throw pose. It must not remain the final own throw script.
- Four added-victim/added-thrower pair records preserve original main38/39
  XY/own-composite records and flight pose lists as typed data, not opcode blobs.
  Original MK3 token10 is recorded as XY data, not blindly copied as an MKII
  animation opcode. Kano's final source command2/facing transition is flagged
  for explicit controller handling rather than silently discarded.
- These new phase records are NOT enabled in the running ROM yet. Proper own
  throw routines, adapted original-roster victim records, Sonya's floor/getup
  transition, facing/release/damage/edge handling and physical runtime testing
  remain required. The known current CPU throw crash is not fixed by data alone.

## Latest: own CPU dispatch implemented; real Sonya CPU throw fault captured

- Added canonical KSAI.ASM with own Kano blade/choke/knife/ball decisions and
  own Sonya leg/bike/ring/square decisions. Square checks an airborne opponent;
  paired moves avoid bosses; projectiles enforce the human owner-PID limit.
  Native normal behavior/reaction functions remain shared, without ID proxies.
- drone_source.py now extends all16 explicitly audited MKDRONE tables through
  ID18, including native fatality alignment distances for the existing own
  db1/db2 entries. Added projectile routes bypass incompatible generic zap
  offsets only for17/18. Original typed dispatch rows are preserved.
  qualify_drone_dispatch.py checks linked new rows; this is NOT exhaustive AI
  safety or gameplay proof. Fresh source preparation applies these transforms.
- Native montage and actual MAIN demo CPU opponent selectors now use the14
  official fighters, mapping random indices12/13 to17/18 rather than bosses.
  Original bio fighter stays P1. Actual selection is still random, not forced
  by Lua. Latest hidden build passes in16.97 seconds; no window created.
- Attract01 ran30,000 fields but observed neither added CPU; not a qualification.
  Attract02 naturally produced P2 Sonya versus Liu, including own ring action212h,
  then recovered after a bad jump. Fault03 reproduces the first invalid PC at
  frame24373 (f434cb30), with Sonya action507h/body slam, zero missing markers.
  Exit0 does NOT make either attempt stable. Register/process capture is saved.
- Source confirms body_slam_jumps in MKSLAM still has17 entries. Independently,
  body_slam_init computes victim animation2ah+attackerID: IDs17/18 incorrectly
  select native impale/decap roots3bh/3ch. Proper own throw routines and victim
  matrices are the next required fix. Do not merely alias IDs to Liu, disable
  CPU throws, or append normal_slam while leaving that bad victim lookup intact.
  Current development candidate is not release-ready or CPU-gameplay-qualified.

## Latest: five common native AI threshold tables cover IDs17/18

- `drone_source.py` reproducibly extends backflipper_x_dist, rh_air_distances,
  divesd_x_dist, fntele_heights and superkang_zap_dist to19 explicit words.
  Common thresholds preserve original engine units; no signature move or actor
  ID is borrowed. Fresh source preparation invokes the same integration.
- `qualify_drone_thresholds.py` verifies original17 words against srcw, all19
  linked words in each table, and unchanged other typed MKDRONE table rows.
  Named table symbols are exported for verification only. Hidden native build
  passes (latest19.79 seconds, zero created window handles).
- `stock_wolf_drone_thresholds_orb_01` passes9,000-frame P2 Reptile versus
  P1 Sonya orb/recovery verification on the exact current program chip hashes.
  This regression does not execute Sonya CPU AI or qualify campaign completion.
- DRONE_TABLE_AUDIT.json explicitly retains11 uncovered dispatch/finisher
  tables. Added CPU actors are NOT ready: own-move selection, projectile
  routing, finishers, remaining indirect tables and real CPU gameplay are open.

## Latest: real single-player probes; CPU roster dispatch gap found

- Added windowless physical-input `--campaign [--sonya]` probes with bounded
  execution, read-only observations, natural roster selection and no P2 join.
  The controller stops on missing-state/recovery, return to selection/attract,
  or30,000 fields; it never forces wins or silently retries losses.
- Kano02 and Sonya03 actually enter native ladder position0 versus Sub-Zero3,
  retaining character17/18 through live combat. Both exploratory controllers
  lose, with zero missing markers and normal emulator exit. These attempts do
  NOT prove campaign completion, balance or Kintaro gameplay. The Kano02 trace
  includes later attract-mode observations; its summary excludes those fights.
  Campaign01 was a controller early-stop mistake, fixed before these runs.
- Source inspection finds MKDRONE's ochar_drone_start and zap_offsets still
  have17 entries (0..16). Added CPU characters17/18 would index beyond them;
  rt_special_start and remaining ochar-indexed tables require a complete audit
  and dedicated own-move CPU dispatch. This does not establish the cause of
  the human-controller losses against original Sub-Zero. No speculative game
  patch has been applied to these tables yet.

## Latest: mirrored orb coverage and Kintaro victim choreography

- `stock_wolf_orb_kano_mirror_03` and `stock_wolf_orb_sonya_mirror_04`
  pass the same orb verifier as the P1 cases:9,000 fields each, four own poses
  in order, real damage, recovery, zero missing markers. These four receipts
  describe the program link before the Kintaro data addition below.
- Canonical `KSREACT.ASM` now implements main3eh for each actor, preserving
  original `a_fb_goro` six paired XY adjustments, six pose steps and terminator.
  Its three own poses use existing explicit STUMBLE1/KNOCKDOWN5/6 mappings,
  not another actor or numeric guess. The root generator binds it explicitly.
  Main coverage is55/66 per actor;11 main and7 special roots remain pending.
- Hidden native build completed in16.76 seconds, zero created window handles.
  `qualify_kintaro_reaction_source.py` matches all25 typed items to original
  source, exact76 linked bytes per actor and each main3eh dispatch pointer.
  Program SHA256:C49535E2E2EFD8DC3AC74220735250AD7839E93FDB26FF6902DA620388B455B1.
  This is source/ROM-data evidence only: actual Kintaro slam gameplay and
  actor-specific paired alignment still need physical campaign testing.

## Latest: native slow-orb knockback root implemented and tested

- `KSREACT.ASM` now supplies main3ah (`a_banged`) for both added actors.
  Its four own poses reuse the explicit LKFLIPPED1..4 mapping in translated
  main2bh; the script preserves the native four pointers plus zero terminator,
  without importing throw XY adjustments or landing phases. Native r_orb
  retains control of flight and landing. Root coverage is54/66 main per actor;
  12 main and7 special roots remain pending per actor.
- Hidden native compile completed in17.45 seconds with zero window handles.
  `stock_wolf_orb_kano_01` and `stock_wolf_orb_sonya_02` pass
  `qualify_orb_victim.py`:9,000 fields each, physical Reptile B,B+HP/LP input,
  all four own poses in order, damage and later animation recovery, no missing
  markers, stock emulator exit0/no timeout. Verifier checks exact linked root
  contents and executed program hashes. No guest-memory writes.
- P2 execution, edges, other callers of this root and visual/audio acceptance
  remain unverified. The previous Bicycle/Pit test receipts are historical
  evidence from their respective earlier program links, not this new link.

## Latest: native Bicycle Kick victim root on both player sides

- Canonical `asm/KSREACT.ASM` supplies main37h using each actor's own
  five stumble poses, preserving MKII's `a_bike_kicked` loop grammar.
  `generate_roster_roots.py` binds this root explicitly; each actor now has
  53 implemented main roots, 13 missing main roots and 7 pending special roots.
- Native assembler reported no errors/warnings, with both named roots linked
  into MK2P. The build uses the hidden dummy SDL helper.
- Four physical-input stock-MAME runs pass `qualify_liu_bike_victim.py`:
  `stock_wolf_liu_bike_kano_01`, `stock_wolf_liu_bike_sonya_02`,
  `stock_wolf_liu_bike_kano_mirror_03`, `stock_wolf_liu_bike_sonya_mirror_04`.
  Each records 9,000 frames, 68 native act_bike fields, all five own victim
  poses, the attacker's saved pointer traversing the linked reaction script,
  real damage, subsequent recovery and zero missing markers. Program ROM
  hashes are checked against each execution receipt. No guest-memory writes.
- This is finite Liu-versus-added-victim coverage, not complete victim/AI or
  full-port acceptance. Root3ah (native a_banged, used by r_orb/r_kano) remains
  missing; its four flipped poses need explicit own-art research, not a stance
  alias or a guessed numeric donor-root mapping. Prior Pit evidence belongs
  to the preceding program link and has not yet been rerun on this link.

## Latest: mirrored P2 Pit execution and post-Pit rejoin pass

- `stock_wolf_pit_p2_kano_rejoin_06` and
  `stock_wolf_pit_p2_sonya_rejoin_07` pass the role-aware Pit/rejoin verifiers.
  The losing P1 now rejoins through its actual Start button; the previous P1
  actor replay had used P2 Start. Only physical test inputs changed, not game code.
- Each replay physically earns14 round knockouts, progresses through native
  backgrounds0..6, runs the correct own-victim Pit scene and rejoins in Portal.
  P2's launch-to-fall delay is147 fields and completion205 fields, one less
  than P1's148/206. Both traces retain the exact58-field five-pose fall and241
  impact observation fields. The verifier checks those explicit side timings,
  not a tolerance or a forced scheduling change. Cause is consistent with
  native process ordering, but no separate scheduler-origin claim is made.
- P2 Kano's old Sonya impact clears at21037; P2 Sonya's old Kano impact clears
  at21142. Both next matches start21693 with161/161 health and run600 further
  elapsed fields with519 live-combat observations, real victim damage, zero
  missing markers and no returning Pit drawing shapes. Screenshot inspected
  for the reversed Portal matchup. Both runs exit0 without timeout.
- Together with the P1 cases, both added actors have finite performer/victim
  Pit coverage on both player sides. Palette/process allocator lifetime, exact
  audio/visual-style approval, full single-player AI/ladder campaigns, remaining
  animation roots, clean rebuild and final ROM patches/release remain open.

## Latest: Pit drawing shapes clear before the next actual match

- `stock_wolf_pit_rejoin_sonya_04` and `stock_wolf_pit_rejoin_kano_05` extend
  the physical seven-match Pit progression through a real coin/Start rejoin.
  qualify_pit_rejoin.py composes the original cinematic verifier with a separate
  full post-scene drawing-list check; no source-game changes or forced state.
- Sonya's retained impact shape last appears at21037 and clears at21038;
  fresh Portal combat starts at21693. Kano's last impact is21149, clearing21150;
  fresh combat starts21813. Both new matches start with161/161 health and run
  another600 elapsed fields (601 observations), including519 live-combat samples
  and actual opponent health loss. No own Pit shapes return in that interval.
- Native object-list traversal and screenshots confirm the old Pit body is not
  drawn in the new match; own characters/HUD names render in Portal normally.
  Missing-root markers remain zero and both runs exit0. Cinematic checks still
  cover backgrounds0..6,14 natural round wins,58 fall/241 impact observations and
  native206-field completion; they are not expanded into a campaign claim.
- This is drawing-shape clearance, not a proof of allocator slot freeing,
  palette refcounts or process-pool lifetime. Those resource checks, mirrored
  roles, exact audio/style approval, full single-player ladder/AI, remaining
  animation roots and clean source/ROM-patch release audit remain unfinished.

## Latest: both own Pit II victim scenes run to native completion

- `stock_wolf_pit_sonya_progress_02` (Kano ->Sonya) and
  `stock_wolf_pit_kano_progress_03` (Sonya ->Kano) pass qualify_pit_runtime.py.
  Each physically wins fourteen rounds across seven versus matches, naturally
  traverses backgrounds0..6 via coins/Start, and activates the actual Pit command.
  No stage/health/state writes, savestate fixture or custom driver is used.
- Native Pit state6 lasts206 fields:148 fields of launch/camera transition,
  then58 own fall-object fields. The logger finds the actual victim ID/object
  in the native list at origin192,64, observes all five own poses in the native
  three-field loop with ground counter1..58, then the own impact at counter59
  and native completion. Impact remains observed for241 fields, through240
  post-completion fields. Missing-root count stays zero. Runs end at frames
  20829 /20941, exit0, not timeout. Screenshots inspected for both own impacts.
- Initial progress_01 reached background3 but the controller missed rejoining
  after an expired finishing window without a final hit; its60-second bounded
  timeout was not gameplay acceptance. Rejoin now also observes native stage
  advancement, not only explicit death-blow completion. Successful runs do not
  change game code to advance stages or disable stage/finisher checks.
- This establishes finite P1 performer/added-victim Pit operation, not full
  visual-style/audio approval, mirrored sides, object retirement at the next
  actual match, or a single-player ladder campaign. Full-port/release remains
  incomplete. The impact body intentionally remains until native scene teardown;
  the observed retained body is not claimed to be already freed.

## Latest: standalone lossless Pit artwork sources rebuild exactly

- Exported twelve readable P2 PGM palette-index sources under assets/pit with
  PIT_SOURCE.json geometry/origin/actor/hash manifest. Index0 remains transparent;
  all semantic indices0..63 are retained, including duplicate palette colors.
  They are authored draft artwork, not falsely labelled original MK3 sprites.
- build_pit_assets.py now regenerates named ASM, packed six-bit pixels, all
  eight standard Wolf sockets and metadata from those sources plus the previous
  native graphics prefix. It does not import/read the old ZIP, old mdata,
  custom MAME driver or any old executable/game payload. Historical hash is
  provenance only. assets/pit/README.txt documents standalone use.
- --verify-existing proves byte-identical KSPITART.ASM, packed graphics and
  eight socket files without another on-disk build copy. Metadata's common
  geometry/output hashes agree; new standalone metadata records source ownership
  rather than requiring legacy binary pointers. PIT_SOURCE_ROUNDTRIP.json pins
  every source and output, and qualify_pit_assets.py passes against linked data.
- No game source/ROM bytes changed in this source-export step. This closes the
  old package dependency for these assets, not the whole-port clean rebuild or
  release audit. Pit6 live camera/fall/impact/audio/cleanup tests remain open.

## Latest: own Pit fall/impact data and nineteen-row native tables linked

- Recovered ONLY the twelve previously authored dedicated Pit draft sprites
  from the withdrawn player ZIP's asset records. They are not original MK3
  digitized poses; no old MAME driver, opaque gameplay payload or executable
  donor code is imported. recover_pit_art.py pins the exact source payload and
  reads typed descriptor/group/sequence fields and six-bit pixels only.
- `KSPITART.ASM` provides named own fall/impact descriptors and the original
  MKII Pit grammar: five-frame loop, native ani_jump, separator and own impact.
  Normal/alternate palette ownership stays with the actual native victim object.
  Native MKFALL coordinate/animation tables now have19 deliberate entries,
  preserving their original twelve rows; IDs17/18 use own sequences and origins.
- `generated_pit` preserves all1528603 prior graphics bytes and appends128340
  pixel bytes, with standard eight-socket reconstruction. Asset previews show
  correct red/black Kano and green/white Sonya fall/impact poses. Full native
  assembly/link passed hidden in17.26 seconds after fixing explicit palette refs.
- qualify_pit_assets.py verifies all twelve linked geometries/controls/palette
  pointers, five-frame-loop/impact grammar, pixel hashes, table coverage and
  original rows, and stock socket round-trip. This is asset/link evidence ONLY.
  In-game Pit6 timing/rendering/camera/impact/audio/cleanup are not yet tested;
  visualAcceptance and runtimeVerified remain false. Current runner packages
  generated_pit sockets. Earlier gameplay receipts pin earlier full binaries.
- Recovery currently depends on the withdrawn package as an asset-provenance
  input. A standalone lossless authored-art source export/rebuild path is still
  required before final source/patch release; the old custom build must not be
  a required final gameplay or rebuild dependency.

## Latest: both added actors verified as Kombat Tomb spike victims

- `stock_wolf_tomb_sonya_victim_09` (Kano ->Sonya) and
  `stock_wolf_tomb_kano_victim_10` (Sonya ->Kano) each pass18000 physical-input
  fields, four natural knockouts and a native versus rematch into Tomb.
  The original native spike routine uses their existing own main0f multipart
  knockdown/flat-on-back scripts; no proxy actor or new borrowed victim art.
- Expanded qualify_tomb_stage.py verifies the actual selected victim ID,
  every spike-state victim shape belongs to that actor, the final shape is its
  own third-part flat-back pose, signed victim Y rises above the stage origin,
  native64-field completion, unchanged baseline stage gate and zero missing-root
  markers. Screenshots inspected: green-clad Sonya and red/black Kano are each
  visibly impaled on the ceiling, with the other actual character below.
- These tests add P1 own-victim Tomb coverage without changing game source or
  relinking. They do NOT qualify Pit6's separate scaled-fall scene/table,
  P2 performer/mirrors, random slide-off timing/audio, subsequent-match resource
  cleanup or full campaigns. MKFALL's twelve-row coordinate/animation tables
  remain a known distinct Pit/new-victim implementation gap.

## Latest: native Kombat Tomb finisher commands for both performers

- KSCMD adds Kano U,U,B+LK and Sonya F,F,D+HP, routed through the original
  check_dtp stage/violence/history/dizzy/grounded/72-pixel-distance checks and
  native do_up_the_spike /do_down_the_pit. The checker is exported, not rewritten;
  prepare_game_candidate carries that export. Dead Pool does not become a Tomb
  or Pit via this command. Its separate shared uppercut finisher remains in scope.
- `stock_wolf_kano_stage_rematch_07` and `stock_wolf_sonya_stage_rematch_08`
  pass qualify_tomb_stage.py:18000 fields each, four physical round knockouts,
  ordinary first match/coin+Start rematch naturally advancing to background1,
  correct own command, native64-field spike state8 and completion, own performer
  poses, actual Liu victim, zero missing-root markers. Original check_dtp body
  matches the supplied baseline exactly. Screenshots inspected: Liu on ceiling
  spikes, actual Kano/Sonya uppercut/victory poses below, correct own HUD names.
- Earlier setup runs did not qualify a stage finisher. Background1 in aggregate
  logs was initially mistaken for the active first-match background; per-frame
  logs proved that attempt was background0 and correctly rejected. Rematch
  setup now waits for actual native completion, not an assumed finish timer.
  Kano's Back is a one-field physical tap to remain inside the original close
  range. No guest stage/state/health writes, cheats or host-side game hooks.
- Last full build passed hidden in14.58 seconds. These finite tests establish
  P1 performers against Liu on Tomb, NOT Pit6, P2/mirrors, added actors as stage
  victims, all stages/edges/audio/cleanup or campaigns. Native MKFALL victim
  tables still need own IDs/art before the Pit/new-victim paths can be accepted.
  Earlier gameplay receipts below remain historical after the new source link.

## Latest: shared native Friendship dispatch covers nineteen IDs

- MKFRIEND's command/action tables now have19 typed entries. Original twelve
  entries are preserved exactly; hidden fighter rows deliberately use their
  native group routines, bosses are excluded from the command checker, and
  IDs17/18 dispatch to the actual distinct ks_kano_friend /ks_sonya_friend.
- Both player routes now use original fs_check, rather than duplicate no-punch
  checks in KSCMD. It distinguishes Kano's button history from Sonya's direction
  history and requires the proper live ending button, no other attack buttons,
  minimum160 range, native no-punch eligibility and restricted_xfer safety.
  Fresh preparation reproduces this through checked friendship_source.py edits.
- `qualify_friendship_dispatch.py` checks19-row coverage, exact preservation of
  all original command/action entries, and unique linked own action/command
  pointer pairs in the ROM. Last full native build passed hidden in18.81 seconds.
- `stock_wolf_kano_friend_shared_07` and `stock_wolf_sonya_friend_shared_06`
  pass their full finite animation/completion verifiers on this binary (Kano P1,
  Sonya P2,9000 fields each). Kano's bubble object and dummy process still retire.
  `stock_wolf_friend_shared_reject_08` confirms punch-use eligibility rejection
  with the actual correct Kano button queue inside Finish Him, also9000 fields.
- This closes the short native dispatch table defect, not AI/campaign runtime
  acceptance. Exact DCS pop/cluck, rapid-input feel, broader victims/edges,
  subsequent-match cleanup, stage finishers, full native animation/victim roots,
  campaign/selection audits and clean rebuild/ROM patches remain in scope.
  Earlier receipts below pin historical binaries and are not current proof.

## Latest: distinct native Kano bubble-gum Friendship

- `KSFRIEND.ASM` now has a separate Kano action: native48-field setup, eighteen
  original body poses x5 fields, then eleven bubble events x5 fields using all
  seven own bubble composites. Holds the final body pose while the separately
  allocated/paletted multipart bubble grows and pops. Retires object/palette/
  dummy process through native kmo_proc, clears p_slave, then native Friendship
  completion. No substitute Sonya action or donor executable callbacks.
- Own LK,Block,Block,HK gate uses native button history, released other buttons,
  native no-HP/LP eligibility and minimum160-pixel range. Initial fast replay
  reached the gate but native restricted_xfer rejected the owner's ongoing Low
  Kick recovery. Read-only input/queue/action traces isolated this. The successful
  replay separates LK from final HK by48 fields, within the existing80-field
  history window. Rapid-input/cancel behavior versus original remains unqualified;
  no blanket recovery bypass was added. Temporary native gate counters removed.
- `stock_wolf_kano_friend_cadence_04` and `stock_wolf_kano_friend_mirror_05`
  pass `qualify_kano_friend.py`: 9000 fields each, two natural kick-only round
  wins against actual Sonya, 193-field native state7, every body/bubble frame
  and duration, own stationary origin/child alignment, 55 visible bubble fields,
  both object and dummy process retired on completion, zero missing-root markers.
  Screenshot visually confirms the pink bubble and Kano's own gum-blowing pose.
- `stock_wolf_kano_friend_punch_reject_06` wins with HP against Liu, presents the
  actual correct four-button queue within Finish Him and is rejected by native
  eligibility, with no Friendship action/completion. Latest build passed hidden
  in14.54 seconds. Exact pop/cluck DCS, rapid command feel, broad victims/edges,
  subsequent-match resource cleanup and whole-current-build regressions remain.
- Both direct player command paths now exist. Generic MKFRIEND AI action/command
  dispatch tables still stop at12 entries and must be deliberately extended for
  actual IDs17/18 before claiming native AI/campaign finisher integration.
  Earlier full-linked-binary receipts below remain historical, not current proof.

## Latest: Sonya native Friendship action and command

- `asm/KSFRIEND.ASM` implements Sonya's own intro (seven poses x5 fields),
  then the original fourteen-pose chicken/flapping loop x3 fields. Uses native
  MKII friendship setup (48-field pause) and asynchronous native completion
  after another128 fields. No donor executable callback is copied or executed.
  The exact original cluck cues remain unfinished, not replaced by claimed audio.
- Own B,F,B,D+Block gate checks Finish Him, non-boss victim, minimum160 range,
  native raw no-HP/LP eligibility and native direction history with no other
  attacks held. The first two runs did not activate: the live MOVES char_block
  row18 was still sucide despite the existing KSCMD handler. Corrected it to
  ks_sonya_block (fresh preparation already specified that row). Removed the
  temporary read-only-observed native gate counter before the successful build.
- `stock_wolf_sonya_friend_dispatch_03` and `stock_wolf_sonya_friend_mirror_04`
  pass `qualify_sonya_friend.py`: 9000 fields each, actual Sonya/Kano IDs on both
  player sides, two natural kick-only round wins, all intro/loop poses and exact
  field timing, unchanged performer origin, 176-field native state7 and completion
  state65535/flag2, zero missing-root markers. Screenshot shows the own flapping
  pose; this is not a replacement with another character's Friendship.
- `stock_wolf_sonya_friend_punch_reject_05` physically wins Sonya's rounds with
  HP against Liu; native eligibility then rejects the same command over a full
  finishing window. No Friendship action or completion is observed.
- Last native build passed hidden in20.44 seconds. Runtime now packages
  generated_friendship sockets. Kano's distinct bubble-gum action/command, exact
  friendship audio, all victims/edges/AI, cleanup and current full-port regression
  remain unfinished. Earlier receipts below are historical after this full link.

## Latest: own Friendship art linked; actions remain unfinished

- Inspected native MKFRIEND: both command and action tables still stop at the
  original twelve actors. The new characters do not yet have working native
  Friendships; neither existing finisher nor stance is being called a substitute.
- `generate_friendship_data.py` imports Kano's 18 bubble-gum body poses plus
  seven separate bubble poses and Sonya's eleven chicken/body poses, as 36
  named composites /56 unique image descriptors in `KSFRART.ASM`. Donor action
  opcodes/callbacks are not copied into the ROM. Native choreography, timing,
  palette switching, commands and audio still need implementation/verification.
- Appends 41658 bytes of original compressed pixels after the entire existing
  1486945-byte graphics prefix; all eight standard Wolf sockets round-trip.
  `qualify_friendship_assets.py` checks every linked frame's original geometry,
  control word, own palette reference, packed graphics address/hash, composite
  membership and terminator. Native assembly/link passed hidden in 14.18 seconds.
- This is asset/source-link evidence only, not gameplay. The current runner
  still packages the preceding `generated_names` graphics set because no native
  Friendship action is connected yet; switch it with action integration. Earlier
  gameplay receipts pin their earlier full linked binaries and remain historical.

## Latest: native lifebar names and matching shadow pixels

- Replaced both actors' BAR_NULL entries with named `KSNAMES.ASM` descriptors.
  KANO is 38x10, SONYA 47x10; P1 starts at native x29/y30, P2 is right-aligned
  to native x367. Uses the original native HUD DMA path and SCORE_P palette,
  not host text or an overlay. Gold glyph pixels come from MKII's own HUD art;
  Y is adapted from native FONT7Y. O's adjacent R column is excluded explicitly.
- `generated_names` preserves the entire baby/fighter/UI/finisher graphics
  prefix and appends 425 bytes of four-bit native HUD pixels. All eight stock
  Wolf sockets round-trip. Full native build passed hidden in 23.07 seconds.
- `stock_wolf_hud_names_01` and `stock_wolf_hud_names_reverse_02` each finish
  9000 fields on unmodified stock MAME. `qualify_hud_names.py` verifies all four
  source/linked-ROM table entries, descriptor sizes/SAGs and every nontransparent
  rendered name pixel in both player arrangements: Kano215 / Sonya251 pixels,
  including 71 /83 shadow pixels. Screenshots show names in their actual bars.
- Shadow is native SCORE_P index2, RGB(66,0,0), matching the stock MKII dark
  shadow exactly; it is not falsely described as pure RGB black. No global
  palette change was made. Full-port regression/campaign/release remains open.
  Earlier receipts pin earlier ROM/socket sets; they do not certify this link.

## Latest: native Babality commands and initial completion tests

- Follow-up `stock_wolf_baby_sonya_victim_03` (Kano P1) and
  `stock_wolf_baby_kano_victim_mirror_04` (Sonya P2) pass the expanded verifier.
  Read-only native object-list traversal finds the exact own baby descriptor,
  correct 35x54 / 27x44 dimensions and bottom exactly at native ground_y.
  Screenshots were visually inspected: Sonya's green baby and Kano's red/black
  baby appear on the floor while the actual winner uses its own victory pose.
  Native 192-field completion and zero missing-root markers pass in both runs.
- `stock_wolf_baby_punch_reject_05` physically wins Sonya's rounds using HP;
  the same Babality command then correctly fails native eligibility, with no
  Babality action/completion and a full finishing window observed. Each of
  these three follow-ups ran 9000 fields without Lua/recovery errors.
  This is not all four actor/side combinations, every invalid gate, palette
  resource lifetime, subsequent-match cleanup or broad campaign acceptance.
- Both new LK dispatch rows now call `ks_baby_kick`: Finish Him, non-boss
  victim and minimum 160-pixel range, then original `bb_check`. Native no-HP/LP
  eligibility, shared delayed action, poof, audio and completion remain native.
  MKBABY command rows implement Kano F,F,D,D+LK and Sonya D,D,F+LK.
- `stock_wolf_baby_kano_01` and `stock_wolf_baby_sonya_02` pass
  `qualify_baby.py`: each 9000 fields, two natural kick-only round wins against
  Liu, 192 fields of native Babality state5 and completion state65535/flag1,
  zero missing-root markers and no Lua/guest recovery errors. This is P1-only
  command/completion evidence, NOT own baby rendering or invalid-gate acceptance.
- `generate_baby_data.py` imports actual original single-image baby descriptors
  for Kano (27x44, 30-color palette) and Sonya (35x54, 32 colors), preserving
  original compressed pixels. `KSBABART.ASM` supplies true-ID baby-image rows;
  the stock Wolf graphics sockets round-trip with a 1249-byte appended payload,
  preserving the full prior 1485271-byte graphics prefix. Own-baby victim runtime
  rendering/grounding now has the narrow evidence above; fresh-match cleanup
  is still unverified.
- Full original-source link passed hidden in 20.51 seconds. New test ROMs use
  `generated_baby` sockets. Earlier smoke receipts pin earlier binary/socket
  sets and need fresh current-build regression, not blanket acceptance.

## Latest: Shang morph identity and timed-return smoke test

- Follow-up `stock_wolf_morph_specials_05` and `stock_wolf_morph_mirror_06`
  each pass 9000 fields on the current binary. Both actual player sides perform
  Kano's Knife and Sonya's Ring while transformed, each causing 22 damage to
  the stationary opponent. The verifier observes 25 Knife action fields and
  15 Ring charge fields, own actor poses, zero missing-root markers and all
  three automatic returns. CSV columns normalize actor/opponent roles in the
  mirrored case; execution arguments record the actual side. This does not
  qualify all transformed moves, palette visuals, interruptions or edge cases.
- `stock_wolf_morph_table_04` passes `qualify_morph.py`: 9000 fields, physical
  selection of Shang versus Sonya, Kano command, then Sonya chord in both
  button orders. Observed actual IDs are 6 ->17 ->6 ->18 ->6 ->18 ->6.
  Each transformed identity lasts 524 fields including reverse animation,
  every transformed shape belongs to that actor, and missing-root count is zero.
- Initial morph_01 had a test input-port error; morph_02 failed to join player2.
  Corrected setup morph_03 exposed an actual missing native morph table and
  failed. MKST's table now extends through IDs17/18 with the reverse-compatible
  script layout; morph_table_04 is the first successful bounded runtime check.
- Temporary own-stance transition frames are explicit rough edges, NOT completed
  bespoke morph-between art. Mirrored-side, transformed specials, alternate
  palettes, edges, interruptions and full current-build regressions remain open.

### Native morph source additions

- MOVES now checks B,D,B+LK for Kano17 before the existing LK morph commands.
  LP and Block both check the live Down+LP+Block chord for Sonya18, allowing
  either button order through the shared native chord predicate.
- The two actions supply actual IDs17/18 to original `shang_morph`, retaining
  native animation, palette selection, ground adjustment, morph timestamp and
  existing timed return-to-Shang path. MKST supplies dedicated target scripts.
  No proxy identity or emulator patch.
- `morph_source.py` carries checked source transformations for fresh preparation;
  KSCMD exports the existing chord predicate. Full native compile/link passed
  hidden, with no window observed (latest table-fix build: 18.16 seconds).
  Physical commands, own identity/poses and timed reversion now have the narrow
  evidence above; full visual/palette/grounding acceptance is still pending.
  This new link also requires fresh regression evidence; prior
  Eye Laser receipts below pin their earlier binary.

## Latest: distinct native Kano Eye Laser

- `asm/KSLASER.ASM` and `generated_laser/KSLAANI.ASM` implement Eye Laser
  separately from skeleton extraction. Both actors now have two distinct native
  fatality actions, not yet full acceptance of those actions or the port.
- Physical LP, Block, Block, HK requires releasing Block before HK, with native
  button history, range and fatality dispatch. No emulator hooks or guest-memory
  writes are used. Actual IDs remain Kano17 and the selected victim's own ID.
- `qualify_laser.py` passed `stock_wolf_laser_01`, `stock_wolf_laser_mirror_02`,
  `stock_wolf_laser_liu_03` and negative `stock_wolf_laser_held_block_04`.
  Each ran 9000 fields with two natural round knockouts and no missing-root
  markers. Positive runs verify all 176 performer/beam fields, 96 actual-victim
  reaction fields, native completion and retirement of beam plus dummy process.
  The held-Block case correctly does not activate.
- Added actors use their own original laser-victim composites. Original MKII
  victims use their own native wound art; that adaptation needs broader visual
  acceptance. Exact DCS cues, all victims/edges/AI, fresh-match cleanup and full
  current-build regression remain outstanding. Earlier receipts below concern
  earlier linked binaries and do not certify this build.
- Compiles use `start_background_compile.ps1` only: dummy video/audio, hidden
  windowless startup, below-normal priority, bounded timeout and no visible
  fallback. Automated stock-MAME tests remain windowless.

## Latest: distinct native Sonya Death Orb/Bubble

- Checked the previous released movelist against donor routines: the remaining
  fatalities are Eye Laser and Death Orb, not Heart Rip. `asm/KSBUBBLE.ASM`
  now implements the distinct Death Orb. Its native second-fatality table entry
  is separate from flame kiss. Actual actor/victim IDs are never substituted.
- `generated_bubble/KSBUANI.ASM` supplies seven growth, four looping enclosure
  and three burst composites, with the original 32-color palette. Pixel
  decoding verifies every referenced color fits that palette. All art was
  already imported; this action needs no additional graphics-ROM space.
- The gate requires far range, Block currently held, U,U,B,D+HK history and a
  latest Block press no later than the first direction. It rejects HP/LP/LK,
  bosses and broken continuous holds, using native switch/history routines.
- The action uses native object allocation/alignment and scheduler, two-pixel
  travel fields, a 177-pixel raw-pivot contact threshold, own native victim
  stumble, 39 enclosure fields, 12 burst fields and an own 32-field salute.
  Generic stock MKII gore particles are spawned on the actual victim. Exact
  new audio and broader balance/donor-timing comparisons remain unqualified.
- Initial `stock_wolf_bubble_01` / `stock_wolf_bubble_fault_02` recover-looped.
  Read-only register/stack evidence identified double palette deletion after
  the stock kiss explosion's broad off-screen cleanup removed the bubble early.
  The new action spawns native gore without that global cleanup loop and
  explicitly retires its own object/palette/process. `bubble_cleanup_03` then
  exposed a still-active, never-woken dummy process; that is not an accepted run.
- Native `MKUTIL:kmo_proc` now recognizes both initial and sleeping dummy
  entry points and guards a null link. The action preserves multipart oslink,
  which aliases the gravity field for other object types. The preparation
  script reproduces these source fixes; preserved baseline srcw is unchanged.
- `stock_wolf_bubble_retire_04`, `stock_wolf_bubble_mirror_05` and
  `stock_wolf_bubble_liu_06` each complete 9000 stock-MAME frames after two
  physical-input round wins. `qualify_bubble.py` verifies all fourteen effect
  poses, native victim stumble, 39 travel fields at two pixels/field, 176-field
  completion in these cases, and read-only active-list proof that both bubble
  object and dummy process retire before completion. Zero missing markers.
- `stock_wolf_bubble_bad_hold_07` is a 9000-frame negative case: Block is
  released/re-pressed between the two Up inputs, then held at final HK. Sonya
  stays grounded and does not enter the fatality before the normal finishing
  window expires. This is not a claim about every invalid input sequence.
- Kano Eye Laser is still unimplemented. All-victim/edge/AI checks, exact DCS
  audio, fresh-match cleanup, current-binary regressions for earlier moves,
  other requested finishers/morphs/UI/campaigns and final patches remain.

## Native Sonya flame kiss (earlier source link)

- `asm/KSKISS.ASM` now implements Sonya's flame kiss in native ASM, using her
  own eleven-pose performer sequence, a native single-object fire orb, actual
  opponent object, native palettes/fade/scheduling and fatality completion.
  B,F,D,D+LP routes through the original fatality gate. Actual IDs remain 18
  and the victim's own ID; no proxy or emulator change is involved.
- `generated_kiss/KSKSANI.ASM` exports eight original orb descriptors/palette,
  burn control data and eight salute poses. Original compressed orb bytes add
  2910 bytes after the unchanged prior graphics prefix. All ordinary Wolf ROM
  sockets round-trip exactly. KSKISS/KSKSANI are linked with the original game.
- The attached orb is explicitly retired before burning. Its native motion is
  five launch fields, 28 ascent fields, ten turning fields and sixteen homing
  fields, then one final visible contact field. The endpoint uses the actual
  victim X and the stage floor minus 88. The burn lasts 116 fields with all
  fifteen own burn poses; Sonya salutes during its final 44 fields.
- `stock_wolf_kiss_ground_03`, `stock_wolf_kiss_mirror_06` and
  `stock_wolf_kiss_liu_05` each complete 9000 frames on unchanged stock MAME
  after two physically won rounds. `qualify_kiss.py` checks every fixed-point
  orb movement step, all eight frames, deletion before burning, unchanged
  victim standing origin, exact performer/burn/salute sequence and native
  completion after 231 fields. There are zero missing-animation markers.
  Screenshots inspected from both sides and the Liu case show the burn on
  the stage and the own Sonya performer/salute, without selection overlays.
- Earlier trials are not passes: kiss_01 attempted the command before post-KO
  recovery ended; kiss_02 exposed erroneous grounding of a torso-only flash;
  kiss_mirror_04 used incorrect navigation directions for the dedicated edge
  slots. The controller now approaches once, waits before command entry and
  follows each target's actual selector edge. No game-memory forcing was used.
- Kano extraction and Sonya flame kiss are now implemented. The other two
  fatalities, exact new native launch audio/mix, all victims/edges/AI, full
  new-match cleanup and the rest of the port remain required. Shared native
  kiss/fire effects are temporary, not accepted exact Sonya DCS cues.
- Compilation is now headless: dummy SDL video/audio, no console window,
  below-normal priority and visible-window checks. All port DOSBox configs
  enforce dummy video. See `BACKGROUND_BUILDS.md`; do not launch visible builds.

## First native fatality — Kano extraction (earlier source link)

- `asm/KSFATAL.ASM` now implements the actual Kano skeleton extraction using
  symbolic native setup/fade, takeover, attached multipart allocation, palette
  handling, drawing, scheduling and completion routines. No emulator hooks or
  copied donor opcodes are used. B,D,F+HK at close range routes through the
  original fatality eligibility/distance gate. Its own states are 021c/021d.
- `generated_extract/KSEXANI.ASM` supplies nine body poses, six skeleton phases
  and six explicit victim phases for each nonboss ID. Original victims use their
  actual native windup/headless composites; Kano/Sonya use their own imported
  extraction bodies. Unique source aliases avoid exporting duplicated local
  names such as Shang's and the ninjas' separate NJDECAP groups.
- Both fatality dispatch tables are extended through ID18. Only Kano's first
  choice is implemented; other unfinished entries remain explicit native null
  entries, not aliases to this fatality. They are not completed fatalities.
- `PBUILD.BAT` now assembles/links KSFART, KSFANI, KSEXANI and KSFATAL with the
  original game. The physical-input runner uses the combined finisher graphics
  sockets. `prepare_game_candidate.py` includes the same source integrations.
- `stock_wolf_extract_01`, `stock_wolf_extract_mirror_02` and
  `stock_wolf_extract_liu_03` each complete 9000 frames on unchanged stock MAME.
  Each physically selects the fighters, wins two rounds naturally, enters
  Finish Him, then activates extraction. `qualify_extract.py` checks 231 action
  fields, all nine own body poses, six skeleton phases (eight fields each),
  six character-owned victim poses and native completion, with zero missing
  animation markers. Test ROM bytes must match the current map/build.
- Screenshots inspected from both player sides show the attached skeleton pull
  and own Sonya victim; the Liu sample shows his own native collapsed body.
  This is finite one-fatality evidence, not all-victim or full-port acceptance.
  Exact native launch audio, all victims/stage edges/AI, retained-child teardown
  into a fresh match and the other three fatalities remain outstanding.
- Earlier special receipts are historical after this new source link. They
  must be rerun against the current binary before release acceptance.

## Earlier isolated finisher asset preparation (historical)

`FINISHER_INTEGRATION.md` records the next source integration. Newly generated
`KSFART.ASM` and `KSFANI.ASM` provide 48 finisher composites/83 frame records and
the eleven-pose own Sonya kiss performer script. Their original compressed pixels
append 154084 bytes after the unchanged fighter/UI prefix, with exact standard
Wolf-socket round-trip checks. Both modules assemble with zero errors/warnings
using the original TI toolchain (`FASM.BAT`, `FART.LOG`, `FANI.LOG`).
At this earlier checkpoint they were not linked into the game and implemented
no fatality actions; see the newer integration above for the current candidate.
`generated_finishers/ASSEMBLY_CHECK.json` is an asset/assembly receipt only.

## Latest: native Leg Grab and Wolf input correction

- `asm/KSLEG.ASM`, `generated_leg/KSLANI.ASM` and shared `asm/KSPAIR.ASM`
  assemble/link as ordinary source modules. Leg Grab uses own Sonya animation,
  actual victim objects and per-character named native victim composites.
- Fixed native `MOVES.ASM:button_mask` for Wolf hardware: LP/LK are in the main
  input longword, not the T-unit auxiliary port. P2 bits are translated to the
  engine masks; both physical Block inputs are normalized. The T-unit branch is
  retained. The preparation script reproduces this source correction.
- `stock_wolf_leg_01` and `stock_wolf_leg_gate_02` are failed activation tests.
  `stock_wolf_leg_inputfix_03` established activation after correcting the mapping.
  Temporary command-gate RAM counters were removed before accepted tests.
- `stock_wolf_leg_clean_04`, `stock_wolf_leg_mirror_05` and
  `stock_wolf_leg_liu_06` each completed 9000 frames on unchanged stock MAME,
  physical inputs only, with seven 46-field holds, 35 damage per release,
  all seven own body poses and five own victim poses, exact grip offsets and
  zero missing-animation markers. Each run fully observes six recoveries;
  its final throw releases before the 9000-frame cutoff but is not observed
  long enough to certify its full get-up. `qualify_leg.py` checks these bounds
  and requires test ROM bytes to match the current build before using its map.
- Tested: simultaneous and Block-first chords, redundant Block input, standing
  Block caught, low Block/far miss and missing-button/direction rejections.
  LP four fields before Block starts an ordinary punch, not Leg Grab; no
  input-buffer forgiveness or acceptance for that ordering is claimed.
- Choke's paired-animation loop now shares `KSPAIR`; fresh
  `stock_wolf_choke_pair_05` passes the existing 9000-frame eight-hold Sonya
  victim trajectory/four-damage-pulse/release regression on this binary.
  Other earlier special receipts remain historical until rerun on this build.
- These are bounded eight-special smoke tests, not full playability acceptance.
  Other victims, stage edges, AI, audio, finishers, morphs, UI, campaigns and
  reproducible final ROM patches remain required. No release is ready.

## Verified foundation

- T-unit source baseline: assembly/link/split, stock MAME 0.289 boot,
  selection, ladder and real combat in a 12000-frame physical-input test.
- Original T-unit diagnostic assembly fails with 27 errors. Four conditional
  directives guard two mistakenly unconditional Wolf-specific blocks. The
  original failure log is retained; no successful unmodified T-unit build is
  claimed.
- Wolf-unit source baseline: supplied compiler/linker/split tools, native
  PLBUILD DCS sound ROMs, stock MAME MK3 hardware, correct original MKII
  graphics lane ordering, boot and ordinary combat in 12000 frames.
- An initial Wolf test used the wrong graphics socket ordering; its garbled
  screenshots are a failed graphics test, not an accepted build. Corrected
  packer uses (UG14,UJ14,UG19,UJ19), (UG16,UJ16,UG20,UJ20),
  (UG17,UJ17,UG22,UJ22). Original game/emulator source did not need changing.

## Work actually migrated

- `asm/KANOMOV.ASM`: cannonball action/recoil/landing and bounded repel callback.
- `asm/SONYAMOV.ASM`: square-wave rise, flight, collision and recovery.
- `asm/KSCMD.ASM`: held-LK release / F,B+HP recognition and native action transfer,
  explicit own IDs 17/18 and airborne-opponent prerequisite.
- First source modules assemble using TI GSPA. Link-map-based engine bindings
  replace fixed retail addresses. These are NOT yet installed into the game.
- `import_character_art.py` generates typed assembly palette/frame/composite
  records from user-supplied MK3 ROM data. 452 Kano frames/281 poses and 456
  Sonya frames/266 poses; two native palettes per fighter. Initial records use
  native graphics offsets at byte 0xc00000, no custom address tag. Alternate
  palette selection and native animation/state routing still need integration.
- Generated art modules assemble with GSPA and link alongside the action modules.
- The current `generated_packed/` export retains 908 frame records and packs
  890 unique original compressed bitstreams into 1319175 bytes, fitting the
  six MiB remaining in the stock MK3 ROM socket layout. No extra ROM definition
  or expanded emulator region is necessary for these graphics. Each copied
  frame bitstream is checked for byte/bit identity after packing.
- Wolf native-DCS audio smoke test: nonzero PCM peak 2282, 10528321 frames
  at 48000 Hz mono; no host samples device. Not a subjective audio review.
- `generated_packed/KSANIM.ASM` supplies fourteen explicitly translated native
  animation scripts (stance, forward/back walks, crouch, forward/back flips and
  two-phase vertical jump for each actor), referencing 63 own pose labels.
  It assembles and links with both art modules and the first action/command
  modules. It deliberately does not create a complete dispatch table or silently
  replace missing animations with Liu/stance. Scripts are not runtime-tested yet.

## Subsequent native source integration

- Source-level translation now preserves 38 explicitly matched ordinary combat
  animation scripts per fighter, including punch-chain cross-jumps, phase
  delimiters, sweep and kick sound callbacks. All compile and link with the
  native engine. The actual baseline main table has **66**, not 65, entries.
  No complete new animation dispatch table is claimed. Native main 36 is paired
  throw choreography and is intentionally not mapped to an unrelated fall.
- `diagnostics/KSART.ASM` and alternate KSSEL source provide a test-only native
  scene. They create two independent multipart objects, IDs 17/18, without
  borrowing a selectable fighter slot. Original game code handles palettes,
  drawing and animation on stock MAME MK3 hardware. No emulator writes or hacks.
- `baseline/stock_wolf_own_art_qualified/qualification.json` proves the live
  objects cycle through all nine Kano/eight Sonya stance pose pointers over
  2800+ frames. Visually inspected clean sprites on the native backdrop.
- Early art tests did not acknowledge CMOS initialization, or read byte-aligned
  diagnostic pointers with an aligned DWORD accessor, or aliased pose cycles by
  sampling every 30 frames. Corrected input/read/sampling probes; do not count
  those earlier attempts as successful identity/pose verification.

## Paired-animation source pass

- Visual inventory of original donor main entries 33..64 is retained in
  `donor_role_review/`. Main 35 is the throw ATTACKER, contrary to the old
  prototype's forward-fall comment. The source translator now preserves the
  native grab/throw/getup phases for that role.
- `generated_templates_throws/` supersedes the earlier 38-entry generation:
  **51 native main-animation scripts per character assemble and link**, including
  twelve per-attacker throw-victim control scripts with native XY phases.
  Existing donor-attacker equivalents use their original pose families; missing
  MKII-attacker equivalents use explicitly documented own-body throw poses,
  not another character's ID, animation or native trajectory. This pairing still
  needs real throw/contact/grounding tests before acceptance.
- `CHARACTER_TABLE_INVENTORY.json` pins the original source inputs and identifies
  66 candidate character-indexed data tables from 80 helper calls plus explicit
  core roots. It is a source-navigation inventory, NOT an exhaustive safety
  proof. Three nearest-load candidates are constants rather than tables and
  remain flagged. No table has been blindly extended or aliased to Liu.

## Stock-MAME script playback and native UI-source migration

- `baseline/stock_wolf_animation_matrix_51/qualification.json`: 12000 frames,
  490 live samples over 8313 frames, both actual IDs unchanged, all 51 scripts
  reached for each actor. Every recorded shape belongs to that actor's imported
  art; every script displayed at least one pose referenced by its own source.
  This verifies **initial-phase playback only**, not complete actions, all
  script phases, collision, paired throws or playability.
- The first matrix link used DOS-incompatible long filenames. Corrected to
  `CYCTEST.OUT/MAP` and short log names; did not bypass linker errors. Earlier
  stance evidence files remain unchanged and independently reproducible.
- `generated_ui_packed/KSUI.ASM` now bakes dedicated 55x70 selection portraits,
  35x45 ladder portraits, and locked-selection palettes as normal ROM records.
  No borders are baked in. Fighter graphics prefix is unchanged. Combined art
  uses 1328277 bytes of six MiB available in stock MK3 sockets. Source assembles
  and links; portrait previews visually inspected. Native selector integration
  and runtime UI acceptance are still pending.
- `asm/KSNAV.ASM` implements ID19-range directional lookup and coordinate-derived
  cursor deltas, plus counted blocked-edge tables. It preserves native cursor
  segment/number ownership rather than drawing overlays. New Sonya/Reptile and
  Kano/Liu links are direct neighbors. Diagonal outer-column downward moves
  account for the 60-pixel horizontal delta instead of accumulating cursor drift.
  Assembly/link and 56-case static graph/geometry schema checks pass. These
  helpers are **not yet wired to MKSEL or runtime-tested**, including auto-select.

## Remaining (full scope, not narrowed by diagnostic passes)

### Native Kano Choke

`asm/KSCHOKE.ASM` implements D,F+LP with three catch poses, six collision fields,
blocked/boss/miss rejection, the paired lift, four 8-point damage pulses, final
held poses and native airborne release/get-up. KSCANI has typed body scripts and
19-row victim data: IDs 17/18 use their original donor choke poses and XY records;
original fighters resolve their own native high-hit pose 2 with per-body grip
offsets. No character ID or victim artwork is substituted. Boss rows are null
and explicitly excluded before collision. Native takeover, palette/slave cleanup,
input ownership, damage reducer, floor physics and recovery remain responsible.

`qualify_choke.py` passed for `stock_wolf_choke_02`,
`stock_wolf_choke_mirror_03`, and `stock_wolf_choke_liu_04`. Each is a 9,000-frame
physical-input stock-MAME run with eight complete 69-field holds, all eight own
body poses and zero missing-root markers. First holds show four separate 8-point
HP drops at hold ages 27/39/51/63 (32 total), then both actors back in stance.
Held XY exactly matches the respective typed trajectory and velocities are zero.
Sonya retains her own donor victim pose; Liu's observed pose is checked against
his actual native animation-root lookup in the tested program ROM. Standing
block, held duck and far attempts cause no hold or damage and recover. Runtime
snapshots for Sonya and Liu were inspected. These are finite cases, not all
victims, bosses, stage edges, mirror Kano victims, AI/campaign or audio acceptance.

The generic native voice dispatcher now recognizes Sonya as female (the supplied
source knew only the original female IDs). This uses native SOUNDW categories;
new launch voice events and mix acceptance still remain. The first Choke input
script stayed outside catch range in planned close attempts; it is retained as
earlier evidence, not misrepresented as a complete hit/block qualification.
Current receipts pin program/map, relevant source, frozen controller and snapshots.

### Native Sonya Bicycle Kick

`asm/KSBIKE.ASM` and generated KSBIANI implement B,B,D+HK with independent
startup, rising seek, standing-block rebound, duck/boss rejection, missed forward
fall, paired lift/float, victim release and both get-ups. Native helpers retain
the true actor IDs, victim's own animation root, input ownership, shake task,
collision/blocking, ground-relative ceiling, object physics and recovery. Both
actual velocities AND normal player requests are updated at paired phase changes
and ticks; the suppressed close-body publisher cannot leave a stale rise velocity.
Get-up/sweep-up speed data now explicitly cover IDs 17 and 18 (four fields).
Sonya reaction row 26 is the native waiting/release routine; unused row 25 is an
explicit error path pending Leg Grab, not a silently substituted move.

`qualify_bike.py` passed for `stock_wolf_bike_01` and
`stock_wolf_bike_mirror_02`: each 9,000-frame stock-MAME physical-input run has
11 activations, 352 paired fields, all nine distinct own bicycle poses and zero
missing-root markers. An incomplete B,D command is rejected. The scenarios show
22-point hits, 3-point standing blocks, duck and far misses, first-pair release
and both actors back in stance. After the initial contact field the victim stays
48 pixels in front / 32 above Sonya; both actors share rise (3px/tick horizontal,
-3 vertical) and float (1px horizontal, +0.5 vertical) velocities. Kano's paired
poses all belong to his own imported art. Snapshots were visually inspected.

These are finite added-versus-added tests, not all victims/bosses, all arenas,
AI/campaign, native launch voice or audio-mix acceptance. Those gates remain.
The first compilation rejected a missing external declaration for the reserved
reaction error path; adding the declaration fixed the source build. Baseline
sources and stock MAME remain unchanged. Older action/contact evidence is
historical rather than current-binary regression evidence.

### Native Blade Swipe and late-contact punch fix

`asm/KSBLADE.ASM` implements D,F+HP with Kano's ten original body poses,
three native animation phases, facing-aware advances, one strike, and a separately
paletted single-object trail. KSBANI reuses original compressed graphics through
ordinary native descriptors. The trail uses `p_slave`: normal and hit recovery
own object/palette teardown. A separate own reaction row 25 uses native blood,
victim voice, airborne/boss setup and the victim's own stumble animation.

`qualify_blade.py` passed for `stock_wolf_blade_04` and
`stock_wolf_blade_mirror_05`: each completed 9,000 physical-input stock-MAME frames,
with 17 activations and all ten blade body poses observed. The finite scenarios
cover an initial whiff, a 26-point hit, 3-point blocked hit, normal recovery and
interruption by one 11-point punch. The attached slot clears within two observer
fields of interruption; inspected later displayed hit-reaction frames show no
trail. Both runs retain zero missing-root markers and ROM PCs. This does not
qualify all victims, boss/airborne/spacing cases or the audio mix.

The earlier `stock_wolf_blade_03` interruption exposed a supplied-source bug:
JOY's `punch_sleep` did not consume A11 after a successful *late* strike check.
One press could repeatedly damage a victim after missing its first check.
The port candidate now sets the existing negative collision-window sentinel on
that successful late check. The corrected run records one 11-point hit rather
than damage on successive fields. This is a shared native ASM fix, not an
emulator workaround; broader original-roster regression remains required.

New test runs retain the exact executed Lua controller as `autoboot.lua`, with
its hash in execution.json, so later controller edits do not erase that input
evidence. The original source baseline and stock MAME executable remain intact.

### Native Knife/Ring implementation and two-sided smoke tests

`asm/KSPROJ.ASM` implements Kano's D,B+HP Knife and Sonya's D,F+LP Ring as
native actor/child processes. `KSCMD` owns the parsers and one-live-projectile
check. Original MKZAP allocator, PID routing, collision/Jade immunity, bounds,
object/palette reference counts and cleanup are reused; no character-ID proxy
or emulator hooks exist. Own descriptor slots use the donor knife/ring cores,
including Sonya's separate release-origin core. MKZAP's short PID/OID tables
now have explicit added-ID entries. KSPJANI contains named release/intro/flight/
impact scripts and original effect palettes, using existing packed graphics.

`qualify_projectiles.py` passed on `stock_wolf_projectiles_03` and
`stock_wolf_projectiles_mirror_04`: each is a 9,000-frame stock-MAME physical
input run, with 19 activations per move. Player sides are swapped in the second.
Initial wrong-direction commands did not dispatch these projectiles. Observed
spawn latencies are three fields for Knife and fifteen for Ring. Projectiles
retain true IDs and own art: 22 distinct knife and 11 ring shapes were observed.
Both moves dealt 22 unblocked / 5 blocked damage in these scenarios, recovered,
and cleaned up; each physical player had at most one live projectile. Both runs
reached their frame limit with ROM PCs and zero missing-root markers.

Visual review rejected versions 01/02 for Sonya's persistent charge palette.
KSPROJ now uses `player_swpal` so native `player_normpal` has its normal temporary-
palette flag; fresh screenshots show her green costume restored after release.
Interrupted-release/alternate-costume restoration is not yet runtime-qualified.
No native projectile launch cues are implemented. Whiff/spacing, close/crouched/
boss victims, balance and AI acceptance remain. Receipts pin the current program,
map, relevant action/engine/descriptor sources, controller and screenshots.
Earlier action/contact receipts are historical, not current-binary regressions.

### First two native special-command smoke tests

`qualify_initial_specials.py` checks two fresh 9,000-frame physical-input tests
on stock MAME: `stock_wolf_kano_ball_02` and `stock_wolf_sonya_square_01`.
The former recorded 20 cannonball activation episodes (action 0x20b); the latter
12 Square Wave episodes (0x207). Each first valid activation damaged the opponent
and returned to stance. The deliberately short initial LK hold did not launch
Kano's ball. The initial F,B+HP attempt against grounded Kano did not launch
Square Wave; all observed Square Wave starts had airborne Kano. Both runs reached
their frame limit, with ROM PCs, zero missing-root markers and no recovery exit.
These checks do not certify every command circumstance, block/whiff behavior,
precise timing/hitboxes or final balance. No native launch cues are implemented.

KANOMOV now owns an explicit seven-pose rotation script instead of indexing the
ordinary flip animation. SONYAMOV owns the imported three-pose Square Wave script
instead of using ordinary flip-kick main slot 30, and its contact pose no longer
comes from the ordinary punch table. `special_pose_review` records the exact
donor pose inventory used; runtime screenshots were inspected. Current program
and action-source hashes are pinned in each run's qualification receipt. Earlier
contact evidence is historical: its global source/runner paths subsequently
changed, so do not describe its pins as matching the newer binary.

### Native roster/contact test, subsequent integration fixes

`stock_wolf_game_contact_06/qualification.json` now records actual physical
selection of Kano (17) and Sonya (18), with matching native object IDs during
combat. In 71 sampled combat frames spanning frame 3620 through 4610, both
received damage and Sonya reached zero health. The full 9,000-frame run exited
normally with no sampled non-ROM PCs, no recovery capture and no missing-root
markers. This is a bounded high-punch contact test, not an all-moves pass.
Screenshots 3240 and 4800 were inspected: dedicated portraits, original border
and player-number rendering, own previews, and native `KANO WINS` result text.
Blink timing, pixel alignment, all UI transitions and floor shadows are not
accepted by those two stills.

Earlier tests intentionally remain failures: selection_01 reached Kano versus
AI but recovery-looped; selection_02 selected both but did not close distance;
selection_03 exposed damage callback overflow; contact_04 exposed reaction-start
callback overflow after the first damage; contact_05 reached round results then
read an invalid winner-text pointer. ASM fixes extend `ochar_damage_table`,
`ochar_power_punches`, `rs_calls`, `winner_text` and `winner_speech`. The new
winner speech entries are explicitly silent pending proper native DCS cues.
No character ID substitution or emulator/game-memory test forcing was used.

The preparation script includes these fixes. The original preparation receipt
is historical and does not describe the current source hashes; the contact
qualification pins the actual compiled sources, program/map and controller.

### First integrated Wolf gameplay candidate

`baseline/mk2-rebuild-main/srcp` is an isolated source candidate. Native
GSPA/GSPLNK compiled and linked the original game objects together with the
new actor roots, art, selector data, navigation and initial actions; BIGSREC
produced P12F8/FC ROM lanes. The first build rejected an overlong `.ref` line;
splitting declarations fixed it. The known baseline linker alignment warning
remains. `PBUILD.BAT` and `port/dosbox-game.conf` reproduce this build.

`baseline/stock_wolf_game_candidate_boot/execution.json` records a 12,000-frame
stock-MAME run with physical inputs only, exit 0, no timeout, and unchanged
emulator hash. Its controller selected original characters (IDs 1 and 11);
health decreased and a round ended. This is only a boot/original-character
regression smoke test, NOT new-character selection, combat or move acceptance.
The `--game` runner uses the candidate program ROMs and packed body/UI graphics.
The earlier preparation receipt describes the pre-build snapshot, not this
subsequently repaired and compiled source state. No playable-port claim follows.

`NEXT_INTEGRATION.md` records the concrete source integration points for the
next real roster/game candidate. `GROUNDING_MEASUREMENTS.json` records opaque
stance soles for all twelve original fighters and both donors; source baseline
ground offsets do not coincide with descriptor heights or a universal zero
sole/ground residual. These are measurements, not accepted new gameplay offsets.

There is now a selectable source-linked candidate with bounded contact and
eight-special smoke tests, but no complete playable port or final ROM patches.
Complete own animation-control coverage, remaining moves, finishers,
Shang morphs, roster/UI/ladder entries, hit/AI/victim tables, exact grounding,
shadows and new native DCS events remain. Existing custom-driver acceptance
tests do not certify any of this work. Initial source actions still require
runtime comparison and may need corrections; assembly/linking is not gameplay
verification.

The supplied source baselines retain known alignment/checksum/spike/ending
risks. The smoke tests do not prove a complete campaign. The proposed full
port targets Wolf-unit capacity; do not describe it as a drop-in T-unit PCB
upgrade. No new GitHub release is authorized until the requested ROM-side
implementation passes appropriate checks; the prior release is removed.
