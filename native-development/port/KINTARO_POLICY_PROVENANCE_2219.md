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
