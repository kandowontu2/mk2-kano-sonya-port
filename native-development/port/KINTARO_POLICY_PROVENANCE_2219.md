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
