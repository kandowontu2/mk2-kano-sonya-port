# Current native Kano campaign comparison

Run 566 uses the unchanged current native program and stock MAME, with
physical controls only. `--campaign-kitana-jump` bypasses the generic
uppercut policy for Kitana so the existing jump-grapple strategy actually
runs against her. Kano's previously established Knife strategy for Reptile,
Jax and Raiden is retained. No ROM/AI/difficulty/health changes are made.

Kano naturally defeats Baraka, Reptile, Jax and Raiden, all before spending
a continue. He loses to Kitana on the initial attempt and two ordinary paid
continues. Her six round health minima are 161/161/161/129/97/161. The run
ends normally at field 25,553; no missing-animation marker or illegal-opcode
recovery occurs, and the audit verifies the current complete ROM set and
own identity 17. This gives current-program coverage through four earned
ladder wins, not campaign/ending completion.

Separately, damage-event inspection of Sonya run 565 finds nine damage events
preceded by Raiden action 010e. MAINEQU defines this as jump-up kick (not
uppercut). This supports the strategy explanation for repeated jump-in losses;
it does not prove every gameplay state correct. Remaining work includes later
ladder/bosses, both earned endings/credits, full audio and final release audit.

## Stance-ready Knife comparison

Run 567 restores the guarded-Knife strategy and adds
`--campaign-kitana-ready-knife`: release guard, wait for grounded stance 0303
(bounded to 45 fields), then start Down/Back/HP. It also holds standing
Block+Away below distance120 rather than permanently crouch-blocking there.
The guard loop can be recognized through the observed linked saved wake,
not only an action tag. These are physical controller changes only.

The first four opponents are defeated again. Kitana's four round health minima
are 29/134/73/95 across the initial attempt and one normal paid continue;
no rounds won. The test ends normally at field23,577. Full-ROM/identity and
no-fault audits pass; campaign completion stays false.

The read-only window17640–17940 captures three HP sequences:
17811–17813,17867–17869,17925–17927. Each has latest joystick entries Right8,
Down6 (relative Back is Right at these positions), and native Knife action
0211 appears on each third HP field. There are33 sampled native Knife fields
in the window. This verifies these actual command activations, not every
requested command or successful hit. The source/tooling unit suite passes28
tests. No ROM or native AI change was made.

## Fan-aware guard: current earned Kitana win

Correction to earlier conversational labels: MAINEQU defines action008 as
Fan Throw and009 as Air Fans, not Fan Lift. MKZAP.do_throw_fans spawns fan_proc
using p1p2_proj_pids; Kitana's P2 record is pid_proj2 (0800).

Run568 adds `--campaign-kitana-fan-guard`. A cycle-checked, RAM-bounded,
512-process-limited read-only scan detects that native CPU projectile PID.
During Fan Throw/Air Fans or a live CPU projectile the controller stops
starting Knife commands and holds Block+Away, adding Down at distance>=120.
It cannot interrupt an already executing game move and does not write game
state. No changes to ROM, AI, health, difficulty or driver were made.

Kano naturally defeats the first five opponents before using any continue:
Baraka, Reptile, Jax, Raiden, **Kitana**. Kitana is beaten2–0. Actual native
result rows at18782 and20172 show player round-win counters1 then2, CPU0;
the two rounds finish with Kano19/46 HP and Kitana0 HP. This is stronger
evidence than merely observing map advance.

The campaign then loses to Liu Kang: CPU minima121/161/161/161 over the
initial attempt and one ordinary paid continue. It ends normally at26289
fields. Current complete ROM/own identity/no-fault audit passes. There is
no ending or full-campaign completion claim. The source/tooling suite passes
29 tests. The next campaign work is Liu Kang and Sonya's Raiden matchup.
