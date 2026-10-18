# Explicit own-ID blocked flying-kick response

`MKREACT.ASM::b_superkang` originally indexed a 16-word table with any
victim ID. IDs 17/18 read executable instruction words, so their hard/lite
branch was accidental. Corrected physical baseline runs 183/184 showed
Kano remaining at x661 while Sonya moved x661 to x685 under the same kick.
Both took seven chip damage and eventually recovered.

The first probe runs 181/182 did not release the victim's Block input;
these are not valid release/recovery evidence. The observer's per-field
reset now explicitly includes P2 Block. No game fix was inferred from that
controller mistake.

`blocked_flying_source.py` checks actual IDs 17/18 before the original
lookup and selects the native light-block routine, an authored behavior
choice. This uses each fighter's own block animation, four native shake
cycles and no hard-branch pushback. Original IDs still take their original
lookup and branch; the original table is not extended with guessed hidden
character values. Source preparation includes this change.

Hidden compilation passed in 25.25 seconds, no window. Stock MAME tests
185–188 each completed 9,000 fields, covering both characters and physical
player sides. All show the actual flying kick, seven chip damage, own block
poses, no hard-branch pushback and stance recovery after Block is released.
No missing-art, illegal-opcode recovery, guest-memory writes or Lua errors.
`qualify_blocked_flying.py` pins the source dispatch, linked marker, exact
current program/graphics, emulator/controller hashes and physical behavior.
Its report is `BLOCKED_FLYING_QUALIFICATION.json`.

Original-character runtime controls, other block heights, interruptions
and edge cases are not yet verified. Earlier program-link reports remain
historical. Source preparation has zero structural-token differences, not
a fresh byte-identical clean-build proof. No release was promoted.
