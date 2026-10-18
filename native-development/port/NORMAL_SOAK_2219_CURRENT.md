# Current native normal-combat stress coverage

This is finite two-player stability evidence, not a complete campaign,
special/finisher qualification, or every-frame animation approval. Native
program ROM2219 is unchanged; only physical-input test controllers changed.

`stock_wolf_2219_normal_soak_v4` completed24000 contiguous observed fields,
exit0 without timeout. `NORMAL_SOAK_QUALIFICATION.json` rechecks the stock
emulator hash, frozen controller, actual26 ROM chips, read-only guest accesses,
clean runtime log, native identities and human player states.

- Kano P1 / Sonya P2:14548 controlled combat fields.
- Six fresh full-health matches; five observed native two-win result entries.
- Both native player states are1 (active human) throughout counted combat.
- Selected IDs and actual object IDs remain17/18 throughout counted combat.
- Both fighters take damage through normal physical attacks.
- Zero missing-animation markers and no sampled illegal-opcode recovery.

`stock_wolf_2219_normal_soak_v4_mirror` also completed24000 fields, exit0
without timeout, and passes the same full qualifier:

- Sonya P1 / Kano P2:14506 controlled combat fields.
- Six fresh matches and five native two-win result entries.
- Both native human states and true selected/object IDs18/17 throughout
  counted combat; no missing markers or sampled illegal-opcode recovery.

Combined:48000 total observed fields,29054 controlled combat fields,
12 fresh match entries and10 native two-win result entries. This is normal-
combat stress coverage only. It does not prove specials/fatalities, boss
campaigns, subjective visual quality or unlimited-duration stability.

## Earlier harness attempts, retained as failures

`stock_wolf_2219_normal_soak` was insufficient for fresh two-human-match
coverage: its selector only handled the original starting cursor positions.
The v2 preflight failed before starting MAME because navigation symbols were
referenced before loading the map; its stderr is retained, with no runtime
directory or game evidence.

The completed v3 trace was explicitly rejected. It contained1828 locked
mode2 fields with CPU-controlled Baraka/Raiden instead of the requested human
Kano. The winning human had continued a native single-player ladder before
the loser rejoined; the controller's `locked` flag was not proof of two human
players. V4 reads native `p1_state`/`p2_state`, rejoins inactive players through
coin/start inputs, uses native ROM navigation tables for cursor movement, and
requires both human states plus true selected/object IDs in the qualifier.
No selection IDs, player states, health, difficulty or results are written.
