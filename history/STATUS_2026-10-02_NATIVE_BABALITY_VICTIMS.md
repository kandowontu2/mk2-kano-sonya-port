# Native babality victim fix — not complete finisher/release acceptance

The current test launcher now opens diagnostic_v728_native_babality_victims.
The production launcher and release ZIP are unchanged.
Candidate SHA256: AC94C412BE6AE2B96C51B86796315385DD013A1CA206C9A35128CDE410FD213E.
Payload SHA256: 1367D5A0D42C661CF555F42231A20A650C28E107AB9C80BD821C0BEA7EB4D5EF.
The payload is unchanged; the new executable installs the native table/art fix.

## Defect reproduced before editing

Cold two-player input-only v725 runs genuinely selected Kitana and each victim,
earned two native combat knockouts with kicks only, and entered the original
babality action. Native MKII checks no HP/LP usage in the winning round, not
Block. Kitana's D,D,D command is dispatched by LK, not HK.

The original victim table has only twelve legal fighter rows. Actual true-ID
lookups read 0000002C for Kano17 and 72540000 for Sonya18, from descriptors
after that table. Kano's recorded scene corrupts and watchdog-resets; Sonya's
scene renders arbitrary graphics. Stock Liu Kang reads its valid own baby
pointer and displays normally. Earlier v720-v724 command/setup mistakes and
v729-v731 post-handoff observer assertions are retained as failed diagnostics,
not promoted to clean acceptance.

## Implementation and actual verification

The original victim lookup operand now selects an extended table with the
preexisting lookup words preserved and independent Kano/Sonya entries. Their
single-frame descriptors and 16-bit-count palettes are copied from MK3's actual
native victim-ID table FFA2A5B0. Graphics addresses tag the already imported
original MK3 graphics. No victim ID, native scheduler, finisher choreography,
damage, difficulty, eligibility or gameplay action is replaced.

Complete actual guest ROM dumps differ from v680 by exactly226 bytes, wholly
accounted for by that lookup operand, table, two descriptors and palettes.
Every other guest byte is unchanged, including the accepted Pit stub. This
does not recertify all historical gameplay tests on the new executable.

Eight clean cold v732 runs cover Kano/Sonya victims in both physical slots,
current stock Liu victims in both slots, and old-build stock controls in both
slots. There are no guest writes, cheats, stage fixtures or health assistance.
Actual selection, original HP stores, native gates/command/action, true-ID
victim lookups and new baby construction are checked. The victim Main naturally
hands ownership to the allocated baby object while the original victim keeps
its real ID; the observer follows that handoff instead of asserting human
ownership during the cinematic.

Twelve rendered snapshots match all10,536 nontransparent original baby pixels
with exact MAME xRGB555 expansion. All30/32 native palette words match at the
checked samples. Both babies use the untouched native height-to-floor placement.
Native original actor retirement stores and subsequent baby-object reuse are
observed. Both stock runs match all182 saved frames /18,491,200 display pixels
against the old executable. Twenty-nine in-memory baseline/corruption tests
pass. This is not full DMA/display coverage, every arena/victim pairing or
audio certification.

Evidence: audit_v726_original_baby_reference; audit_v727 historical sources;
v732 eight clean cases; tools/verify_native_babality_victims_v728_v1.py;
tools/test_native_babality_victims_v728_v1.py.

## Remaining full goal

Kano and Sonya still need their own Babality/Friendship performer integration
and remaining finisher/cinematic coverage. Full unassisted towers/boss clears,
broader human/CPU special and interruption/audio checks, whole-scope regression
and matching final production CMD/release ZIP remain required.

Full-port and full-finisher acceptance remain false. No material data deleted.
