# Current-link single-player attempts, not completed campaigns

Runs359/360/361 are audited against actual current ROM bytes, all graphics
and sound sockets, original MKII graphics, stock MAME and hash-pinned physical
controllers. Selected/object identities stay correct; no missing markers,
Lua errors or illegal-opcode recovery. Audit now checks observer SHA and
read-only guest-memory access explicitly.

359 Kano defensive-ball: naturally beats Baraka in two rounds, advances to
Reptile, then loses. First Reptile round reaches95 CPU HP; second161.
360 Sonya uppercut: naturally beats Baraka in two rounds, advances to Reptile,
then loses both rounds with no damage dealt to Reptile.
361 Kano retreat-kick controller variant: retains uppercut strategy against
Baraka, then tries defensive away-jump kicks against Reptile. Still loses
with no CPU damage. This variant is observer/input logic only: no game
difficulty, health, AI or move code changed.

These attempts demonstrate entry/advancement into the second CPU matchup,
not ladder/ending completion. A failed controller tactic is not itself a
port defect; original-character comparison and move/contact analysis are
needed before attributing the losses. Do not weaken the CPU or force wins
to obtain a campaign video. Full campaigns/videos remain unfinished.

Original-character control362 uses actual Liu Kang and the same retreat-kick
controller. He also beats Baraka and loses to Reptile, with CPU health161/129
at the two round minima. Identity/ROM/observer checks pass without missing
markers or recovery. This comparison does not prove every own normal hitbox
correct, but it contradicts treating this tactic's loss as a Kano-only defect.

Run370 changes only the physical jump-kick timing to a later press. Kano
again beats Baraka, then damages Reptile to135 HP in each round but loses.
Run371 preserves Sonya's winning Baraka tactic, then alternates forward
movement/block while approaching for Leg Grab. She loses to Reptile without
reaching a Leg Grab action in the trace. That attempt is not evidence of a
failed activated Leg Grab; the previously qualified move was never entered.
Both current-ROM audits retain true identities and show no missing markers,
Lua faults or illegal-opcode recovery. Neither is campaign completion.
Game/AI/health/difficulty source remained unchanged throughout these trials.

## Later current-program evidence (the above runs are historical)

See LIU_KANG_CAMPAIGN_CURRENT.md and SUB_ZERO_CAMPAIGN_CURRENT.md for
Kano's current native match wins through Liu and remaining Sub-Zero losses.
See SONYA_KITANA_CAMPAIGN_CURRENT.md for677: Sonya repeats her natural
Baraka/Reptile/Jax/Raiden match wins and wins one Kitana round with77 HP,
but loses the match1–2. Six native duck-uppercut counter contacts are
request-linked and verified. Earlier prefix equality and actual26-chip
checks pass; no current full campaign, later bosses or earned ending is
certified by these finite improvements.

681 subsequently verifies Sonya's full2–0 Kitana match on the first attempt
after the established Raiden win, using two actual46-field native Leg Grab
holds from established crouch-block. She naturally advances to Liu, then
loses there. See the same Sonya/Kitana document for exact counters, HP,
read-only controller/ROM pins and remaining limitations.
