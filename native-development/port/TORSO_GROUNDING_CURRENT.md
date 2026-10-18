# Current torso-rip evidence and remaining grounding defect

Superseded for the targeted native fix by DETACHED_LEGS_2219_CURRENT.md:
the rebuilt2219 program fixes the own leg-object ground anchors, and12 fresh
Cage/Scorpion/Sub-Zero cases pass. The historical diagnosis below remains the
before-fix evidence. Packaging and full-port acceptance are still unfinished.

Four fresh current26-ROM stock-MAME Cage torso-rip/reselection fixtures
complete normally: stock_wolf_6ae0_torso_{17,18}_p{1,2}. Each earns two physical
KOs, retains own separate upper/lower assets through native completion, then
verifies600 consecutive fresh-combat fields with correct identities, full
initial health, live damage, reset state and77400 hardware-palette comparisons.
297 local tests pass. No native ROM/package changes were made.

The verifier was strengthened from receipt-only program/graphics checks to
actual26-chip archive validation, frozen read-only controller checks, natural
KO/performer identity checks, full source/runtime/capture pins and optional
fresh-match verification. The four-case matrix requires full victim/side
coverage and600 fresh fields. It deliberately retains
lowerOpaqueFootPlacementAccepted=false and fullVisualAcceptance=false.

## Confirmed lower opaque boundary mismatch

Sonya victim-player1 fan_05337.png was individually decoded and inspected.
The native torso-rip legs object is placed at ground-136 in these recordings.
Both own phase6 images have height94, yOffset=-47, and their last nontransparent
row is93. Thus the exclusive opaque lower boundary is:

    objectY + 94 - (-47) = ground - 136 + 141 = ground + 5

The PGM images are assets/torso/{kano,sonya}_6.pgm. This is a real five-world-
pixel geometry mismatch, not a missing body/state marker or a failed native
completion. The existing leg-origin/upper-body checks did not test this opaque
lower boundary; their passing results must not imply corrected foot placement.

## Consumer trace before a fix

MKDEATH has three lower-leg object creation paths: the Goro-family rip,
Scorpion swipe and Cage torso rip. Each creates the actor's torso part6,
copies character/flags, matches animation points and inserts the new object.
The own Sub-Zero shatter branch also selects torso part6 into the victim object.
These consumers use different preexisting anchors. A global image-offset edit
would move all of them and must not be assumed safe.

The next native fix should ground only the actual own leg objects at each
consumer, preserving original-roster paths and shared upper-body image pivots,
then rebuild source/ROM patches and rerun affected cases. No such fix has been
applied or qualified yet. Native code remains6AE0. No emulator/compiler remains
running after these fixtures.
