# Own-body deep-freeze path (unfinished fatality integration)

Native `MKDEATH.ASM::r_super_freeze` read `frozen_stunned` with a true ID
despite only 12 entries, then clamped any ID above Jax to his ice artwork.
Physical baseline 191 showed Kano becoming Jax's statue. Baseline 192
returned to mode 1 immediately after the Sonya freeze impact, rather than
holding the native frozen state. Neither is acceptable own-character
behavior. Earlier trials 189/190 failed to select Sub-Zero because the
observer used edge-slot navigation; these do not prove freeze behavior.

`superfreeze_source.py` handles IDs17/18 explicitly before both original
paths: dizzy frame zero for the initial reaction and final own body, using
the own frozen palette. It retains the native `super_frozen` sleep/wake
loop, shadow clearing, initial palette flashing and actual ID. Original
roster lookup and ice-art branches are unchanged in source. No proxy ID,
Jax body or custom MAME driver is used for the added fighters.

The native build passed hidden in 21.87 seconds. Current runs 193/194 use
physical controls, win two natural rounds and activate the native deep
freeze. Both completed 9,000 fields; each own victim remains in the native
0616h action for 227 contiguous fields and retains its own first dizzy
pose. The final 100 observed fields have a stable frozen palette. Sonya
no longer resets at impact. Both captures were inspected: this is blue
own-body artwork, NOT yet a finished crystalline ice statue.

`qualify_superfreeze_victims.py` checks current ROM/graphics and stock
emulator pins, read-only observer, two natural KOs, true IDs, own compiled
poses, frozen duration and palette stability. It explicitly does not
qualify the shatter fatality: f_death stays zero during freeze alone.
`SUPERFREEZE_VICTIM_QUALIFICATION.json` preserves those limits.

Next: proper own ice-art treatment, physical shatter follow-up, mirrored
victims, original-character controls and full fatality completion. Native
shatter command is source-defined `scom_sz_db1` + HP at close range after
freeze: forward, down, forward, forward (reverse history in MOVES.ASM).
It routes through `do_shatter_punch`, then `r_shatter_punch`. Follow-up
inspection found a separate direct-indexed `frozen_legs` table there (not
`r_pitched`, which was an incorrect initial inference). See SHATTER_FIX.md
for the subsequent own-body fix and completed physical sequence evidence.

Source reproduction has zero structural-token differences, not a fresh
byte-identical clean-build proof. Older program-link reports are historical.
No release was promoted; full-port acceptance remains open.
