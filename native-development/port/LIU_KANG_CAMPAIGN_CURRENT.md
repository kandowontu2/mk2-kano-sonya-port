# Kano versus Liu Kang: current controller work

Run568 clears five opponents naturally, then loses to Liu Kang. Recorded
damage events include opening native Bicycle Kick0204 for48 damage, repeated
native throws0507 for32, and uppercut0107. These are not sufficient evidence
of a port defect.

Run569 extends the stance-ready guarded-Knife controller to Liu (native ID1),
guarding fireballs/actions2/3/4, advancing specials0203/0204 and a live P2
projectile PID0800. The first five opponents are defeated unchanged. Liu's
four round health minima improve to29/95/95/90, but no round is won. The run
finishes normally at27247 fields after one paid continue. Current full-ROM,
own identity and no-fault audits pass; full campaign remains false.

Source/trace inspection exposes a controller handicap: all ordinary combat
input is gated by `combat>60`. At run569 fields20484–20498 Kano remains
stance0303 while Liu's Bike0204 closes from distance192 to84 and delivers48
damage. The controller has not yet begun guarding. Run570 is testing ordinary
Block+Away during those first60 fields specifically for the opt-in Kano/Liu
policy; other opponents' already verified strategy is unchanged. No ROM,
native AI, health, difficulty, action state or driver is altered.

Run570 completes27146 fields with one normal paid continue. The first five
opponents remain defeated; Liu wins all four rounds, with CPU minima95/51/68/51.
This is not a campaign solution. Full-ROM/identity/no-fault audit passes and
31 source/tooling tests pass. The initial-input correction must not be described
as a gameplay/ROM fix or a successful Liu matchup.
The opening trace does confirm the intended input effect: by20486 Kano is
native standing-block0700, and the20498 Bike contact takes6 blocked damage
instead of run569's48 unblocked damage. This narrow success does not imply
better overall survival or a round win.

## Post-hit guard comparison rejected for Liu

The harness now allows `--campaign-post-hit-opponent=1` to restrict the
opt-in post-hit delay to Liu, retaining the verified earlier ladder policy.
The default opponent filter is-1 (all eligible guarded-projectile matchups);
valid filter range is-1..18. This changes only the controller's physical
inputs, never native action, health, difficulty or AI memory.

Run575 tests the24-field post-hit guard against Liu with two normal paid
continues. It ends normally at29746 fields; Kano still clears the first five
opponents but loses all six Liu rounds, CPU minima139/139,156/95,129/112.
This does not improve on the earlier stance-ready guarded-Knife results, so
it is not adopted as Kano's preferred Liu policy. Full-ROM/identity/no-fault
audit and33 source/tooling tests pass; campaign/ending verification remains
false. No ROM or new release was generated for this controller comparison.

## Physical Ball comparison

Source review confirms KSCMD's own ID17 release gate requires held-LK age
strictly greater than050h native ticks, then ordinary restricted_xfer into
KANOMOV.ks_kano_ball. The existing physical Ball plan holds Block through81
fields and LK through85, then releases; the Liu-only variant adds Away while
charging to retain native standing throw-away protection.

Run576 (`--campaign-liu-ball`) bypasses only Liu's generic uppercut/guarded
Knife selection and uses that existing Ball plan. It completes27021 fields,
one paid continue. First five opponents are defeated again; Liu wins four
rounds at CPU minima161/151/161/161. Two native Ball020b action episodes are
observed, but the requested repeated charges do not establish repeated move
activation or successful hits. This is not adopted as the campaign strategy.
Future Ball controller work would need to confirm release eligibility after
charge interruptions, rather than infer activation from85 requested fields.
Current complete ROM/identity/no-fault audit passes;34 source/tooling tests
pass. No ROM, driver, AI, health or difficulty change was made.

## Why releases were rejected; state-ready Ball input

Run577 adds only bounded read-only flags/animation instrumentation and Liu
input logging to576. The complete campaign CSV remains byte-identical. At
LK releases20630 and20773, Kano is grounded and tagged0700, but process
flags0005 include pm_reacting0004. Native restricted_xfer rejects reacting,
sitduck0008 and special0010, so the action tag alone incorrectly suggested
release eligibility. The gate is functioning; this is not a ROM command bug.

The Liu Ball controller now keeps charging until grounded and those native
flags clear, lowers Block for four fields, then rechecks eligibility before
releasing LK. Its wait is bounded to300 plan fields; other Ball policies are
unchanged. Run578's sampled release20702 has flags0001 and height0, and the
full run observes nine native Ball020b episodes versus two previously.
Nevertheless Liu wins all four rounds, CPU minima146/141/161/151, after one
paid continue. End field28957; first five opponents defeated again. More
activations are not successful hits or campaign completion. Current complete
ROM/identity/no-fault audit and34 source/tooling tests pass.

Separately, audit_campaign_damage_window now verifies the exact observer
frozen with historical run550, pinned by its recorded SHA256, rather than
requiring today's evolving observer file. That historical549/550 byte-identical
read-only proof passes again; no original raw trace was edited.

## F650 current-program progression: run601

The48-field Kitana Knife interval plus20 logged native paid continues
earns a current-program Kitana2–1 win on attempt14 and advances to Liu.
The ordinary guarded-Knife Liu policy then loses14 rounds across attempts
14..20, with CPU minima117/139,29/95,134/29,151/156,90/90,73/112,139/139.
This is stronger damage in some rounds than the old-program comparisons,
but no Liu round or match is won. The run exits normally at85883 fields;
the full current26-chip/identity/no-marker/no-illegal-recovery audit passes.
No gameplay or AI code was changed, and full campaigns/endings remain open.

Next comparison: run602 keeps Kitana interval48 and sets only the optional
--campaign-liu-knife-interval=36 (default60, bounded24..120). The controller
uses it only for Kano against Liu; all other matchups preserve their prior
interval.53 source/tooling tests pass, including scoped/default contracts.
No native ROM or AI change is involved. Runtime outcome remains pending
until this existing run is terminal and its completed trace is audited.

Run602 is now terminal: normal exit at86117, full current-ROM/identity and
no-marker/no-illegal-recovery audit passes. The entire pre-Liu trace is
byte-identical to601:32553 data rows, header-inclusive prefix SHA256
98F68603E926CCC940B46D2B2D0EF9A4A3FAA9E2959B15BCAB1CB27E32D6AEEE.
This reproduces the current Kitana match win and isolates the changed
controller behavior to Liu. Liu still wins all14 rounds, CPU minima
139/134,94/90,95/156,73/51,73/112,68/134,90/112. There are no native Liu
player-winning result rows. The36-field policy is not a campaign solution.
The original60-field policy's29-HP minima were better in some rounds;
neither setting has proved a completed Liu match. No ROM change was made.

## Passive projectile-geometry comparison: run627 pending

The existing cpuProjectileActive guard returns true for any live pid_proj2
process, without projectile position/velocity filtering. This is a candidate
controller over-guard, not a demonstrated defect. Run627 repeats601's same
inputs (Kitana interval48, Liu60,20 paid continues) and appends only a passive
Liu observer. Its bounded/cycle-checked512-process scan reads the native
projectile's saved A8 object, signed X/16.16 X velocity, own position, action
tags and health. An away-and-beyond64 flag records geometry, not collision
safety or proof that an input should have been changed.

Three contract tests check MAINEQU procid/pa8, DISPEQU oxvel and the native
spawn_proj_proc assignment, read/pointer bounds and scoped passive inclusion.
No controls, health, AI, difficulty, positions, timing or ROMs are changed.
The actual627 trace must finish, match601 and be analyzed before inferring
that the observer was noninterfering or that guards were unnecessary.

Run627 is terminal: normal exit85883, current26-chip/identity/no-marker/
no-illegal-recovery audit passes. Its entire campaign.csv is byte-identical
to601, including the Kitana win and subsequent Liu losses. The passive
observer records10493 live-health Liu frames,375 with a CPU projectile;
zero have a projectile moving away beyond64, and zero have only such
projectiles. This trace does NOT support the proposed positional over-guard
fix. No guard behavior or native game code was changed based on that theory.

The matching601/627 gameplay trace SHA256 is
721E81EF383AECF6CF18B5707F753811573287A07D6042F4F47F00D4481E167B;
627's liu_projectiles.csv SHA256 is
8BC156581E208B3AC1CC281A7F289E922B2ED638FDE8B4254BACB15505773BAC.

Sampled damage correlations show substantial loss around Knife/recovery
and enemy stance tags, but tags alone do not identify each attack. The
next628 comparison adds --campaign-liu-rfp-duck: the existing bounded native
process/stack detector is used only against Liu, guarding detected low/final
rapid punches and ducking/countering detected high ones. It also avoids new
Knife plans below120 in that policy. Kitana remains on the successful48-field
policy. This is physical-input logic only, not an AI/difficulty/ROM change.
78 selected tests pass.628 is pending terminal audit and actual RFP telemetry.

Run628 is now terminal: normal exit88986, full current26-chip/identity and
no-marker/no-illegal-recovery audit passes. All32553 pre-Liu data rows match
601 exactly, reproducing the same current-program Kitana win. The detector
records3020 positive RFP-context fields:2149 low-root14h and871 high-root13h.
This verifies the native context classification was exercised, not that every
requested dodge/counter executed. Liu still wins all14 rounds; CPU minima
134/68,112/73,146/134,129/151,117/85,112/107,73/73. No native player-winning
result is recorded. Thus this is a working finite detector comparison, not
an adopted winning strategy or proof of a game defect. No ROM/AI/difficulty/
health changes were made; full campaigns/endings remain unverified.

## Spacing comparison: run629 pending

Run629 preserves601's successful pre-Liu policy and tries physical backup
below distance220 when grounded/native flags clear, ahead of starting a new
Knife. Active projectile/pressure guards and already-started input sequences
retain priority. Counter telemetry is enabled. It does not alter native
movement speed, AI, health, difficulty, positions or ROMs.

The run froze the initial spacing-controller revision. Local source was
subsequently refactored to an explicit retreating boolean so fallback guard
suppression follows the actual chosen branch, rather than re-evaluating the
distance predicate.79 selected tests pass on that local revision;629 must
not be presented as runtime coverage of the later refactor. Its frozen
autoboot.lua/hash remain the authoritative input-controller evidence.
Both matchup outcome and latest-refactor runtime behavior remain pending.

Run629 now exits normally at the90000-field observation cap, with termination
reason field-budget (mode3/map5/winner2). Current26-chip/identity/no-marker/
no-illegal-recovery checks pass. No Liu player-winning result is recorded;
the14 observed target rounds have CPU minima51/156,117/117,90/139,95/95,
139/51,139/73,7/139. The best7-HP minimum is not a round or match win.

Counter/main-trace joins identify2543 sampled grounded backup requests with
ordinary/stale-normal action tags and Block released;869 have unchanged X
across adjacent two-field samples. This demonstrates that requested backup
does not always produce movement, not that every such sample is a boundary
stall rather than native recovery/collision. Indefinite distance recovery is
not an adopted strategy. A bounded stall/cooldown policy would need to check
actual native flags and movement before another comparison. The later local
retreating-boolean revision remains untested by629's frozen controller.
No native game source, ROM, AI, health or difficulty changed.

## Bounded retreat comparison: run630 pending

The local controller now counts unchanged X only after a retreat request on
the immediately preceding field, while grounded and with native reacting/
sitduck/special flags clear. After12 consecutive stationary samples it
suppresses retreat for60 fields, allowing existing guard/attack decisions.
Movement, gaps and round transitions reset the stationary count. This detects
failed movement requests, not a proven specific wall/collision cause.

Run630 froze the current source after the retreating-boolean refactor and
counter telemetry additions (stall count/cooldown/request, native flags, X
coordinates and LP). Source and frozen observer SHA256 both equal
2CDF2847B25B4A7C2008A350AA6240B27BC7311BD176CE9F7B27544CCAD72010.
80 selected tests pass. The hidden below-normal campaign uses the same
bounded20 paid continues; outcome and actual cooldown behavior are pending
terminal audit. No game ROM/AI/difficulty/health changes were made.

Run630 now exits normally at90000 fields with reason field-budget
(mode11/map5/winner2). Full current26-chip/identity/no-marker/no-illegal
recovery checks pass. The actual cooldown telemetry records46 distinct
cooldown starts and2499 live-health fields within cooldowns, with zero
retreat requests during them.248 cooldown fields carry the Knife action
tag; this does not establish248 attacks/hits. The bounded input fallback
is exercised on the exact frozen source revision, not merely unit-tested.

No native Liu player-winning result is recorded. CPU minima are29/73,
90/117,85/68,117/139,139/139,73/139,139/95 over14 observed rounds. Thus
the controller no longer requests indefinite stationary backup, but it
still is not a successful match strategy. No native game rules, ROM, AI,
health or difficulty were changed. Full campaigns/endings remain open.

## Slow Knife cadence: run647

This current-ROM comparison uses the successful601 pre-Liu controls and
changes only --campaign-liu-knife-interval=120 (versus60). It does not enable
retreat or RFP-duck. The hidden below-normal process exits normally at86180
fields, reason left-campaign, after the bounded20 paid continues. The native
same-attempt result audit reproduces the Kitana match win on attempt14.
All26 current ROM chips, true identities, frozen controller, no missing roots,
no illegal recovery and no guest-memory/register writes pass the audit.

All14 Liu rounds are lost. CPU minima by attempt14..20 are117/139,95/139,
139/139,29/139,117/139,139/161,139/73. There are50 sampled Knife-tag episodes;
these are not50 certified launches/hits. Slower cadence is not an adopted
winning strategy and these losses are not themselves proof of a port defect.

compare_campaign_prefix.py records all32707 trace data rows before the first
mode2 Liu matchup as exactly equal to601, SHA256
47763F7A93BB00B097EB0E917028ED1F657C9BBD7775CB81203F5553C4DF4001.
This includes result/intro rows, unlike the earlier32553-row combat-only
comparison; the counts do not contradict each other. The report pins both
traces, receipts, frozen controllers and comparison script. Four helper tests
reject missing target, earlier changes and column changes while permitting
target-matchup differences. The selected local suite now passes88 tests.
Full campaigns, later bosses and earned ending/cast/credits remain unverified.

## Close Choke comparison: run660, first current Liu match win

The optional --campaign-liu-choke controller changes only Kano-versus-Liu
physical inputs in601's successful prefix. At grounded distance<=85 with
native reacting/sitduck/special flags clear and the opponent grounded, it
releases guard until observed stance303, then uses the verified D,F,LP
timing (Down0–2, Forward6–8, LP12–15). It cancels on native reaction, waits
at most45 fields for stance, retries no faster than100 fields, resets each
round, and suppresses fallback guard during the command. No native game,
AI, health, difficulty, positions or outcome state are modified.

Run660 exits normally at88630 fields, reason left-campaign after the bounded
20 paid continues. All26 current ROM chips, own identities, frozen read-only
controller, no missing roots and no illegal recovery pass the campaign audit.
The native same-attempt result counters verify a2–0 Liu match on attempt18:
frame77976 counter1/0 with Kano6HP/Liu0; frame79244 counter2/0 with Kano9HP/
Liu0. The trace includes103 paired actor535/victim536 Choke observations
against Liu; these are sampled fields, not103 separate holds or certified
damage pulses. Earlier attempts14–17 lose their eight Liu rounds.

All32707 pre-Liu trace data rows exactly match601, same prefix SHA256
47763F7A93BB00B097EB0E917028ED1F657C9BBD7775CB81203F5553C4DF4001.
The frozen controller and current campaign_probe.lua SHA256 are
5E6903727D13C4C30FF8DB06800C2855A6D6F71E3CA46C451D47041616FE29C8.
The audit records natural wins over Baraka, Reptile, Jax, Raiden, Kitana and
Liu, then genuine advancement to map6/Sub-Zero. All six Sub-Zero rounds on
attempts18–20 are lost, CPU minima161/161,161/121,161/121. This is new finite
campaign progression, not campaign completion, boss or ending proof.

The selected92 source/tooling tests pass. One existing source-contract
assertion was updated to require the added Choke suppression alongside the
unchanged Leg Grab suppression; the new check covers matchup scoping,
native stance/reaction handling, timing, retry/reset bounds and no writes.
No test outcome/native-game requirement was relaxed to obtain this win.
