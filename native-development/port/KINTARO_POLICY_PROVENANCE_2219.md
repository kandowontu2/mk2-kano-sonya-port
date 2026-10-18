# Boss-controller provenance correction

The current Sonya clear's authoritative inputs are the terminal
`stock_wolf_2219_sonya_campaign/execution.json` and its frozen `autoboot.lua`.
The receipt enables `--campaign-sonya-kintaro-evade` and
`--campaign-sonya-kintaro-early-evade`, but **does not** enable
`--campaign-sonya-kintaro-guard`. No `boss_context.csv` exists in that run.

Consequently the guarded 100-distance, 36-field cooldown, crouch-table-ready
counter branch must not be described as Sonya's successful campaign policy.
It is an existing alternative controller branch. The opt-in Kano
`--campaign-kano-kintaro-evade-counter` trial reuses that alternative and is
experimental, not a replay of the successful Sonya inputs.

In the frozen successful controller, ordinary boss offense falls through to
the shared uppercut policy: Down, HP pulses at `combat % 24 < 3` when distance
is below 115, or the earlier airborne-enemy 12-field pulse branch. Early native
stomp evasion has priority. Kano's earlier baseline already uses corresponding
shared pulses and stomp evasion, so simply re-running those settings is not a
new hypothesis. Their different campaign outcomes alone do not prove a ROM
defect, and do not authorize changing boss balance or difficulty.

The new trial preserves the earlier Kano human route and uses physical inputs
only. Source/unit-test success alone is not a campaign clear.

## Terminal result

`stock_wolf_2219_kano_kintaro_evade_counter` finished at field153887 with
exit0, no timeout, stock emulator, no custom driver, and no game-memory writes.
The completed `CAMPAIGN_AUDIT.json` verifies current ROMs, no missing markers,
and no observed illegal-opcode recovery. It records16 Kintaro rounds across
paid attempts25–32, **zero native Kintaro round wins**, and best remaining
boss HP101. Three rounds have no observed boss damage. Some rounds timed out
with positive player HP; neither survival nor HP minima count as a win.

This alternative performed worse than the prior ready104 counter's best
observed boss HP21, and worse than stance-ready Knife's69. These minima are
finite observations, not comparable seeded difficulty benchmarks. Do not
repeat this policy unchanged or describe it as a gameplay fix. No native ROM
change was justified by the failed controller result.

## Close-ready84 result

`stock_wolf_2219_kano_kintaro_ready84` completed at field161475, exit0 without
timeout. Its terminal campaign audit verifies current ROMs and physical-only
inputs. The readiness audit records24 valid requests,24 native Uppercut
entries within8 fields, and24 linked20-HP damage windows. There are no missed
activations in this finite request set, but also no native Kintaro round wins
across16 observed rounds. Best remaining boss HP is81.

The earlier ready104 trial had117 requests,90 native entries and49 linked
20-HP windows, with best remaining boss HP21. Thus ready84 eliminates misses
in the sampled requests but substantially reduces offensive opportunities.
Accuracy is not campaign completion. Neither trial indicates a broken
Uppercut implementation; further work must address timing/survival rather
than merely tightening this threshold again. The existing84 preparation
experiment was a different controller with a60-field cooldown; this one
retains the ready counter's6-field request guard and native recovery rules.

## Standing High Kick result

`stock_wolf_2219_kano_kintaro_short_kick` completed at field150965, exit0
without timeout, on the unchanged current ROM. Its terminal campaign audit
records16 Kintaro rounds, best remaining boss HP113 and zero native boss
round wins. This standing-HK alternative is not a solution; do not repeat it
unchanged. The failed controller trial is not evidence that High Kick needs
different strike data or that Kintaro should be weakened.

## Retreating Ball result

`stock_wolf_2219_kano_kintaro_retreat_ball` completed at field170288, exit0
without timeout. The terminal campaign audit verifies current ROMs and
physical-only input. `KINTARO_BALL_CHARGE_QUALIFICATION.json` rechecks39 logged
releases: every one has more than80 consecutive observed LK-held fields and
a sampled native Ball entry within8 fields. No interrupted-charge release is
counted as a success. This proves finite activation, not attributed damage.

There are18 observed Kintaro rounds, zero native round wins, and best
remaining boss HP35. No victory or ending follows from this trace. Ball's
native charge/release works in these requests; a further experiment should
address finishing/survival, not alter its native charge gate or damage. A
bounded low-HP switch to the already-tested stance-ready Knife is a distinct
physical-input hypothesis; it has not yet been implemented or tested here.

## Low-HP Ball-to-Knife result

`stock_wolf_2219_kano_kintaro_retreat_ball_finish_knife` finished normally.
The terminal audits record33 complete physical charges and33 native Ball
entries. The50-HP-or-less switch issued one stance-ready Knife request with
one native entry. Across18 Kintaro rounds the best remaining boss HP was49,
with zero native round wins. This hybrid did not improve on the earlier Ball
run's35-HP minimum. Do not treat its input activations as a boss clear or
repeat it unchanged. No native gameplay change followed from the result.

## Early crouch-ready counter result

`stock_wolf_2219_kano_kintaro_early_ready104` removed the controller's60-field
opening inactivity only for Kano versus Kintaro; native readiness/range gates
and all ROM bytes remained unchanged. It completed at field164195 with exit0
and no timeout. The terminal audit records155 ready requests,118 sampled
native Uppercut entries and67 linked20-HP damage windows.

Two native round wins occurred: attempt26 round2 (match counters1–1) and
attempt27 round1 (1–0). These are **different paid attempts**, not one match
clear. All18 observed Kintaro rounds are retained. The best boss HP minimum0
does not override the missing same-attempt two-win result.

The preceding65146 sampled trace rows match ready104 byte-for-byte up to
Kintaro's first combat field; earlier human matchups were preserved. The ready
log begins at field130294 with distance192 instead of the old first observation
at130354/distance62. Earlier reaction therefore occurred, but full survival/
campaign completion remains unproved. A bounded64-continue,300000-field trial
of this now-round-winning policy is separate pending evidence, not a clear.

The extended `stock_wolf_2219_kano_kintaro_early_ready104_endurance` trial
subsequently completed at field286338 with exit0 and no timeout. Across82
observed boss rounds it logged708 ready requests,517 native Uppercut entries
and293 linked20-HP damage windows. Its only two native round wins are the same
attempt26/27 results above; no additional round win or full Kintaro match clear
was obtained in the extra continues. Do not repeat this policy unchanged or
infer success from the greater number of sampled hits. Native ROMs/AI remain
unchanged, and the failed extended controller is retained as finite evidence.

## Native six-hit-queue variety result

`stock_wolf_2219_kano_kintaro_varied` completed at field158819, exit0 without
timeout. It reads Kintaro's actual six-word incoming hit queue; MKDRONE's
`count_q_repeats` scans these six entries, and MKBOSS punishes three repeated
flying kicks or punches. No queue, AI, hitbox or damage value was written.

The terminal variety audit validates all logged queue counts/decisions. It
records56 kick plans,52 punch plans and53 Knife plans; sampled native entries
were53/49/49 respectively. Requested plans are not counted as successful hits.
There are16 Kintaro rounds and zero native round wins. The best remaining
boss health is6HP in attempt31 round2.

That close round was not a healthy finishing opportunity: Kano had only1HP
when Kintaro reached8HP. At field153685 the controller started another jump
punch from116-pixel separation; Kintaro later remained at6HP when Kano lost.
This does not support claiming a clear or simply adding more continues. The
next useful investigation is safer grounded launch spacing/retreat and corner
handling, rather than weakening native repeat punishment or damage rules.

The separate `stock_wolf_2219_kano_kintaro_varied_spacing` trial completed
cleanly, exit0/no timeout. Its 16 boss rounds yielded no native round wins;
minimum boss HP was69. It requested34 kicks/20 punches/7 Knives, with33/17/6
sampled native activations. Grounded retreat below175, held until220, caused
6740 retreat fields and fewer attack opportunities. One continuous retreat
lasted292 fields; sampled positions show both players moving while the boss
followed, not a proven corner collision. A distinct bounded-spacing trial
limits each physical retreat episode to48 fields before waiting for actual
stance and attacking. This is an experimental controller change only.

That bounded trial, `stock_wolf_2219_kano_kintaro_varied_spacing_bounded`,
completed at159411 fields, exit0/no timeout. All current-ROM/frozen physical
input/clean-log campaign checks pass. Across16 boss rounds it recorded44 kick,
58 punch and41 Knife requests, with41/43/37 sampled native entries. Actual
logged retreat totaled3599 fields; its longest continuous run was48, confirming
the cap operated. Best boss HP was17, but there were zero native round wins
and no full Kintaro match. This restores attack opportunities versus unbounded
spacing but does not prove a clear or justify repeating unchanged. The next
investigation is native close-range exchanges versus retreat/jump timing.

The distinct `stock_wolf_2219_kano_kintaro_varied_counter` experiment adds a
close-range branch to the bounded variety controller. At <=104 separation it
physically holds Down and requests HP only after actual native duck-dispatch,
body<=96, eligible grounded flags and grounded opponent are observed, with
six-field minimum request spacing and three-field pulse. Readiness requests
are logged separately in kintaro_ready_counter.csv; queue-based ranged requests
remain in kintaro_variety.csv. The terminal auditors must check both logs and
native counters, not confuse an uppercut request with a hit or a match win.
The earlier human route and native gameplay code are unchanged. Result pending.

The hybrid subsequently completed at157751 fields, exit0/no timeout. Both
terminal auditors pass:49 kick/48 punch/17 Knife requests yielded47/47/13
sampled entries;43 ready uppercut requests yielded35 native107h entries and
18 linked damage windows. Across16 boss rounds, minimum boss HP was47 and
there were zero native round wins. Retreat remained capped at48 consecutive
logged fields (2233 total). This is a regression from bounded variety's17HP,
not an earned campaign clear. Input recognition is demonstrated; repeatedly
rerunning the same policy or changing native recovery/damage is not justified.

The separate `stock_wolf_2219_kano_kintaro_varied_adaptive` trial retains the
bounded variety policy without the regressing close-uppercut hybrid. Requested
air attack age is now clamp(floor((distance-80)/4),10,28), logged per request.
It tests earlier physical attack inputs for close launches instead of assuming
the fixed28-field delay suits both116- and192-pixel gaps. This is a controller
hypothesis, not verified geometry/contact or a ROM change. The terminal audit
checks logged timing against actual request distance and seeks native entries
relative to each requested age. Result pending; no win or hit inferred.

The adaptive trial completed at157863 fields, exit0/no timeout. The audit
validated each logged age against its launch distance:68 airborne requests
kept age28, while35 used earlier ages10..27. Across16 boss rounds it requested
55 kicks/48 punches/28 Knives with49/40/25 sampled native entries. Best boss
HP was36; zero native round wins. Retreat totaled3274 logged fields and never
exceeded48 continuously. Thus earlier physical inputs were actually tried,
but did not improve on the bounded fixed-timing trial's17HP minimum or earn
a match. Current-ROM/frozen-input/clean-log checks pass; full clear remains
unproved. Do not convert this failed controller experiment into a ROM timing
or damage change without independent game-defect evidence.

## Stomp escape phase-tracking defect in the test controller

Read-only postmortem of the first variety trial shows the first stomp escape
at130451 began with Kano already77 pixels airborne from an offensive jump.
The old controller immediately set stompJumped=true from that old airborne
state. Kano landed by130479 but received no new Up request. He then walked
at2 pixels/field, reachingX466 versus the saved stompX374 at130529 (92px).
The source psycho_fall_call checks horizontal separation<060h once below
050h height; native stomp damage56 followed at130534. Jump height itself
does not exempt a victim from that native horizontal-only check.

The separate `stock_wolf_2219_kano_kintaro_varied_stomp_refresh` trial retains
fixed28 mixed attacks and bounded retreat. Only its opt-in Kano escape path
counts airborne state after a new Up request made during this stomp phase.
An older offensive jump no longer suppresses a new jump after landing.
The existing Sonya/controller paths and all native game code remain unchanged.
435 local unit cases pass. Runtime escape behaviour and earned wins remain
pending, not inferred from this source-level controller fix.

The refresh trial completed at160388 fields, exit0/no timeout. Terminal
current-ROM/frozen-input/clean-log audits pass. All12 contiguous logged
old-air/ground/new-Up cases subsequently show new airtime, confirming this
specific controller fix operated. There are11 HP-drop windows preceded by a
stomp action tag; these are sampled tag associations, not complete causal
stomp attribution. Across16 boss rounds, minimum boss HP was60 with zero
native round wins. Mixed requests55/51/52 yielded49/45/45 sampled native
kick/punch/Knife entries. The tracking fix is not a campaign-clear claim or
evidence for weakening native attacks.438 local unit cases pass; no emulator
remains from this run.

The refresh trace at138186 requests Left fromX711 during a stomp; the boss
subsequently repositions toX698. Kano crosses back through that target and is
atX643 versus698 by138204, preceding a56HP drop at138210. This motivates the
separate `stock_wolf_2219_kano_kintaro_varied_stomp_momentum` trial: at escape
direction selection, preserve signed native own horizontal velocity when
there are at least128 pixels to that edge, otherwise choose the roomier side.
It retains the refresh fix, bounded retreat and fixed28 air attacks. It reads
own velocity and sends directions/Up only; no movement or target RAM is written.
439 unit cases pass. Trial result and any escape benefit remain pending.

The momentum trial completed cleanly, exit0/no timeout. All12 observed
old-air/new-Up cases reached fresh airtime. Six sampled HP-drop windows were
preceded by stomp tags versus11 in refresh-only; these are neither complete
causal stomp counts nor a seeded balance comparison. Across16 boss rounds,
minimum boss HP was65 with zero native round wins. Mixed requests50/53/43
yielded45/45/40 sampled native entries. It did not earn or improve a clear.
Native ROM/gameplay remain unchanged. A separate earned-lethal victim pilot
is now being run sequentially to close another actual acceptance-coverage gap.

## Vertical jump-kick trial

After completing all112 lethal-victim cases, the separate
`stock_wolf_2219_kano_kintaro_vertical_kick` trial tests native vertical
jump-up kick (act_jupkick=010eh), not diagonal0200h/0201h attacks. MKBOSS's
explicit repeated-flip landing checks name only the diagonal tags; vertical
stationary attacks still have their own native block/counter behaviour, so
absence of that one repeat rule does not imply success. Physical Up is held
for3 fields without horizontal input, then HK at48..51, using timing already
verified for normal vertical-contact clips. Requests require real grounded
eligible stance/button table/body>=120 at separation<=115; farther ground
movement approaches physically. The controller retains opt-in stomp refresh
and momentum direction, logs kintaro_vertical.csv, and changes no native
recovery, damage, AI, health or game state.445 unit cases pass. Outcome pending.

Timing correction: the first vertical controller incorrectly treated the
normal-contact fixture's attackAge48 as jump-relative. That fixture starts
its jump at age20, so the verified relative delay is28 fields, not48. The
first run was deliberately stopped at the human ladder (last complete sampled
field49746, map4/attempt10), with its frozen trace retained as an aborted
controller experiment. It is not a completed campaign or a game failure.
Only the exact identified trial emulator PID71048 was stopped.

`stock_wolf_2219_kano_kintaro_vertical_kick_v2` uses physical Up at1..3 and
HK at28..31, preserving the other profile and opt-in escape handling. The
independent terminal auditor requires this timing in the frozen controller,
actual ground/eligible/stance dispatch for each request, and samples native
010eh actions separately from requested plans and native round counters.
447 local unit cases pass, including relative-delay and unready-request
rejections. Corrected runtime outcome remains pending.

The corrected v2 trial completed at152469 fields, exit0/no timeout. Its
terminal audit validates94 grounded/eligible/stance jump requests, with32
sampled native010eh kick entries in the expected window. Across16 Kintaro
rounds it obtained zero native round wins and minimum boss HP113. Seven
logged old-air/ground/new-Up escape cases include five with subsequently
observed airtime; a requested Up is not always a completed escape. Three
sampled damage windows were preceded by stomp tags, not a complete causal
stomp count. The vertical policy is substantially worse than prior mixed
attacks and is rejected as an improvement. No emulator remains. A native
move-activation observation is not a campaign clear or a reason to change
ROM recovery, hitboxes, boss AI or damage.

Read-only v2 postmortem separates missed requests from actual kicks:32 missed
windows contain303h/30bh/503h (stance, vertical jump, hit reaction);6 contain
303h/503h without sampled jump. Other missed windows include native507h boss
grabs and407h stomp interruptions. These tag sets are sampled associations,
not complete causal attribution. Several shown HP drops occur before age28.
MOVES do_jumpup_kick gives the native attack16 strike frames. The distinct
`stock_wolf_2219_kano_kintaro_vertical_kick_early` trial requests HK at10..13
instead of28..31, keeping the same readiness/range, jump and escape policy.
Each request logs its attackAge; the audit checks it against the explicit
receipt flag and samples the matching entry window. Native strike duration,
movement, damage and AI are unchanged.447 unit cases pass. Outcome pending.

The early trial completed at152264 fields, exit0/no timeout. Its terminal
audit validates79 ready requests at age10 and46 sampled native010eh kick
entries, versus94/32 for age28. Nevertheless, across16 boss rounds, minimum
boss HP worsened to129 and there were zero native round wins. Five logged
old-air/new-Up escapes all show new airtime; three sampled damage windows
were preceded by stomp tags. Thus recognition/activation improved without
useful damage or survival. The vertical approach is rejected; no further
unchanged repetition or ROM balance changes follow from this result.
No emulator remains. All112 lethal victim cases have meanwhile been
requalified from retained traces against current tools, and their exact full
proof-hash audit passes without any additional emulator launch.

## Guarded native-recovery counter trial

`stock_wolf_2219_kano_kintaro_recovery_counter` tests physical crouch-block,
releasing Block and requesting an uppercut only while the boss process/return
stack is observed in the linked MKBOSS range goro_strike_missed..goro_block
(missed/blocked strike recovery and roar). Addresses come from the actual LST
relocated with the linked kahn_start symbol, with bounded ROM-range checks.
Grounded eligible own flags, native duck table/body<=96, grounded opponent,
distance<=104, no CPU projectile and minimum6-field request spacing remain
required. Three-field HP pulses are physical input only; no native recovery
is shortened. Early stomp escape/refresh/momentum takes precedence. Read-only
kintaro_recovery_counter.csv includes the gate and enemy wake pointer, and
the terminal auditor rejects requests lacking the recovery gate. This is a
new timing/survival hypothesis, not a verified clear. No ROM balance edits.

The recovery trial completed at158255 fields, exit0/no timeout. Terminal
readiness/current-ROM/frozen-input checks pass:14 gated fire requests became
14 native uppercuts and14 linked damage windows. Across16 boss rounds there
were no native round wins, minimum boss HP121. The log contains2775 observed
recovery-gate fields but only152 prepare/14 fire fields versus15010 guard
fields, so verified contact alone leaves too few opportunities. No emulator
remains.449 local unit cases pass. The full112 lethal cases were also rechecked
from existing traces and their current exact-coverage/proof-hash audit passes;
no second emulator or game-memory write was used.

Recovery distance review found1528 gated fields at105..160 separation and
732 beyond160, versus515 within104; only1337 gated fields were also own-grounded
and eligible. The14 fire gaps were62..96. The new separate
`stock_wolf_2219_kano_kintaro_recovery_counter_approach` trial releases Down
and Block and walks toward only at105..180 separation, while both grounded,
eligible, no CPU projectile and the same linked recovery gate remains active.
At<=104 it stops walking, prepares real duck dispatch and uses the unchanged
counter readiness gate. At loss of recovery it returns to guard immediately.
Read-only logs add actual toward/Down/Block inputs; the terminal auditor
rejects approach rows outside these limits.450 unit cases pass. Outcome
pending; this is not a change to hit range, native movement or boss behaviour.

The approach trial completed at155934 fields, exit0/no timeout. Its terminal
audit validates all366 physical approach fields under the intended gate and
16 ready fire requests. All16 become native uppercuts;14 linked damage windows
are observed. Across16 boss rounds there are zero native round wins and best
boss HP141, worse than stationary recovery-counter121. Phase counts are13050
guard,366 approach,205 prepare,16 fire and16 pulse. The physical approach
operates but does not provide a better strategy, so it is rejected rather
than repeated or used to justify ROM balance changes. No emulator remains.

## Windup-reactive mixed aerial trial

A firsthand player tactic describes aerial attacks timed to Kintaro's
uppercut attempt rather than a fixed jump age:
https://www.trmk.org/forums/threads/how-to-beat-kintaro-and-shao-kahn-in-mk-ii.33180/
This is a hypothesis lead, not proof for Kano or a claim of universal success.
The separate `stock_wolf_2219_kano_kintaro_varied_reactive` trial keeps the
six-hit-queue kick/punch/Knife selection, bounded spacing and refreshed
momentum-aware stomp escape. For aerial plans it observes the linked native
goro_uppercut..goro_kick process/return-stack range, requests the selected
attack on the first observed windup at age>=6, or falls back at28. The input
pulse lasts at most4 fields. It does not edit/shorten the enemy windup or
change movement, attack physics, damage, AI or game memory.

Read-only kintaro_air_timing.csv records each plan's request frame, age,
windup flag, own height, first chosen attack age and actual HP/HK inputs.
The independent auditor checks the first eligible trigger/fallback and exact
pulse, then counts sampled native actions separately from requested attacks
and native wins.452 local unit cases pass. Runtime outcome remains pending.

The reactive trial completed at156849 fields, exit0/no timeout. The audit
initially rejected its trace because it assumed plan age1 executes on the
request field. The frozen controller's elseif chain executes new plans on
the next field: first request130294, age1 at130295. Correcting that checker
offset (and adding a shifted-trace rejection test) makes the unchanged trace
pass exact trigger/fallback/input-pulse checks. No runtime was rerun/edited.

There are50 kick/47 punch/25 Knife requests with47/42/21 sampled native
entries.94 aerial plans reach a fire input:57 use the28-field fallback and
37 trigger earlier at6..25; three other aerial plans are interrupted before
fire. Across16 boss rounds, minimum boss HP87 with zero native round wins.
The reactive policy actually ran but did not improve the earlier mixed
results. It remains failed campaign evidence, not an AI/physics bug or a
reason to modify native balance. No emulator remains. The112 lethal traces
were requalified without another emulator, and their full hash audit passes.

## Original mixed spacing with a low-HP finishing choice

`stock_wolf_2219_kano_kintaro_varied_finish` explicitly restores the first
variety controller's spacing: retreat only for Knife below175, no later
aerial-retreat hysteresis, no later escape-refresh/momentum or reactive timing
options. Normal six-hit queue selection remains unchanged while boss HP>13.
At<=13 it requests the longer-active diagonal kick rather than punch/Knife,
even when the queue would normally choose another move. The source threshold
is a physical move-selection hypothesis, not changed damage, queue contents,
AI, health or outcome. Native kick repeat punishment remains fully intact.

The terminal audit validates the explicit low-HP exception, counts actual
native entries and native results, and compares the earlier campaign trace
to the original first-variety run up to the first changed move-selection
request. A mismatching prefix will be reported rather than assumed preserved.
455 unit cases pass. This experiment's result, prefix equivalence and any
finishing hit remain pending; it is not a campaign-clear claim.

The finishing-choice trial completed at159581 fields, exit0/no timeout.
The independent prefix comparison matches76842 sampled campaign rows before
field153685 against the original first-variety run. Exactly one move-selection
override occurs there, with Kintaro8HP; thus the earlier close opportunity
was actually reproduced, not assumed from similar profiles. Mixed requests
61/52/58 yield58/49/54 sampled native kick/punch/Knife entries. Minimum boss
HP improves only to5, and all16 boss rounds still have zero native round
wins. The changed final kick is not a successful finishing hit. No emulator
remains. The source/test tooling up to launch was published at
dbd7bb7481186c3ba4baf908b3c7abc135fdc5a9; this terminal outcome is local follow-up.

The separate `stock_wolf_2219_kano_kintaro_varied_finish_uppercut` trial keeps
the same original mixed spacing/selection above20 boss HP. Below that threshold
it stops choosing new aerial plans and holds Down, requesting an uppercut
only after actual eligible ground/duck dispatch/body<=96, grounded opponent,
distance<=104 and minimum6-field spacing. Existing native moves/recovery and
all boss behaviour remain unchanged. The kick override is disabled in this
mode; readiness requests are logged in kintaro_ready_counter.csv. The prefix
comparison boundary is the first low-health counter observation, not a later
successful input. No request is counted as an activation or win without the
separate native audit.456 unit cases pass. Runtime result/prefix remain pending.

The finishing-uppercut trial completed at159849 fields, exit0/no timeout.
Its prefix matches76779 sampled rows before153559, but this is an earlier
takeover than the kick trial: the20HP rule triggers at19 boss HP, player1HP,
gap162 and enemy38 pixels airborne. Thus it suppresses the original next
aerial attack that would have produced the later8HP opportunity. There are
193 duck fields, one ready fire request/native uppercut and zero linked
damage windows. Minimum boss HP stays19; all16 boss rounds have zero native
round wins. This does not test the same8HP decision point and must not be
described as though it does. A tighter threshold would be a different finite
experiment; no game damage/range/AI change is justified. No emulator remains.

The separate `stock_wolf_2219_kano_kintaro_varied_finish_uppercut13` trial
uses explicit --campaign-finish-uppercut-threshold=13. Default20 remains
available for reproduction of the earlier failed experiment. The13HP rule
preserves the original19HP aerial plan before considering duck/uppercut;
actual prefix equivalence and whether the8HP opportunity is reached must
still be audited. Readiness/range/input timing and native game bytes are
unchanged.456 unit cases pass, including13/14 threshold boundaries. Runtime
outcome remains pending; no finishing contact or campaign clear is inferred.

The13HP trial completed at161302 fields, exit0/no timeout. It matches76842
sampled campaign rows before153685 against the original first-variety trace,
reproducing the actual8HP opportunity. At153692, player1HP/boss8HP/gap95,
native grounded duck/body68 dispatch qualifies one uppercut request. One
native107h entry and linked8HP depletion are observed at153700. Native mode5
results prove a Kintaro round win at153892, attempt31 round2, counters1-1.
This is one earned round, not a match: the deciding round was lost. The trial
observes17 boss rounds and no completed Kintaro match or campaign clear.

Because this precise finishing change now earns a native round win, the
separate `_endurance` trial extends only the declared budget to64 paid
continues/300000 fields. All input policy flags and threshold remain the same;
no AI/difficulty/HP/damage/win state is changed. It is bounded, hidden and
BelowNormal with one emulator.457 unit cases pass, including budget/profile
preservation. Extended outcome remains pending; more attempts are not wins.

The64-continue endurance trial completed at276392 fields, exit0/no timeout.
Across81 observed Kintaro rounds, its only native round win is the same
attempt31 round2/result153892 already proved in the32-continue run. No further
round win or full Kintaro match was earned in the extra attempts. Two ready
finishing requests became two native uppercut entries; only the original
8HP depletion window is linked to one. The earlier76842-row prefix still
matches. No emulator remains. This policy must not be repeated unchanged or
treated as a clear merely because the minimum observed boss HP is0 once.

The streaming damage-distribution audit of this same retained endurance run
now separates sampled HP losses by attempt/round and both adjacent action
tags. It finds81 boss rounds; the next closest after the earned round is
attempt45 round2 (boss minimum4HP, player minimum1HP). This is not another
win. Common player-loss samples include70 losses of40HP with prior actions
0/0 and62 losses of56HP with boss action1031 on both adjacent samples.
These are action adjacency, not causal identification: tags may be stale or
replaced by hit/recovery. The next policy investigation should examine these
large-loss windows and the actual linked boss routines before choosing an
input change, rather than extending the unchanged losing policy again.
KINTARO_DAMAGE_DISTRIBUTION.json pins the retained trace/controller/receipt;
the scanner reads CSV incrementally without launching MAME.463 unit cases
pass, including HP-reset, round/attempt boundary and noncombat-gap checks.

The attempt31 deciding-round losses occur at154474 (40HP),155002 (56HP),
155242 (40HP) and155540 (remaining25HP); boss HP there is114/74/66/55.
Native MKREACT slammed_by_goro explicitly loads decimal40 before damage;
MKBOSS goro_pycho_hit explicitly loads038h (56). These source amounts match
the large observed losses, but sampled action tags do not independently prove
the active damage routine at each event. The final loss has boss tag1287,
so it must not be labeled another stomp based on proximity alone.

The current MKBOSS source is NOT byte-identical to the supplied original:
two category shifts call ks_boss_category and its helper is appended. The
new actual-build-source regression test proves the complete file is exactly
integrate(supplied original), with no extra boss edits. Existing exhaustive
helper tests restrict altered classification to true Kano/Knife0211h and
Sonya/Ring0212h; original identities/actions retain original categories.
Thus original boss damage/spacing/timing code is preserved, while the native
new-projectile integration remains explicitly acknowledged.464 tests pass.

The new stock_wolf_2219_kano_finish13_stomp_refresh trial combines only the
13HP finishing policy and old-air/new-Up stomp refresh, without momentum or
an extended continue budget. The first invocation was rejected by the CLI
combination guard before any run directory or emulator existed. The guard
now explicitly admits refresh alongside finishing; no Lua/game code changed.
The successful launch uses a fresh directory,32 continues, one hidden
BelowNormal emulator (observed main window handle0, working set200MiB).
465 unit tests pass. Runtime is in progress; neither a win nor a finished
execution is inferred from launch. Separate audits will inspect readiness,
escape intervals, native round results and damage after terminal execution.

This combined trial is now terminal at159868 fields, exit0/no timeout.
All16 boss rounds lost, minimum boss HP29. Mixed requests67/51/66 produced
61/51/56 sampled kick/punch/Knife entries.16 old-air/new-Up escape intervals
were observed,15 followed by new air, with7 pre-drop stomp-tag damage windows
(not causal proof). The13HP finishing threshold was never reached; no fire
request occurred, so inspect_kintaro_ready_counter correctly rejected the
trace instead of certifying a positive activation. The wrapper stopped at
that failed audit; escape and streaming damage audits were subsequently run
against the same saved terminal trace, without another emulator. This
combination did not improve the earned-round policy and must not be repeated
unchanged. No game/ROM edits or native full-match/campaign clear occurred.

Knife-spacing follow-up on that retained trace: the66 requested Knife plans
include starts at gaps202/235, above the controller's175 minimum. At130778
the gap235 becomes211 at130786,187 at native Knife529 entry130794,163 at
130802 and139 at130810; player HP remains146 across this sampled sequence.
Thus a request-time minimum is not the clearance remaining during projectile
recovery: the CPU can close96 pixels in32 fields. Native can_goro_slam permits
distance<=120 and does not exclude airborne opponents (the exclusion is
commented out in the supplied original). This sampled example is not itself
a grab and must not be labeled one. It demonstrates why the controller's
175 launch threshold cannot guarantee staying outside grab range throughout
the input/launch/recovery interval. Any new spacing trial should retain the
mixed attack policy, explicitly measure launch and recovery clearances, and
bound retreat rather than rerun the rejected pure-Knife260 policy or create
another endless follow/retreat loop. No gameplay patch is warranted yet.

The fresh stock_wolf_2219_kano_finish13_knife260_bounded run now tests
--campaign-knife-clearance=260 with the original mixed/13HP finishing policy,
not pure Knife or stomp refresh. Default175 remains unchanged. Only Knife
preparation requests a wider gap; extra retreat has a48-field elapsed cap,
after which normal cooldown/readiness still applies and a launch may occur
below260. Therefore260 is a target, NOT guaranteed safe clearance. Existing
variety CSV records actual request gap/retreat decisions; campaign samples
must establish launch/recovery clearance and native results after termination.
The wrapper admits only explicit260 with varied-finishing and propagates it
to the physical controller environment.466 current unit tests pass; they
do not certify the new policy's effectiveness. One hidden BelowNormal emulator
is running under the normal32-continue budget. No game/ROM bytes changed.

inspect_knife_clearance.py now streams64-field post-request windows, preserving
request gap separately from actual sampled action529 gaps and HP minima.
Against the earlier terminal finish13_stomp_refresh trace it finds66 requests,
56 windows with native Knife samples and9 with a Knife-tag gap<=120. These
are not nine proved grabs; HP changes/action adjacency do not identify the
active damage routine. New unit cases distinguish request/action distances,
exclude samples beyond64 fields, and terminate windows on noncombat entry.
468 full unit cases pass. The new wider-gap runtime is still active; no
improvement or successful clearance is inferred before its terminal audit.

The knife260 bounded trial has now finished at159137 fields, exit0/no timeout.
Its16 Kintaro rounds yield zero native wins, minimum boss HP53. Retreat is
actually bounded:2603 logged fields, longest contiguous interval48. Across
71 Knife requests,59 windows contain native Knife samples and25 include a
Knife-tag gap<=120. This is worse than9/56 in the earlier combination (the
different policy/route means this is not a controlled causal comparison).
The48-field fallback allows unsafe launches and wider request spacing alone
does not solve the recovery exposure. Do not repeat this policy unchanged or
claim260 guarantees clearance. No emulator remains, no gameplay/ROM change
was made, and Kano's full boss match/campaign remains unearned.

New finite timing trial stock_wolf_2219_kano_finish13_boss_continue_delay60
keeps the original mixed/13HP finishing combat policy and32-continue budget.
Only the buy-in controller changes: after a Kano boss loss (map>=15), hold
coin/start released60 fields before replaying the existing120-field purchase
input cadence. Human-ladder and initial boss inputs retain default timing;
there is no explicit difficulty/RNG/AI/state write or guaranteed improvement.
Default delay0 preserves prior input cadence. The wrapper admits only explicit
60 with the Kano boss profile.470 current unit tests pass; the actual changed
buy-in timing and native results still require retained-trace inspection.
The new run is active, hidden/BelowNormal with one emulator; no completion
or win follows from launch. No native game/ROM bytes changed.

The delayed-buy-in trial is terminal at158748 fields, exit0/no timeout.
Its16 Kintaro rounds have zero native wins; minimum boss HP68. The dedicated
event-latency audit observes32 purchases: all human-map selection latencies
remain141 fields and boss-map latencies are201, versus141 in the original
finish13 trace. Thus the intended timing difference occurred, but did not
improve the boss result. This checks native event latency, not raw per-field
coin/start pin transitions. Do not extend/repeat this policy unchanged or
claim a campaign clear. No emulator remains.471 full unit cases pass.
