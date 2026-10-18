# Current6AE0 finite special fixtures

Program6AE0A069BDFCF4AB2E2F2A1E3B0B7481735AC2654E0036D9331280037BB8BAF9.
All14 stock_wolf_6ae0_special_01..14 runs complete9000 fields normally on
stock MAME with frozen physical-input controllers, all26 current ROM chips,
no missing markers and fresh per-run qualification.json evidence. The
explicit matrix verifies16 distinct move/physical-side cells:

| Move | P1 suffix | P2 suffix |
| --- | --- | --- |
| Kano Knife | 01 | 02 |
| Kano Ball | 03 | 05 |
| Kano Blade | 07 | 11 |
| Kano Choke | 08 | 12 |
| Sonya Ring | 02 | 01 |
| Sonya Square Wave | 06 | 04 |
| Sonya Bicycle | 13 | 09 |
| Sonya Leg Grab | 14 | 10 |

Per-fixture command/rejection/contact/recovery gates remain unchanged.
This does not certify all normals, victims, bosses, arena edges, arbitrary
interruptions, morph interactions or full native audio. Full-port/release
flags remain false. All114 targeted unit tests pass. No game code, damage,
difficulty, AI or custom driver was changed for these regressions.

## Historical F650 fixtures

These entries are historical, not current6AE0 runtime proof. The explicit
completed stock_wolf_6ae0_special refresh is summarized above.

Program SHA256: F65002019A05D47400BD755B95C06546B9ADD104140472A111F1D107C3F6D512.
Each listed run completes9000 fields on stock MAME, uses physical inputs
and read-only guest observation, verifies all26 actual current ROM chips,
and has no missing markers/Lua faults. Run numbers are baseline folder
suffixes (`stock_wolf_gameNNN`); per-run qualification.json is the evidence.

| Special | Player1 run | Player2 run | Defined fixture scope |
| --- | --- | --- | --- |
| Kano Ball | 606 | 624 | Short-charge rejection; valid activation/hit/recovery |
| Kano Knife | 612 | 613 | Wrong direction, own projectile art/ID, hit/block, cleanup |
| Kano Blade Swipe | 610 | 622 | Whiff/hit/block, poses, interruption trail cleanup |
| Kano Choke | 608 | 620 | Block/duck/far gates, paired poses, damage pulses, recovery |
| Sonya Square Wave | 626 | 607 | Grounded-opponent rejection; airborne launch/hit/recovery |
| Sonya Ring | 613 | 612 | Wrong direction, own projectile art/ID, hit/block, cleanup |
| Sonya Bicycle Kick | 623 | 611 | Incomplete command, hit/block, miss, paired geometry/recovery |
| Sonya Leg Grab | 621 | 609 | Chord, standing/low block, range, paired throw/recovery |

This is14 successful run fixtures covering16 move/physical-side cells,
not16 independent runs and not126000 fields of unrestricted human gameplay.
The failed625 attempt stopped before gameplay because the old observer
explicitly rejected mirrored Square.626 uses correctly swapped physical
roles/directions with unchanged timing; it passes unchanged behavior gates.
The observer correction changes no ROM or move rules.

These fixtures do not establish every normal, victim, boss, arena edge,
whiff/interruption, morph interaction, native audio cue or visual frame.
Finisher, campaign, ending/cast/credits and final release gates are separate.
No full-moveset/full-port/release acceptance follows from filling this matrix.
