# Current native CPU roster observation

Program F65002019A05D47400BD755B95C06546B9ADD104140472A111F1D107C3F6D512,
stock MAME0.289, original native random demo selection. No forced character,
AI/health/difficulty/game-state writes, coins, Starts, or gameplay inputs.
Only startup HP acknowledgement occurs before field3000.

The compiled current CPU reaction records were requalified: both own-ID sparse
tables have valid pointers/zero terminators,4608 signed lookup cases pass,
and the actual helper call is linked. This is table proof, not all AI behavior.

Run580 requested42000 fields but was killed by the harness's60-second wall
limit at34200. It remains explicitly timed-out/incomplete, not a full pass.
The harness now gives --cpu-long the same90-second bound as --campaign-long
and records that bound in execution.json. No game or observer control policy
changed for run581, which completes42000 fields normally.

Both added actors appear naturally on CPU side2. In the sampled observations,
Kano has69 animation shapes,92 opponent-health loss and61 own-health loss
over6 damage-exchange events. Sonya has68 shapes,107 opponent-health loss and
100 own-health loss over11 events. These finite health changes and shapes
do not establish every special, victim interaction, or fatality executed.

First-seen snapshots can retain the preceding biography framebuffer, so those
images are not visual-combat proof. Run582 adds read-only snapshots only after
60 fields of actor presence, positive health on both sides, and an observed
non-full health value. Arena images at31019 (Kano/Cage) and22059
(Sonya/Kung Lao) were visually inspected: both show the correct added actor
and lifebar name in the arena, not a proxy or biography screen.

Runs581/582 both finish42000 fields with exit0, no wall timeout, zero missing
markers, no captured fault and no illegal-opcode recovery. Their entire CSV
traces are byte-identical, SHA256
F6ECC7460D8F8133249337AFD5063DF22DB03902FEE0ED42B65DF0C0048A2112.
The snapshot changes therefore do not change the observed gameplay trace.
All26 ROM chips are requalified against582.42 source/tooling tests pass.

Still unproven: every CPU special/finisher, every victim/interruption case,
actual later ladder and secret/boss transitions, both full earned campaigns,
endings/cast/credits, remaining audio and final release acceptance. These are
attract-mode observations, not a full-port or campaign completion claim.

## Health-fill filter correction and finite native CPU action tags

The previous positive-health filter included39 initial health-bar-fill
samples per actor. The non-full-health screenshot trigger also permits
health-bar fill, not just damage; those images prove the arena/own sprite
and name are rendered, not that damage had already occurred at that instant.
The corrected report requires observing both health bars at161 within the
same contiguous identity context before counting post-fill observations.
Gaps/context changes reset that gate. Three regression tests cover fill,
gaps and identity changes. No raw CSV, screenshot or ROM was altered.

For582 the corrected post-fill counts are347 per actor, with67 Kano/64
Sonya shapes (previously69/68 including fill). Full-health observations begin
31038/22078 respectively. Measured damage/exchange totals remain unchanged:
Kano92 outgoing/61 incoming in6 sampled exchange events; Sonya107/100 in11.
Post-fill action tags include Kano Ball020b (6 samples), Knife0211 (13)
and Sonya Ring0212 (22). These are native CPU-tag observations, not hit
counts, every special's execution or a direct dispatch-helper PC trace.

The report now pins its evidence/filter source, verifies actual26 current
ROM chips including sound/original graphics and checks stock MAME plus
read-only guest access. Full CPU gameplay/all-special/boss/campaign and
release qualifications remain false. This correction narrows prior claims;
it does not modify gameplay or infer full acceptance from the sampled tags.
