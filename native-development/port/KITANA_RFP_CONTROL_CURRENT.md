# Native rapid-punch observation and controller comparisons

Current ROM remainsF65002019A05D47400BD755B95C06546B9ADD104140472A111F1D107C3F6D512.
No game, driver, AI, difficulty, health or victory-state changes were made.

MKDRONE.drone_rfp calls init_special without assigning a new action tag.
Its repeated animation sleeps can therefore appear as stance0303 in the
ordinary CSV. The optional --campaign-kitana-rfp-duck controller recognizes
the linked routine's wake/return address, reads its native punch counter,
and examines at most8 longwords within the actor's own process stack
(psdata3d0h..prcsiz6f0h). Every read is bounded; no state is written.
Routine addresses come from the current MAP/LST, not stale absolute PCs.

Run586 tries ducking during the detected combo, then guarding when its count
reaches1. It loses all ten Kitana rounds after reaching her on paid attempt1.
1283 detected RFP fields are logged. Actual player actions show that many
duck requests occur during Knife/reaction states, not an eligible duck.
An input request does not cancel native recovery. The counter also need not
reach1: a missed punch exits early into the unpunch routine.

Run587 avoids starting Knives below distance120, distinguishes the final
unpunch code region, and requests a normal uppercut only from an actually
grounded duck with no reacting/sitduck/special flags. It still loses all ten
Kitana rounds, CPU minima51/95,73/117,73/95,95/73,73/117. Damage during some
duck requests invalidates the assumption that every RFP is a high attack;
it does not by itself prove a collision-box defect.

Native drone_rapid_hi uses animation13h; drone_rapid_lo uses14h. The saved
RFP animation argument distinguishes them. Run588 guards low punches and
ducks/counters only high punches, raises guard in unpunch recovery, and also
guards the previously idle first60 fields specifically against Kitana.
The log observes386 high-root fields and1692 low-root fields. The run ends
normally at37653 fields after five paid continues, but loses all ten Kitana
rounds, CPU minima51/95,95/7,73/73,117/139,117/29. Its33 uppercut and150 Knife
episodes are totals across the whole campaign, not proof of all requested
Kitana counters landing. This is not adopted as a successful match strategy.

All three runs retain the four same-attempt verified wins through Raiden.
Their complete current-ROM/true identity/no missing-marker/no illegal-recovery
audits pass.48 source/tooling tests pass. Full campaigns, later ladders and
earned endings/credits remain unverified; no new ROM patch/release was made.

## Projectile interval comparison: run599

The optional --campaign-kitana-knife-interval=36 shortens only Kano's
Kitana command retry interval (default60, bounded24..120). Native readiness,
fan-threat guard and physical command sequences remain unchanged. Other
opponents retain60. No ROM/AI/difficulty/health modifications are involved.

Run599 exits normally at37553 fields with five explicit paid continues.
The full current-ROM/no-fault audit passes and verifies the first four
opponents again. Its pre-Kitana trace is byte-identical to run584:
9867 data rows, prefix including header SHA256
49605F6AEBE36509F03097ED7CAD3FC7B3FB50C27659895790F0507771165EEC.

Kitana attempt1 round2 is a native player win at22078 with round counters
1/1 (not a completed match). The attempt is lost in round3. No later Kitana
match is won. CPU minima by attempt are161/7/7,7/73,117/7,51/51,29/95.
Thus the shorter interval produces one finite round win but does not solve
the matchup.49 source/tooling tests pass, including scoped interval/default
contracts; whole-campaign and ending acceptance remain false.

Run600 tests interval24 with the same remaining flags and five paid
continues. It exits normally at36488; current full-ROM, own-identity,
no missing-marker and no illegal-recovery checks pass. The first four
matches are again verified. Kitana attempt5 round2 is a knockout win at33662,
with player/CPU round counters1/1; the following round and match are lost.
CPU minima by attempt are139/51,95/7,51/117,7/51,73/0/95. Neither interval
comparison proves a completed Kitana match, so neither is accepted as the
campaign solution. No game code, AI or difficulty was changed.

## Current-ROM Kitana match win: run601

Interval48 with20 explicit paid continues finishes normally at85883 fields,
not a timeout. Current full26-ROM/own identity/no missing markers/no illegal
recovery auditing passes. Baraka, Reptile, Jax and Raiden are again verified
as complete same-attempt matches. Kitana is defeated2–1 on paid attempt14:
native round1 result62820 has player/CPU counters1/0 and Kano1 HP; native
round3 result65106 has counters2/1 and Kano6 HP. Both are player-winning
results with CPU HP0. This is a currentF650 match win, unlike the earlier
program run568 comparison.

The run advances normally to Liu Kang, loses all14 rounds across attempts
14..20, and exits the campaign. Liu CPU minima are117/139,29/95,134/29,
151/156,90/90,73/112,139/139. No ending/full-campaign claim is made and this
is not a1CC. Only physical controller timing changed; ROM/AI/difficulty/
health/victory state were not modified. The remaining Kano campaign work
starts with Liu; a repeatable cheaper Kitana strategy is still desirable.

## Sonya guarded Ring comparison: run604 pending

Run603's successful current-program Raiden policy is retained. The optional
--campaign-sonya-kitana-ring enters the same ready-stance guarded projectile
controller only for Sonya versus Kitana. It uses Sonya's physical Down/
Toward/LP sequence, waits for native readiness, and guards fan threats and
the configured post-hit window. This is not a ROM or AI modification.
The option requires --sonya.56 source/tooling tests pass; the initial7404
complete runtime data rows match603 exactly before the target matchup.
Do not infer a recognized Ring or a match win merely from this option:
the existing604 process must finish and its trace be audited first.

Run604 now exits normally at82912 fields. Current full-ROM/own-identity,
no-marker/no-illegal-recovery audit passes. All20479 pre-Kitana data rows
are byte-identical to603 (header-inclusive SHA256
C34E82BC685F7BF6141ACCEC5D9EC8842A1FA58C6E5A029FA392C23EF395D32B),
including the same Raiden2–0 win. Kitana still wins all28 target rounds.
CPU minima in the target rounds reach29 and7, but no native winning result
is recorded. The audit observes108 Ring action-tag episodes0212 against
Kitana; this is neither108 recognized commands nor108 hits, since tags can
persist after interruption. The guarded Ring policy is not yet a match-win
strategy. No native source/ROM/AI/difficulty change was made.

Campaign audits now separate sampled action-tag runs per opponent, resetting
at round/attempt boundaries. A regression test covers repeated samples,
new rounds/paid attempts and opponent isolation;57 source/tooling tests pass.
The distributed-package source check was rerun after report regeneration,
so its qualification pins the current evidence instead of stale report hashes.

## Sonya Ring interval comparison: run605 pending

Run605 changes only Sonya/Kitana's Ring retry interval to48 (default60,
bounded24..120). The interval option requires the explicit Sonya/Kitana
Ring policy; no other matchup, including Raiden, uses this value. Native
readiness and fan/post-hit guarding remain unchanged. The hidden stock-MAME
campaign uses the same20-continue bound. Outcome remains pending until its
existing process is terminal and the complete trace is audited.

The interval-scope regression brings the selected source/tooling suite to58
passing tests. Eight separate synthetic patcher tests also pass: deterministic
roundtrip/input preservation, overwrite refusal, bad source/patch/result,
unsafe/duplicate target, unsafe patch path and incomplete chip-set rejection.
These66 selected tooling tests are not whole-game acceptance. No playable
ROM or AI changes were made.

Run605 now exits normally at83404 fields, with current full26-chip/identity,
no-marker and no-illegal-recovery checks passing. The pre-Kitana20479 rows
match604 exactly (SHA256 C34E82BC685F7BF6141ACCEC5D9EC8842A1FA58C6E5A029FA392C23EF395D32B),
reproducing Raiden2–0. Kitana wins all28 rounds again; the best CPU minimum
is46 rather than604's7. There are136 sampled Ring-tag runs against Kitana,
not136 proved hits/recognized commands. The48-field interval is not adopted
as an improvement. No native program or game rules changed.

## Sonya Ring with close Leg Grab: run614 pending

The optional --campaign-sonya-kitana-leg-counter requires the Sonya/Kitana
Ring policy. It preserves60-field Rings and the existing Raiden strategy,
but tries a block-first Down+Block/LP chord at distance<=85 only when both
actors appear grounded and native reacting/sitduck/special flags are clear.
Controls release for four fields before the chord; another request waits
at least90 fields. Reaction cancels the request. Only physical inputs are
sent; no health, AI, position, difficulty or action state is written.

The input state machine has a scoped/recovery/input-order regression test;
72 selected source/tooling/patcher/local-ROM-verifier tests pass. Counter
telemetry is enabled for this comparison. A requested chord is not proof
of a recognized Leg Grab or a hit: run614 is pending terminal audit and
target-matchup action/paired-state inspection. No game ROM changed.

Run614 now exits normally at84521 fields with current full26-chip/identity,
no-marker/no-illegal-recovery checks passing. Raiden is again defeated, but
Kitana wins all28 target rounds. The best CPU minimum is16. Against Kitana
the audit records19 seek-tag runs0219 and four hold-tag runs021a;92 sampled
rows pair own hold021a with victim action021b. Thus actual paired grabs are
observed, not merely requested LP/Block. This does not prove every request
or damage event. The combined tactic is not a completed-match solution.
No native game source, ROM or AI was changed.

## Tight-range Leg / ranged-only Ring comparison: run619 pending

The619 variant of the optional Leg-counter policy starts Leg requests only
at distance<=72, rather than614's85, and starts new Ring plans only at
distance>=120. Physical move windup/recovery still applies; these controller
gates do not freeze spacing or guarantee a hit. Native game code/damage/AI
remain unchanged. Other matchups, including the prior Raiden strategy, keep
their controller behavior.72 selected source/tooling/patcher/ROM-verifier
tests pass. The existing619 campaign is pending its terminal outcome.

Run619 is now terminal: normal exit88870, current full26-chip/identity and
no-marker/no-illegal-recovery checks pass. Raiden is again defeated, but
Kitana wins all28 rounds; best CPU minimum29. No Leg seek/hold tag run is
observed against Kitana. The tighter gates removed the paired-grab behavior
seen in614 rather than producing a match win; they are not an adopted
successful tactic. No native program, AI, difficulty or health was changed.
