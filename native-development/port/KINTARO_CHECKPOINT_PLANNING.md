# Stock-MAME checkpoint planning (not campaign acceptance)

Purpose: avoid repeatedly running the earned human ladder while developing
boss input policies. Only stock MAME's scheduled save-state API is used;
no game code, health, positions, AI, difficulty, RNG or win counters are
edited. The initial helper only SAVES, never loads a checkpoint. It waits
for physically earned Kano/Kintaro intro state7/map15/selected IDs17 and12,
records the native HP, requests an absolute local state file, checks that
the scheduled operation produced a nontrivial file and exits after four or
more fields. A saved checkpoint alone is not proof that loading works or
that any round/match was won.

Official API: https://docs.mamedev.org/luascript/ref-core.html documents
machine:save and machine:load as scheduled operations. The helper checks
the stock hardware's supports_save property before requesting a save.

Preserved failed launches:

- stock_wolf_2219_kano_earned_kintaro_checkpoint: Lua's200-local top-level
  limit rejected the appended helper before gameplay.
- stock_wolf_2219_kano_earned_kintaro_checkpoint_v2: helper locals were moved
  into a function but a missing statement boundary attempted to call the
  preceding registration result; runtime initialization failed.

The v3 helper uses a semicolon-prefixed isolated function and a fresh run
directory. It is now running hidden/BelowNormal. No save-success claim is
made until the terminal receipt, exact ROM/controller identity, physically
earned route and checkpoint file/hash are verified. The existing acceptance
fixtures remain unchanged. Any future loaded-state trial must be explicitly
marked planning-only and excluded from full campaign/video acceptance.
The final requested campaign video still requires a continuous physical-input
replay from startup with no checkpoint load. Checkpoints can contain game
state/assets and must remain local, not in public Git or player releases.

Terminal v3 result: exit0/no timeout, no Lua/fatal error. Save requested at
129988 and file observed at129992, native intro7/map15/IDs17/12. The
416900-byte local checkpoint has qualified provenance: all14 human matches
were earned normally and64996 sampled campaign rows are byte-for-byte equal
to the original finish13 reference through termination. HP91/0 in the saved
intro is the native previous-fight state, not an edited health refill; the
next round's initialization must be observed after loading before any planning
use. EARNED_CHECKPOINT_QUALIFICATION.json pins state/controller/ROM-run trace
evidence. Saving succeeded; loading remains unverified. No emulator remains.

campaign_continuity.py now rejects explicit machine-load call syntax and
declared loaded-state planning profiles in campaign acceptance. It does not
claim to detect arbitrary obfuscated Lua; qualified controllers remain frozen
and inspectable. Save-only checkpoints may prove their earned prefix, never
a boss clear.474 unit cases pass, including save/load distinction tests.

Load preflight: the first stock_wolf_2219_kano_checkpoint_load_preflight
restored the correct intro but exited after one field. Its absolute
-seconds_to_run30 limit was already behind the checkpoint's saved guest
clock; this was a harness timing error, not a game-state failure. Its trace
and failed gate remain intact. The fresh v2 run uses no absolute guest-time
limit, a1200-field Lua limit and30-second subprocess wall bound. It observes
120 native combat fields with actual IDs17/12 at map15, including native
161/161 HP initialization, without any combat input or RAM/register edit.
PLANNING_LOAD_QUALIFICATION.json pins the state, frozen observer and trace;
exit0/no Lua/fatal errors. Loading is now verified for this finite preflight.
This remains explicitly loaded-state planning and cannot qualify a continuous
campaign or final video. No emulator remains after either preflight.

Controller continuation: stock_wolf_2219_kano_checkpoint_reference restores
only Lua bookkeeping alongside the stock checkpoint; it does not edit guest
RAM/registers. Its terminal run matches15657 sampled native-reference rows
through field161302 against the original continuous finish13 run. All native
CSV fields match, including IDs, HP, positions, actions, shapes, PC, scores,
rounds and attempts. The Lua combat-age counter matches during combat; its
stale noncombat value is intentionally excluded. Thus save/load/controller
timing fidelity is demonstrated for this finite continuation. It reproduces
the same loss, not a new win. PLANNING_REFERENCE_QUALIFICATION.json pins both
traces and verifies the continuous campaign auditor rejects this loaded run.
New execution receipts explicitly mark planningStateLoadUsed.474 unit cases
pass. No emulator remains. The next useful step is short policy experiments
from this verified checkpoint, followed by a no-load full replay if one wins.

Fixed-air timing trials now admit explicit24/26/30-field attack-button ages
in the existing mixed policy (default28 retained). Adaptive/reactive timing
combinations are rejected. Loaded trials pin the checkpoint SHA256 against
its earned-route qualification; no arbitrary state file is admitted.
The24-field trial is terminal:16 lost Kintaro rounds, minimum boss HP80,
zero native round/match wins. PLANNING_BOSS_RESULTS.json checks actual current
26 ROMs, stock executable identity, frozen controller, native score counters
and missing markers while remaining campaignAcceptance=false. The26-field
trial is running sequentially, hidden/BelowNormal.474 unit cases pass.

The26-field trial is now terminal:16 lost rounds, minimum Kintaro HP48,
zero round/match wins. The final declared30-field timing trial is running
from the same verified state. No native game/ROM edits or campaign-clear
claims follow from these timing experiments.

The30-field trial is terminal:16 lost rounds, minimum Kintaro HP36, zero
native round/match wins. All three declared fixed timings24/26/30 are now
tested from the identical earned checkpoint; none improves the original28
policy's one earned round. Each retained execution exits0/not timed out and
passes current26-ROM/stock-emulator/frozen-controller/native-result gates in
the explicitly planning-only qualifier. This rejects the small fixed-air-age
set as a solution, rather than extending failed timings unchanged. No
emulator remains. Native ROM/gameplay bytes were not edited.

Native geometry review finds is_he_close_ground uses028h (40 pixels), while
grounded uses3; flip kick/punch still use shared MOVES routines and mark
act_fk_sd during descent/landing. In the reference first three requests start
at192/175/162 gap and initially deal13/13/8 damage without player HP loss.
Kintaro enters stomp during the third punch sequence. This motivates a
bounded directional experiment rather than another attack-age sweep.

stock_wolf_2219_kano_checkpoint_retreat_hop allows one backward mixpunch jump
when the request gap is<175; the next aerial request is forward, preventing
an unbounded repeated-backward-hop policy. Knife spacing,28-field attack
age,13HP finishing and all game rules remain unchanged. Its first backward
hop at130420 is followed by a forward punch request at130515/gap247, so the
intended wider subsequent approach is actually observed (player HP146 then,
not proof of successful damage avoidance). Terminal at160512 fields, exit0/
no timeout,16 lost rounds, minimum Kintaro HP39, no round/match wins. All50
logged backward requests are mixpunch at gap<175 with direction=away. This
variant also fails to improve the original policy.474 unit cases pass and
no emulator remains. Loaded results stay excluded from campaign acceptance.

Original-spacing finish13 plus existing stomp refresh/momentum was tested
separately as stock_wolf_2219_kano_checkpoint_finish_momentum. Earlier
momentum tests used the other generic-retreat spacing, so this is not a
repeat of that profile. Terminal at160386 fields, exit0/no timeout,16 lost
rounds, minimum Kintaro HP45, zero native round/match wins.17 logged old-air/
ground/new-Up intervals include16 with observed air after Up; this validates
input/airtime behavior, not successful evasion. Combining these escape inputs
with the best spacing still does not improve the original earned-round
policy. No game/ROM changes, no emulator remaining;474 unit cases pass.

Bounded short-input search: stock_wolf_2219_kano_short_search compares seven
ordinary physical-input sequences from the same parent for120 fields each,
then chooses using native health/round counters. It is greedy planning, not
game AI/health/RNG editing. One hidden BelowNormal stock MAME, approximately
201MiB RAM,60-depth/60000-field/180-second bounds. All candidate inputs/results
are retained; only internally named rejected temporary search states are
removed. Two generated states totaling909492 bytes remain, plus the original
earned checkpoint; no older runtime evidence or rebuild input was deleted.

The search terminates at depth37 with native player/cpu counters2-0, CPU HP0,
player HP161. qualify_kintaro_short_search.py independently checks259 candidate
scores, all37 best-branch selections, actual current26 ROMs, stock executable,
frozen controller/checkpoint hashes and terminal counters. The physical route
is preserved in KINTARO_SHORT_ROUTE.json (37 chunks of120 fields). This is
the first promising PLANNING match candidate, not an earned continuous
campaign clear. Continuous startup replay of the exact inputs remains
required; if it differs, reject/diagnose rather than transfer state/results.
475 unit cases pass, including score-priority/bounded-distance tests. No
emulator remains. No native game/ROM bytes were changed.

The no-load startup replay is now active as
stock_wolf_2219_kano_continuous_short_route. It retains the earned human-route
controller and replaces only Kintaro inputs with the37 recorded chunks. The
first native161/161 combat field must be130294 or the replay aborts. Input
phase logic matches the search, including releasing all controls on each
chunk's120th field and advancing route time across noncombat/round transitions.
A source regression test checks the search/replay input bodies match.
No checkpoint helper is appended and no save/load profile is used. The
new qualifier requires37 identical boundary states, an unchanged human prefix
and a same-attempt native two-round Kintaro win. None is claimed before the
runtime is terminal. One hidden BelowNormal emulator is progressing through
the ladder; native game/ROM bytes remain unchanged.

Continuous replay PASSES: stock_wolf_2219_kano_continuous_short_route ends
at149771, exit0/not timed out.65146 pre-Kintaro rows match the earned reference;
all37 route boundary states match the chosen search path. Native Kintaro
results132648/134986 prove2-0 within attempt25, with no state loads/saves.
The unchanged Kahn controller then wins2-0 in attempt26: clear141326/Kano17HP,
attract149771. Both continuous-route and independent full-campaign qualifiers
pass current26-ROM/frozen-controller/identity/native-score/flow gates. The
planning candidate has now been reproduced as a genuine continuous clear;
the original planning runs remain planning-only and are not relabeled.

Kano's full campaign recording is in progress using the exact continuous
profile. It will require identical campaign CSV and native media checks.
No recording/ending-render/final release claim follows before those pass.
