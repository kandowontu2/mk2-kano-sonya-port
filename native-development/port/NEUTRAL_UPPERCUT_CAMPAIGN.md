# Kano/Sub physical neutral-uppercut trial

## Follow-up: prepare before close pressure

Terminal result:119110 fields, exit0/timedOutfalse, normal left-campaign after
the32-continue limit on Mileena/map7. Current26-ROM/stock/frozen-controller
audit passes. Kano beats Sub-Zero2–0 on the SAME attempt18:
round1 result80660, counters1–0, player98HP/CPU0;
round2 result82256, counters2–0, player34HP/CPU0.
All8 uppercut requests activate and show40HP/victim-hit evidence. All4 spaced
Knife commands activate; requests80427 and81847 observe the final1HP loss.
No complete Mileena match/full campaign win is certified.

The39776 pre-Sub rows remain byte-identical to the standing-Knife trial,
SHA25625932FE2098D118A2EA2005FECA59A40767FA7A7C156F5614FF5D47AA64762DA.
Diagnostic SHA256CB51243F8AE5E7B4D3AA709F45B0EB305DCA8B433550A0E472F387F98377569C.
This is a real native campaign progression result with physical input only,
not combined wins from separate continues or a modified game balance.
No emulator remains after the run; Mileena is the next controller gap.

Original early-preparation plan:

`stock_wolf_2219_kano_early_prepare` is active hidden/BelowNormal, same native
ROM/arguments and120000-field/32-continue bounds. Only the physical strategy's
preparation/approach distances change: begin the Down/input-table preparation
at<=140 rather than84, stop far forward approach at160 rather than100. Actual
HP request remains<=84, actual duck-height/table readiness, cooldown60 and
the same threat/reaction gates. Knife finishing logic is unchanged.

Rationale: earlier close-entry preparation repeatedly spent its readiness
transition inside CPU pressure/throw range. Starting farther away may finish
the transition before the enemy enters HP range. These are requested movement
and input timings, not changed native hitboxes/ranges/AI. All323 tests pass;
the request-evidence tests still reject HP at85. No campaign win is claimed
before actual terminal round/match audit.

The source MOVELIST_NATIVE.txt now explains the verified post-block/rising
input pitfall and gives the passing spaced Knife example. It is user input
guidance, not a new command or changed native restriction. The development
ZIP was subsequently regenerated in place with that tip and current verified
status; patch/source audit passes and generated26-chip ROM bytes are unchanged.

## Follow-up: verified standing entry and spaced Knife command

Terminal result:120000 fields, exit0/timedOutfalse, current26-ROM/stock/
frozen-controller audit passes.47/47 uppercuts activate;35 show40HP loss and
victim-hit tag. The one spaced-standing Knife command at103120 activates
native211h within8 fields and observes the final1HP drop within55 fields.
Native round result103340 verifies attempt25/round1 counters1–0. No completed
Sub match or map advance. The true physical Knife now executes; lack of a
campaign clear is not evidence it failed.

All39776 pre-Sub rows match the previous compact-Knife trial byte-for-byte,
prefix SHA25625932FE2098D118A2EA2005FECA59A40767FA7A7C156F5614FF5D47AA64762DA.
The compiled Kintaro victim throw scripts were separately checked on current
2219:25 typed items/six coordinate adjustments each; runtime remains unproven.
No emulator remains after this completed trial.

Original standing-entry plan:

`stock_wolf_2219_kano_standing_knife` is active hidden/BelowNormal with the
same native ROM/arguments and120000-field bound. The previous failed Knife
trace shows native duck readiness103106, then rising action301h103107..112,
then normal punch101h103115. Releasing Down immediately before the compact
sequence allowed the rise process to consume its Down history. The standard
projectile fixture instead uses three-field Down/neutral/Back/neutral/HP
steps (starts10/16/22), not the compact command's missing neutral gaps.

The new low-health branch releases guard/Down until actual303h, rendered
height>=96 and a non-duck input table, then reproduces3Down/3neutral/3Back/
3neutral/3HP. Reaction/airborne/threat cancellation, health/range gates and
native rules remain unchanged. The evidence inspector distinguishes the
old compact recording from this spaced-standing recipe, verifies every gap
and readiness, and still requires actual211h activation. All9 targeted
Knife/uppercut evidence tests pass. No outcome is claimed before completion.

The full323-test local suite passes. The damage-window completeness field now
requires samples through the end of the SAME context, not merely enough global
frames after a round/continue change; the strengthened context test passes.
This changes evidence interpretation only, not live controller inputs.

## Follow-up: low-health Knife finish

Terminal result:120000 fields, exit0/timedOutfalse; actual current26-ROM,
stock emulator and frozen physical-controller audit passes.47/47 uppercut
requests activate;35 pair with victim-hit tag and40HP loss. One native
Sub-Zero round win is verified at103388, attempt25/round1, counters1–0.
There is no same-attempt completed match and no map advance. Do not combine
rounds across paid continues or claim the campaign cleared.

The single recorded3Down/3Back/4HP sequence starts103113 but does NOT enter
native Knife211h within the following8 observed fields; no HP drop in its
55-field window. Thus the newly earned round cannot be credited to a proven
Knife hit. Inspect actual input-table/action timing before another strategy
change. No native ROM/rules were modified and no emulator remains.

All16 recorded nonlethal and all16 stage cases were separately requalified
against current harness/source pins, without changing frozen recordings or
starting another emulator. Their requalification coordinators exited0.

Original low-health trial plan:

`stock_wolf_2219_kano_knife_finish` is active, hidden/BelowNormal, same native
2219 ROM,120000-field and32-continue bounds. Prior attempt25 had5 player HP
when CPU reached1HP; attempt27 had40. Both recovered at196-pixel separation
and then approached back into pressure (chip/throw) rather than finishing.

The revised physical policy changes only the existing Kano/Sub opt-in branch:
at CPUHP<=5, grounded gap>=120 and own normal readiness, prepare the proven
D,B,HP Knife with actual stance/duck-table readiness, one release field,
3Down/3Back/4HP fields and80-field repeat spacing. Guards cancel on observed
projectile/ice/slide; reaction/airborne state cancels preparation; round reset
clears the latch. Other health/range windows retain the uppercut strategy.

Native JOY strike_blocked compares remaining strength minus blocked damage
and routes to block_is_useless when<=0; bar_reducer subtracts/clamps at0.
Thus a projectile with nonzero blocked damage can be lethal at1HP without
changing rules. The current ordinary projectile qualification measures Knife
22 hit/5 blocked damage. This is a strategy rationale, not proof of a finish.
All319 local tests pass. No source ASM/ROM/AI/health/difficulty/hitbox changes.

The terminal-run inspector now verifies the recorded3Down/3Back/HP command
before each first `knife_punch` field, distinguishes native211h activation
within8 fields from a request, and joins same-attempt/round HP observations
and native round counters. Three new tests reject malformed commands and
treat truncated/no-activation windows correctly; all8 targeted Knife/uppercut
evidence tests pass. The live trial remains on the earlier ladder, so no
Knife finish or Sub win is claimed yet.

## Follow-up: bounded preparation hold

Terminal result:120000 fields, exit0/timedOutfalse; stock/current26-ROM/
frozen-controller audit passes.43 requests all enter native107h within8
fields, with zero incomplete windows.33 additionally have victim503h and
exact40HP drop within55 fields, same attempt/map/round. Body height68 and
matching nonzero native duck input pointers are recorded at the requests.
No native Sub round/match win occurred across26 rounds. Best CPU minima:
1HP on attempt25/round1 and attempt27/round1;41HP on attempt20/round1 and
attempt21/round2. These are minima, not wins or combined progress across
continues. The actual diagnostic SHA256 is
`3221BC3A5B61C5265543AF7431A70BDB3C4DC0C47056E7C78F733597DBFABA48`.
No emulator remains. Next analysis should inspect the two1HP finishing
windows, not assume the newly proven uppercuts failed to activate.

The inspector now joins observed damage/hit tags within the same native
attempt/map/round; a fifth unit test prevents counting another round or
paid continue's HP as damage from this request. All five evidence tests pass.

Original follow-up plan:

`stock_wolf_2219_kano_uppercut_hold` is active with the same arguments/native
ROM as the terminal trial below and a newly frozen controller. It preserves
an already-started preparation through grounded enemy attack flags for at
most24 fields, instead of discarding it immediately at attack entry. Own
normal readiness, distance<=84, grounded target and projectile/ice/slide
guards remain. Actual duck-height and duck-button-table equality still gate
the HP pulse. Such requests are explicitly tagged `uppercut_counter` when
the enemy attack flag is set, not mislabelled neutral requests.

Body height and actual/expected button-table pointers are now recorded in
the physical-input CSV; the inspector verifies these rather than assuming
readiness from source alone. Four evidence tests pass, including mismatched
readiness and explicit neutral-versus-counter separation. No native game
rules or difficulty/AI/health/positions changed. No outcome is claimed yet.

## Terminal result

The trial completed120000 fields normally (exit0/timedOutfalse); current26
ROM/stock/frozen physical-controller campaign audit passes. The diagnostic
records zero HP requests, zero uppercut activations and no native Sub-Zero
round or match win.3030 approach fields,15848 guard fields and306 preparation
fields were recorded. Contiguous preparation durations/counts:1/3,2/38,3/10,
4/28,5/17. No window exceeded5 fields; the policy repeatedly returned to
guard before observing duck readiness. This is an input-opportunity limitation,
not a failed requested native uppercut. Do not report a gameplay fix or win.

All16 ordinary special/side cells were separately requalified against current
harness/source pins without rerunning emulation or altering frozen recordings.
No emulator remains after this trial. Further physical strategy should address
the readiness-window reset, not relax native range/AI or call requests hits.

## Original trial plan

`stock_wolf_2219_kano_neutral_uppercut` is active hidden/BelowNormal,
120000-field bound and existing32-paid-continue limit. It uses the previous
normal-throw route arguments plus explicit opt-in
`--campaign-kano-sub-neutral-uppercut`. No win is claimed yet.

Motivation: the earlier throw trial reached only71 ready-state separation,
outside the native64 player throw range, and issued no throws. Native CPU
throw-entry distances70..80 make further grounded approach a pressure race.
This trial changes physical input strategy, not native ranges/AI/damage.

Only the existing Kano17/Sub8 normal-throw branch is overridden. Projectile,
ice and slide threats retain crouch-block. Within84 pixels against a grounded,
standing, not-busy opponent, release Block/Away and request Down. After at
least4 preparation fields, actual rendered duck height and native duck-button
table identity are required before a3-field Down+HP pulse; cooldown60. Far
safe approach stops at100 instead of trying to enter throw distance. Other
windows guard. `sub_neutral_uppercut.csv` records observed states and physical
HP requests. Requests alone do not prove activation, damage or a match win.

All314 local tests pass. The native ASM/ROM, stock MAME, difficulty, health,
AI, positions, hitboxes and results are unchanged. Source pins for verifiers
that include the modified wrapper will require normal evidence refresh;
frozen past controllers/traces were not altered. This is not a port release.

`inspect_sub_neutral_uppercut.py` is ready for the terminal run: it first
requires the actual stock/current26-ROM campaign audit, validates physical
request gates and cooldown, joins each request to the following8 dense native
action fields, and derives round/match wins using the native same-attempt
counters. Three tests verify request-vs-activation, incomplete-window unknown,
and invalid-request rejection. They pass. No diagnostic or Sub win is claimed
while the emulator is still on the earlier ladder.
