# Raiden close-shock victim fix

Physical charged-HP tests 169/170 reproduced the broken original lookup:
32 damage occurred, but Kano left Raiden active for 5,196 observed fields
instead of completing the shock. Sonya also used a malformed victim path.
The native `MOVES.ASM::shocker_lineup` unconditionally indexes a 17-long
`shocker_info` table with the victim's true character ID.

`shocker_alignment_source.py` extends that table with explicit own-ID
entries `2300c0e0` for both characters: own main animation 23, frame zero,
signed relative x/y offsets -64/-32. No original row, victim ID, or body
is replaced. The helper is included in source preparation. Inspection
confirmed that `shocker_lineup` restores Raiden's animation pointer before
`shock_shake`; the victim's finite stumble sequence is posed once, not
walked as an endless shaking script.

Hidden native compilation passed in 25.28 seconds with no window created.
Stock MAME tests 171–174 each completed 9,000 fields, using only physical
controls and read-only observations. Both characters on both player sides
took 32 damage, retained their own bodies, flashed the own frozen palette
for 48 fields, restored their normal palettes, and recovered with Raiden
to stance. Raiden's active shock lasted 99 contiguous fields in each run.
No missing-art marker, illegal-opcode recovery or Lua error was observed.

`qualify_shocker_victims.py` independently checks the compiled 19-long
table (including all unchanged original rows), current ROM lanes and
graphics, emulator/controller pins, identities, damage, palettes and
recovery. `SHOCKER_VICTIM_QUALIFICATION.json` records the limited evidence.
Captures show own bodies lifted in front of Raiden, but full visual lineup,
interruption, blocking, distance and edge-case acceptance remains open.

Source preparation still has zero structural-token differences; this is
not a fresh byte-identical clean compilation. Earlier program-link test
reports, including the spear report, remain historical after this link.
No release ZIP or GitHub release was promoted.
