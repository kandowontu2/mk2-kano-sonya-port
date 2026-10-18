# Native spear alignment

`MKZAP.ASM::lineup_rope_with_him` indexes `spear_adjustments` with the
victim's real character ID. The original 17-word table ended immediately
before executable code. Kano (17) and Sonya (18) therefore used instruction
words as rope offsets: damage and pull-in worked, but the rope disappeared.

`spear_alignment_source.py` adds explicit 124/124 alignment words. The
original 17 entries, actual character IDs and native victim animations are
unchanged. This is assembled game code in the program ROM, not a MAME fix.

Stock MAME 0.289 runs 165–168 each completed 9,000 fields. Physical controls
selected Scorpion and each added fighter on both player sides. Read-only
traces show 8 damage, distance shrinking from 208 to 64, native spear stun
and subsequent stance recovery, with own bodies and identity retained.
The observed hit/stun spans are 111 fields for player-two victims and 110
for player-one victims; the verifier preserves this measured distinction.

All four field-160 screenshots were visually inspected: the horizontal
rope is visible and attaches at the upper-body region on both sides.
This is limited visual evidence, not pixel-perfect acceptance for every
pose, distance, collision edge or interruption.

`qualify_spear_victims.py` verifies the compiled 19-word table, unchanged
original entries, exact current program lanes and added graphics, stock
emulator hash, controller hash/no guest-memory writes, true IDs, native
damage/pull/stun/recovery and no missing-art/illegal-opcode observations.
It records screenshot hashes in `SPEAR_VICTIM_QUALIFICATION.json`.

Source preparation was also re-audited: 242 generated files, 213 exact
matches and 29 textual differences, with zero structural-token differences.
That is not a fresh byte-identical clean-build proof. Earlier program-link
runtime and clean-build reports remain historical; this change does not
make the full port, campaigns or release ready.
