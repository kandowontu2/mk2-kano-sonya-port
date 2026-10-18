# Current-link Ball / Square Wave smoke checks

Runs stock_wolf_game325/326 use the current entry-grounding-corrected ROM
and stock MAME. The strengthened qualify_initial_specials.py checks actual
archive program bytes, all current graphics sockets, frozen controller hash,
read-only observation, missing markers and Lua errors, not just receipt flags.

Kano Ball: 13 activation episodes; the deliberately short initial LK hold
does not activate it. The first valid activation hits and returns to stance.
Sonya Square Wave: 12 activation episodes; the initial grounded-opponent
attempt does not activate it. Every activation begins with the opponent
airborne; the first valid activation hits and returns to stance.
Both runs reach field9000 without missing-animation markers.

These are command/hit/recovery smoke checks, not final per-frame geometry,
damage/timing, blocked/whiff/interruption/audio or all-moves acceptance.
Per-run qualification.json files pin current program, map, controller,
sources and captures. No ROM/game rules were changed by these tests.

Six mirrored entry/return art captures from run324 were also viewed: sampled
Kano/Sonya phase0/phase2 and reverse phase0 have correct facing and no clipping
in those poses. This limited inspection does not accept the entire animation.

## F650 current-program refresh: runs606/607

Both stock-MAME runs exit normally at9000 observed fields on program
F65002019A05D47400BD755B95C06546B9ADD104140472A111F1D107C3F6D512.
The qualifier now uses the shared actual26-chip verifier, including current
native sound and original MKII graphics, and pins that verifier plus itself.
Five local integration tests pass: actual current26-chip acceptance and
in-memory corruption rejection for program, sound, original/added graphics.
The tests do not mutate any ROM files or change gameplay.

Kano Ball P1:13 observed activations, first3856; insufficient initial LK
charge rejected; first valid activation hits and returns to stance. Sonya
Square Wave P2:12 activations, first3762; grounded-opponent initial attempt
rejected; every valid launch has an airborne opponent and the first hits
and recovers. Neither run has missing markers/Lua faults. Native launch
audio, full geometry/timing, all blocked/whiff/interruption cases and broad
all-moves acceptance remain separate. No native source or ROM changed.

## Opposite-side F650 refresh: runs624/626

Kano P2 Ball624 passes13 activations, first3895, short-charge rejection and
first valid hit/recovery. Sonya P1 Square626 passes12 activations, first3801,
grounded-opponent rejection, an airborne opponent at each valid launch and
first valid hit/recovery. Both finish9000 fields normally and verify all26
chips with no missing markers/Lua faults.

Run625 is a failed observer setup, not a game result: special_probe.lua
explicitly rejected mirrored Square before gameplay. The fixture now swaps
owner/victim controls and forward/back directions for that profile while
retaining the same timing and invalid grounded first attempt.626 passes
the unchanged qualifier. No game/ROM change was made. The verifier CLI now
requires explicit run pairs and derives the physical sides from receipts.
See CURRENT_SPECIAL_MATRIX.md for the precise current special/side coverage.
