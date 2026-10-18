# Jax arm-rip historical failure and current verification

All four fresh `stock_wolf_2219_arms_{17,18}_p{1,2}` cases now qualify;
coordinator exit 0. Each has two natural KOs,147 native fatality fields,
all five own body phases, all five detached-arm phases/two arm objects,
and native completion without fault recovery. Current actual26 ROMs and
source/runtime/all-PNG pins pass. Report SHA256:
`0A96E627F9B37F0F74C53355DB66EA47B4CFA360C6C9CB47F8E272FA887FF9B5`.

28 captures were individually viewed: five body poses plus first/last
detached-arm pose captures for every victim/side. The tested hand grip,
armless collapse and visible shoulder blood placement are visually accepted.
This does not prove every intermediate blood particle, arbitrary position,
audio, original-roster runtime or post-fatality fresh-match recovery. Machine
qualification keeps its conservative visual gate false; this paragraph records
the separate scoped visual judgment. No ROM/art changes were necessary.
No emulator remains after the batch.

The failure narrative below is historical, not a statement that current ASM
still lacks arm-rip data. Current source includes KSARART and dedicated own
body/detached-arm paths. Fresh 2219 tests were run as
`stock_wolf_2219_arms_{17,18}_p{1,2}`, hidden and BelowNormal, one at a time.
Their results are recorded above. The verifier now requires explicit distinct
current runs, all26 actual ROM chips, true recorded roles, source/runtime/PNG
pins, and full phase/native completion observations. Two new plan tests pass.
Visual grip/blood/origin review is scoped above to the inspected fresh captures.

## Original diagnosis

Current-link stock MAME tests215/216 select Jax11 against true Kano17 or
Sonya18, win two rounds with physical inputs, step into the native69..128
pixel range and press Block four times then LP. Source bcom_jx_db2 confirms
that command; no finisher/health/AI state is forced.

Both actual arm-rip activations crash into illegal-opcode recovery: Kano
frame5213 and Sonya5171. Both had native f_death2 and produced fault dumps.
MAME exits0 because the observer catches recovery and exits; that is NOT a
passing move. Missing-art markers remain zero despite the crashes.
`audit_arm_rip_failures.py` verifies both natural KOs, the actual activation,
early recovery dump, read-only observer and exact current program/gfx/
stock-emulator pins. ARM_RIP_FAILURE_AUDIT.json records failures explicitly.

Known unguarded short data dependencies:

- MKDIE ochar_arm_ripped_ani:16 pointers; used by r_arms_ripped.
- MKDEATH arm_ripped_adjust:16 coordinate pairs; used by that reaction.
- MKDEATH ochar_flyin_arms:12 pointers; used by the detached-arm objects.
- MKBLOOD arm_flow_lineups:16 coordinate pairs.
- MKBLOOD left_gush_lineups:12 coordinate pairs.

Each lacks own IDs17/18. This list is not an exhaustive dataflow proof.
The current authored asset folders contain torso/decap/drain/pit/etc., but
no dedicated arm-rip body and detached-arm set. Normal torso assets must
not be relabeled as an armless victim or replaced with another fighter.

Next implementation needs readable own-body stretched/ripped/falling
sequences, proper own detached-arm images/animation, palette-safe shoulder
wounds, alignment to Jax and both blood emitters. Review get_arm_object/
ani_with_arms, the native multipart formats and r_arms_ripped2 sequencing
before wiring data. Preserve original-character paths rather than filling
reserved rows with guessed proxy art. Then test both physical sides,
completion, edge placement, blood and original-character controls.

No game code was changed in this investigation. The current clean-build
and freeze/shatter regression receipts still match this program link.
No release was promoted; this fatality remains incompatible.
