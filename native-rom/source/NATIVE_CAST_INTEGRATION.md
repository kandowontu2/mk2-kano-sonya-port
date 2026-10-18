# Own native cast pair

ending_source.cast appends Kano17/Sonya18 as the seventh ordinary cast pair,
before the existing zero terminator. The original six pair records and all
following original text bytes remain unchanged. No custom process or emulator
routine is introduced: the existing make_player_obj/take_a_bow/credit renderer
consumes the new row at the usual left/right positions 112/288.

Credits are source-backed: the original donor program contains RICHARD DIVIZIO
as KANO AND KABAL and KERRI HOSKINS as SONYA. audit_donor_cast_credits.py pins
the donor program and exact string offsets. Only Kano's applicable role is
listed in the added MKII cast row; no unrelated Kabal character is added.

Working hidden compile passes in30.60s; independent clean compile passes
in95.31s, both without windows. Fresh clean inputs differ only in MKEND.ASM;
135 hash-checked generated outputs were removed, retaining all sources. All
130 fresh linked objects are present; all four program ROM parts match the
working build byte-for-byte. Current program SHA256:
0F4B6A4EC965E3A3F7522D0B19A9A215533FD768537B2727F437EB935F1C65CD.

qualify_cast_link.py verifies actual seven cast rows, correct own IDs/names,
coordinates/text pointers, terminator, and each own jump root6/victory root41.
qualify_ending_link.py revalidates all ending page/image/palette and cleanup
call records on the same program. The ending generator audit and 23 source,
art, roster, coordinate, round, CPU, boss and IPS tests pass.

Fresh stock-MAME run548 exercises a physical P2 Sonya Friendship followed by
selection and600 fields of fresh live combat. Full26 actual ROMs, own identity,
health/damage/state reset,78,000 hardware palette comparisons and retirement
of observed dance/completion contexts pass. This does not run the cast or
ending, and does not qualify their animation, pixels, timing or credits return.
Earned campaign/ending/credits verification and final release remain open.

The cast review also exposed the historical ID7/Mileena mislabel. Native ID7
is RAIDEN, ID5 is MILEENA; see CAMPAIGN_ID_CORRECTION.md. Raw evidence is kept,
new audits use source-checked names, and bot matchup classes have been corrected.
