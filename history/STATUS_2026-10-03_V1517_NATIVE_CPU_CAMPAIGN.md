# v1517 remains the checked development playtest; full integration is open

Run PLAY_CURRENT_V1517_TEST_BUILD.cmd. No playable game source, executable,
payload, user controls, difficulty, RNG, health or ladder state was changed in
this work. The previous selection, human-combat, Dead Pool floor-shadow and
owned launch-audio checks remain bound by the v1541 checkpoint.

## New actual native CPU evidence

Fresh cold P2 Cage/P1 CPU runs use only ordinary coin/start/select/guard inputs.
The original schedules choose Baraka for boot 601, Sonya for 602/603, and Kano
for 604. No CPU ID, move, position or random choice is supplied by the harness.
Only the boot-604 Kano interleaving below has fresh independent acceptance;
terminal Sonya captures are not silently added to verified coverage.

v1556 independently verifies Kano's first actual choke, its complete 22-step
sequence and 70 held callbacks, four native eight-point squeezes (32 damage),
release/fling, original own ready at frame 1831, and victim ready at 1871. Kano
chooses blade at 1832, before the victim recovers; that attack adds a separate
26 damage through the actual native collision writer. Both physical actors'
full action/body/Main flag ledgers and the victim HP ledger match every callback
through the 240-field window. Native original ready cleanup restores control.

All 119 retained scanouts reconstruct exactly from native DMA/CPU writes,
original compressed graphics plus independently reconstructed current graphics,
actual published ROM composites/cache/FIFO ownership, and native Kano palette.
This is real CPU choke/early-blade/contact/recovery coverage, not universal AI,
all victims, audio, unsampled rendering, artistic approval or full-port proof.

The immutable first-cycle observer still says INCOMPLETE for its narrower
uninterrupted-grab fixture: it counts the early blade damage in its grab total.
The new verifier does NOT rewrite that capture or relabel it COMPLETE. The same
run later contains a genuine separate third-cycle COMPLETE; that is not spliced
into the first-cycle proof. The v1555 failed verifier is retained: it incorrectly
required the entire run to contain no COMPLETE instead of scoping this first
cycle. The v1556 successor scopes the check to the actual observed cycle.
v1557 rejects six in-memory state/identity/health/instruction/handoff corruptions
without changing the actual capture.

## Campaign and CPU timing evidence

The two completed v1550 1200-second Kano P2 boss-policy captures are now
independently verified by v1549/v1551. Both naturally reach Shang and Kintaro,
with 29 own round wins and 11 actual paid-continue losses. Cross-stomp has 270
actual knives and 466 native damage stores; projectile has 386 and 514.
Neither defeats Kintaro or starts/completes an ending. These are bounded native
progression checks, NOT successful towers or proof that boss balance needs a fix.
Earlier v1547 Sonya P1 reaches five stages with actual native leg entries; its
tower is also incomplete.

v1545 verifies 7718 actual original RNG calls across old/current unassisted CPU
captures. At the first differing call, both have the same seed/operand/context,
but actual hardware beam count differs (223 vs 226), producing the different
native rotations/results. This explains the first RNG divergence; it does not
claim that every later AI branch is traced or force the old repeat-grab sequence.

## Still open

Full CPU repertoire/opponents, remaining native move audio/choreography and
P2 square interruption/overlap/KO/round cases; all-arena/all-phase grounding and
floor shadows; remaining victim/finisher consumers; actual completed towers,
both bosses, endings, secrets and cinematic teardown. Final release ZIP and
larger obsolete-build cleanup remain open. No further old builds were removed
in this work. v1517 is a development playtest, not a finished native release.
