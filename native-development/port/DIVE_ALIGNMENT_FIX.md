# Native Raiden flying-tackle victim tables

Before-fix physical tests 175/176 showed 30 damage and eventual recovery,
but both victims disappeared during the drag (field-150 captures). Native
`MKPROP.ASM::dive_hit` unconditionally reads the true victim ID from both
`ochar_dived_poses` and `ochar_dived_adjust`; both tables had only 17 rows.

`dive_alignment_source.py` supplies own-ID entries: frame zero of each
fighter's own main-0F knockdown, and relative x/y -72/0. The original rows
and actual character IDs are unchanged. Source preparation invokes this
helper, and the working ASM includes the same entries. No emulator changes.

Hidden native build passed in 19.8 seconds with no window. Tests 177–180
used physical controls on stock MAME 0.289, each completing 9,000 fields.
Both fighters on both player sides took 30 damage. During the sampled
21-field drag they stayed 72 pixels apart and each travelled 200 pixels.
Own poses remained visible; both actors subsequently returned to stance.
No missing-art, illegal-opcode recovery, guest-memory writes or Lua errors
were observed. Captures 177/178 and mirrored Sonya 180 were inspected.

`qualify_dive_victims.py` pins the compiled 19-row tables, verifies every
original row is unchanged, current program and graphics bytes, stock
emulator/controller hashes, physical true identities, damage, shared
movement, own poses and recovery. Its report is
`DIVE_VICTIM_QUALIFICATION.json`. Precise visual hand lineup, blocking,
interruptions and additional edge cases remain open; this is not full-port
acceptance. Earlier program-link reports are historical after this build.

Source regeneration audit: 242 files, 212 exact matches, 30 textual
differences, zero structural-token differences. A fresh byte-identical
clean program build is still required. No release was promoted.
