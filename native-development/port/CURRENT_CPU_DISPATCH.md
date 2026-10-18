# Current CPU dispatch / sampled attract observations

Correction: historical "Mileena" campaign references for ID 7 mean RAIDEN.
Native MILEENA is ID 5. See CAMPAIGN_ID_CORRECTION.md for corrected scope.

Current linked-ROM/source checks pass16 listed dispatch tables and five
explicit scalar extensions. Original typed rows are now compared directly
against MKDRONE.ASM in the supplied rebuild ZIP, not a working backup file.
Dispatch and scalar reports are saved separately so neither overwrites the
other's evidence. This is not an arbitrary-indirect-caller safety proof.

Attract runs367/368 each complete30000 fields on stock MAME with current
program/graphics pins and immutable read-only observers. Both naturally
observe Sonya as Player2 (774 sampled object observations each, all matching
the selected identity), including native Ring action530. No missing markers,
fault file or current-link recovery PC observed. Neither run observes Kano.

The old summarizer hardcoded a recovery address from an earlier ROM. It now
reads the current link map and refuses mismatched archive program/graphics.
Selected-identity matches are recorded separately from raw object counts.
These bounded sampled attract observations are NOT full CPU gameplay, all
specials, original-roster regressions, campaign or release acceptance.
No AI/gameplay code was changed or character forced into a demo.

Longer run369 also completes42000 fields without recorded faults and still
samples only Sonya among the added fighters. It is not new Kano coverage.
Source review confirms all three natural choice paths (two montage sides
and bio CPU choice) call randu14 and map indices12/13 to trueIDs17/18; the
original random helper is unchanged. test_demo_roster.py checks those exact
source paths and canonical helper preservation. This proves source eligibility
for Kano, not that a sampled run actually exercised Kano's AI or every branch.

## Current-link physical campaign attempts372/373

Both use the current SoundP/program/graphics and stock MAME, with no game RAM,
health, stage, AI or difficulty writes. The controller adds forward late jump
kicks outside95 pixels and ordinary backward-LK sweeps inside that range against
Reptile; other opponents retain the existing uppercut strategy. ROM code is
unchanged. Both traces pass audit_campaign_run.py's all26-chip and identity
checks, with zero missing markers/recovery observations and no Lua errors.

Kano372 beats Baraka twice, then loses both Reptile rounds (minimum CPU HP109
and135). Sonya373 beats Baraka twice and wins the first Reptile round with67HP
remaining. She loses the second with Reptile at16HP, then loses the deciding
round without damage. Both terminate on the real campaign loss/continue mode;
neither retries silently or claims a completed campaign. This improves observed
Sonya CPU-match coverage, not campaign/boss or final port acceptance.

## Ending-enabled link: bounded jump-timing exploration

The input-only campaign controller now accepts --campaign-kick-age=N (6..28),
recorded in execution arguments. Runs385/386/387 test18/16/20 fields after jump
input. All three use the same current ending-enabled ROM and pass the complete
ROM/identity/no-missing/no-recovery/no-Lua-fault campaign audit. Each naturally
beats Baraka twice, but none advances past Reptile. At18, Sonya wins one round
and loses the others with CPU HP10/22. At16, CPU minima62/161; at20,29/135.
The earlier22-field attempt384 had a win then CPU minima16/161. These finite
timing probes do not establish a ROM defect or campaign completion. Further
blind repetition of these exact profiles adds no useful coverage; change the
controller's tactical recovery/defense next, without changing game difficulty,
AI, health, stage or outcomes. Full campaigns/bosses/endings remain unverified.

Recovery experiment388: inspect_campaign_damage.py reports sampled incoming
hit contexts from audited traces (adjacent actions are not proof of causation).
Many385 hits occur at close collision spacing or during action0 recovery.
An optional --campaign-defense controller variant cancels an attack plan on
observed damage, crouch-blocks24fields, and holds Block after the jump-kick input
window. This changes no game bytes. It improves observed Baraka winning health
to127/135, but loses both Reptile rounds with CPU HP141/82, worse than385.
Do not promote that tactic as an improvement or blindly repeat it. Run388 still
passes current26-ROM/identity/no-missing/no-recovery/no-Lua-error audit; it is
not evidence of completing the later ladder, bosses or new ending routines.

Controller reachability fix402: reptilegrapple previously waited until60pixels
to initiate its grab although native collision spacing can be62. The threshold
is now75, changing physical inputs only. Current SoundP/program/graphics run402
still loses to Reptile, but actually performs three leg seeks and one hold; the
previous371 attempt never reached the leg action. CPU_LEG_SAMPLE.json verifies
23 consecutive sampled hold frames at2-field intervals, Reptile's matching
victim action, stable Sonya health during the hold, one35-damage release and
Sonya returning to stance. All current ROM/identity/fault checks pass.
This is one genuine CPU-opponent special interaction, not campaign completion
or exhaustive CPU/move acceptance. No difficulty, AI, health or game bytes changed.

Jump/grapple403 reaches new coverage: Sonya physically defeats Baraka and
Reptile2-0, then loses to Jax at ladder position2. Reptile combines14 jump-kick
episodes/six leg seeks/four paired holds across the attempt. The first round's
last mode2 sample retained CPU HP6, but native result-mode5 records CPU HP0,
winner1 and player round counter1; the second result counter reaches2. This was
not established as a timeout. audit_campaign_run.py now requires two native
result states/counters for advancement, not only HP minima inside sampled
combat rows.402's existing Baraka-only result also rechecks correctly.

Current full ROM/identity/no-fault gates pass. Player health at Reptile results
is59/106. No game code, difficulty, AI, health or outcome was modified; the
controller adds jump approach before using the native grab in collision range.
Later ladder/bosses/endings remain unverified; Jax needs a different tactic.

Jax tactics404/405: applying jump/grapple to Jax loses both rounds (CPU minima
135/154), so it is not an improvement there. Optional --campaign-jax-ring uses
the physical D,F+LP Ring command at range and leg chord close up.405 preserves
the earned Baraka/Reptile2-0 path, wins the first Jax round with75HP, loses the
second with Jax at17HP, then loses the third with Jax at146HP. It observes24
Ring action episodes and seven paired leg holds across the attempt. Full ROM,
identity/no-missing/no-recovery/no-Lua-fault audit passes; no game ROM/difficulty
or AI change. The auditor was initially invoked before405 had finished and
correctly failed on its absent terminal receipt; the same live process was
polled to exit0, then audited. No concurrent duplicate/retry was started.
One winning Jax round is new matchup coverage, not a completed Jax match or
campaign. Later roster/bosses/endings and complete Ring/victim interactions
remain unverified.

Kano406 on the current16-clip/ending-enabled link uses the improved physical
jump/grapple profile. Native result/counter proof confirms Baraka2-0, followed
by two Reptile losses (CPU minima44/128). Three Choke seeks and one Choke hold
episode are sampled across the attempt. Current26-ROM/own-ID/no-missing/
no-recovery/no-Lua-fault audit passes; this does not qualify complete Choke
damage geometry against every CPU or a Kano campaign. Sonya's Reptile success
must not be transferred to Kano. Both full campaigns/bosses/endings remain open.

Kano407: optional --campaign-kano-knife sends the real D,B+HP Knife command
at range and D,F+HP Blade close up against Reptile. Native result/counter
evidence verifies Baraka2-0, then Reptile2-1 (Kano health72/90 in the winning
rounds), reaching Jax at ladder position2. It samples27 Knife action episodes
and one Blade episode across the attempt. Jax still wins both rounds. Current
full ROM, true-ID and no-fault checks pass; the game/difficulty/AI/outcome is
unchanged. The observer session was polled to actual terminal exit before the
successful audit; no duplicate process was started. This is new earned Kano
ladder/CPU-move coverage, not either character's complete campaign or endings.

Kano Jax probes408/409 keep the earned Baraka2-0/Reptile2-1 sequence. Extending
Knife/Blade to Jax408 loses both rounds (CPU minima46/112). Optional physical
--campaign-knife-guard409 crouch-blocks after Knife launch against Jax only,
with a60-field plan limit; it also loses both rounds (CPU minima102/134).
These are not campaign improvements and must not be rerun unchanged as useful
new coverage. Both pass current ROM/identity/no-fault audit; no ROM/difficulty,
AI, health or outcome edits. The result verifier now additionally excludes
result rows preceding that round's first combat observation, so an earlier
attract/result state cannot satisfy advancement evidence.
Jax remains unbeaten by either complete test profile; bosses/endings remain open.

Common own-action dispatch follow-up (413/414)
--------------------------------------------
The original common lookup could bypass the boss classifier or read beyond
the propulsion table for own action tags. The native sparse lookup now handles
explicit own-ID/action pairs before falling through to unchanged original
tables. The first implementation (412) failed with an illegal-opcode recovery;
that failure remains evidence. Its signed-word FFFF terminator was replaced
with zero. Do not characterize 412 as a passing test.

Corrected Sonya413 passes the ROM/identity/no-fault audit across 13,541 fields:
earned Baraka2-0 and Reptile2-0, then two losses to Jax. Original Liu Kang414
passes the same structural/no-fault checks across 10,159 fields: Baraka2-0,
then Reptile losses. Neither is a complete campaign or boss-runtime proof.
The independent clean rebuild passes all129 object comparisons and four
program-part comparisons; the26-chip qualification against413 passes.

The source lookup interpreter checks87,552 identity/action/Jade combinations
(19 identities,0x900 actions,two Jade states), including carry, A0 restoration,
A1 preservation, sparse stride, zero termination and original-ID fallthrough.
Together with the boss-helper suite all five unit tests pass. This is host
source interpretation, not target execution. The compiled-record qualifier
separately verifies48-bit records, pointers, zero sentinels and4,608 signed
lookup cases. Actual boss encounters and complete campaigns remain open.
The development ZIP still predates this dispatch change until explicitly
refreshed and requalified; these findings must not be attributed to that ZIP.

Kano415 on that corrected dispatch link passes current26-ROM/identity/no-fault
audit across15,050 fields. Native results prove Baraka2-0 and Reptile2-1;
Jax wins the match2-1, with Kano health65 in his winning round. Observations
include47 Knife and three Blade action episodes. This is the first current
dispatch Kano runtime coverage, not a completed campaign. No game-state,
health, difficulty or outcome writes were used. Bosses/endings remain open.

Physical Jax sweep/block comparison416 changes only the Jax controller branch
via --campaign-jax-sweep. Earlier Baraka/Reptile results reproduce415 exactly,
but Jax takes no damage in either round (CPU minimum161/161). This strategy
is worse, not progress toward campaign completion; do not rerun unchanged.
The14,044-field trace passes current ROM/identity/no-fault checks. The retained
optional controller is a failed diagnostic, not the default or release logic.
The source regression suite still passes all five tests; no ROM was rebuilt
or modified for this experiment. Further work must diagnose the missed attack
opportunities rather than infer a game defect from this controller loss.

416 trace inspection:785 Jax combat samples contain only five sweep-action
samples (one episode, distances97 down to76), versus184 block-transition
samples. This suggests poorly timed inputs, not demonstrated broken sweep
collision. Follow-up417 adds an explicit neutral-release/Back+LK plan and
approaches within75 before starting it. It still produces only one sweep
episode and zero Jax damage, losing both rounds. The13,808-field trace passes
the current ROM/identity/no-fault audit. Therefore the timing hypothesis is
not established as the cause and this profile is not campaign-qualified.
Both417 and416 are retained failed diagnostics; no ROM gameplay edits.

Development package refreshed after415-417 (supersedes the stale-ZIP note
above): MK2KS_NATIVE_DEVELOPMENT_IPS.zip is5,450,875 bytes, SHA256
A15844C03F39D9818B2302EEA48EEDA770BCA0B4299781B17907B1556A972DFE.
It includes the current native program, both new CPU/boss source generators,
58 own ASM modules and explicit remaining-gate warnings. Both independent IPS
decoders and the actual user patcher roundtrip match all26 current chips.
The local PLAY_CURRENT_NATIVE.cmd points at that refreshed roundtrip set.
Ten combined IPS/CPU/boss unit tests pass. This is still development-only;
no final release or full campaign/boss/ending acceptance is claimed.

Physical throw approach477-479: optional --campaign-jax-throw changes only
Jax inputs, approaches65 and sends a released/neutral LP burst. Kano477
reproduces earlier Baraka/Reptile wins but loses Jax (CPU minima161/127),
with one own throw-action episode. Sonya478 inadvertently used default10-field
jump-kick timing, losing Reptile; it is not a controlled Jax comparison.
Corrected479 explicitly uses --campaign-kick-age=18, reproduces Baraka2-0 and
Reptile2-0, then loses Jax without damage (161/161). All three pass current
26-ROM/identity/no-fault audits; no game/health/difficulty/AI writes. Throw-only
Jax strategy is a failed diagnostic, not a release gameplay change or reason
to repeat the same test. Native JOY toss checks include facing, airborne,
landing, wall and CPU checks; proximity alone does not guarantee a throw.
Campaign/boss/ending verification remains open.

Ranged jump-kick Jax profiles480/481 use explicit18-field kick timing and
unchanged earlier ladder inputs, jumping toward only beyond180 and away
otherwise. Both reproduce earned Baraka/Reptile wins, then lose Jax. Kano CPU
minima109/154; Sonya109/135 (her first round ends without HP reaching0 in the
sampled combat rows, so do not call it a knockout). Full ROM/identity/no-fault
audits pass across13,968/13,196 fields. Sonya's Jax trace has only three CPU
damage reductions total, at ranges60-62, plus repeated CPU throw/hit actions;
the ranged policy does not maintain a productive attack distance. Own0200 is
native flying kick and060d its recovery (MAINEQU), not missing special tags.
Do not repeat this controller unchanged or weaken the ROM to manufacture a
campaign result. Bosses/endings remain untested; all release flags stay false.

Legacy video investigation found tools/audit_finished_video_delivery_20261015.py
and older completed campaign controllers, but their runner launches custom
mk2ks with sample/artwork paths. Those videos/results are NOT stock-MAME native
port acceptance. Only a physical-input tactic was adapted: new optional
--campaign-jax-reactive observes native ground-pound action0137, jumps away,
and sends short Leg inputs from grounded ready states with48-field cooldown.
Current Sonya482 (explicit18-field earlier jump timing) reproduces earned
Baraka/Reptile wins, then loses Jax with CPU minima91/91. The trace samples
12 Leg seeks/10 holds across the whole campaign; this is finite native matchup
coverage, not a complete campaign. Full26-ROM/identity/no-fault audit passes
through13,197 fields. No legacy driver/artwork/audio payload or game-state
writes were imported. Older footage must not be presented as this ROM's videos.

Explicit normal paid-continue testing521/522 supersedes the prior Jax-unbeaten
note. Optional --campaign-continues=0..5 uses only Coin1/Start in native buy-in
mode3, then ordinary selection. CSV attempt ordinals and separate buyin/
selection/combat events preserve every loss; round segmentation and winning
results are now attempt-specific (old traces default attempt0). No difficulty
settings, native AI, health, ladder or outcomes are edited.14 unit tests pass,
including reused round-counter segmentation after a continue.

521 is NOT a qualified Kano campaign: identity audit caught Liu1 after the
first continue. Startup HP had leaked into the first selection field when its
global timing phase was0. The physical controller's initial bootstrap is now
restricted to pre-campaign non-selection mode; no ROM selector fix was needed.
The failed run is retained and not filtered into campaign success.

Fresh522 passes all actual26-ROM/identity/no-fault checks for24,836 fields.
Kano remains17 throughout all combat and earns Baraka2-0, Reptile2-0 and
Jax2-0 on attempt0 (winning Jax health33/96), reaching Mileena7 at map3.
Three physical paid continues there each preserve map3 and true Kano identity;
the controller ultimately loses. Native result/counter proof establishes all
three cleared matches. Both the cleared-Jax and three valid native continues
are new coverage, not a complete campaign/boss/ending proof. Initial bootstrap
timing differs from older runs, so do not attribute the victory to a game-code
or AI/difficulty change. Current ROM program bytes remain unchanged.

Kano523 adds optional physical Knife/Blade zoning only for Mileena7; earlier
Baraka/Reptile/Jax results reproduce522. It wins a Mileena round, loses that
match, pays one native continue and wins Mileena2-0 (health23/29), reaching
Kitana4 at map4. Kitana remains unbeaten after two further paid continues.
The27,410-field trace passes actual26-ROM, true-ID and no-fault audit; every
loss/continue stays in evidence. Native result counters prove the attempt1
Mileena match win, not merely a low HP sample or timeout assumption.

Sonya524 with corrected bootstrap and normal Ring/Leg Jax policy now earns
Baraka2-0, Reptile2-0 and Jax2-1 on attempt0 (winning health35/23), reaching
Mileena. Three paid continues preserve Sonya18/map3; Mileena still wins.
The26,106-field trace passes the same full audit. Both characters now have
verified native Jax wins; next campaign obstacles are Kano/Kitana and
Sonya/Mileena. Native ROM bytes, difficulty and AI remain unchanged. Bosses,
later opponents and endings remain open; no full-campaign/video claim.

Female-roster projectile zoning525/526 is a finite failed physical-policy
comparison, not a ROM change. Kano525 reproduces523 through the earned Mileena
win and reaches Kitana, but Knife/Blade there still fails after the remaining
paid continues. Sonya526 preserves the three earlier match wins; Ring/Leg
damages Mileena but never wins that match across three native continues.
Both pass all26-ROM/true-ID/no-fault checks for28,034/26,003 fields. Every loss
and native continue remains in trace; no outcome, AI or difficulty edits.
Do not rerun these profiles unchanged or infer complete campaign coverage.

Mixed physical zoning527/528 also fails to clear Mileena. The optional policy
uses every third ranged Kano attack as a normally charged Ball, or attempts
Sonya Square only when the opponent is sufficiently airborne. Five normal
paid continues and explicit45000-field host bound are allowed; subprocess
wall bound is90s only with --campaign-long, with hidden/below-normal execution.
Kano527 ends31,735 fields at map3, six actual Ball episodes, worse than523/525.
Sonya528 ends36,406 fields at map3, one actual Square episode and174 Rings,
also without a Mileena match win. Both retain earned first-three match wins,
all five accepted native continues, exact26-ROM identity/no-fault acceptance.
These are failed controller strategies, not native gameplay changes or reason
to rerun them unchanged. Original successful Knife-only Kano Mileena profile
remains available; later campaign/boss/ending coverage remains unachieved.

Guard/punish529/530 is another bounded failed physical-policy comparison.
It reads native projectile/recovery/grounding states, guards during ranged
pressure, and attempts Blade/Leg only from ready grounded states. Kano529
preserves the earned Mileena win but loses Kitana across remaining continues
(31,962 fields). Sonya530 preserves first-three wins, samples62 Leg seeks/
28 holds across the full campaign, but still loses Mileena (35,817 fields).
Five accepted normal continues each retain original ladder position and true
own identity. Both pass exact26-ROM/no-fault audit; no game/AI/difficulty writes.
Neither establishes later campaign progress, and neither should be rerun
unchanged as a claimed improvement. Motion correctness remains distinct from
the controller's ability to beat the stock opponent policy.

Back-guard531/532 follows the actual JOY.tchk4/is_stick_away opponent-input
check: add away only during defensive states, not during move commands. This
is physical input, not throw immunity or a modified native check. It still
fails the next matchups: Kano/Kitana32,291 fields, Sonya/Mileena35,545 fields,
five accepted native continues each. Whole native ROM/identity/no-fault audits
pass and earlier earned wins remain. Sonya has23 hold episodes versus28 in530;
this is not demonstrated improvement. Source-based rationale alone cannot
qualify the strategy or claim all CPU throws were rejected. Keep failures and
do not rerun unchanged. Campaign/boss/ending and final release gates stay open.
