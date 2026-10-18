# Mileena body-suck: actual own-victim failures

MKDEATH do_body_suck shares dizzy_wait and kiss_reach_out with Kitana.
The new guards protect those two setup lookups, but MKDIE r_body_suck then
reads sucked_in_anis, a12-pointer original-roster table, with true17/18.
It shakes the victim, matches it to Mileena, flips its multipart sprite,
plays the ingestion script at4 fields/frame, then sets native invisibility.
Proper own reaction art and calibrated origins are still required.

MOVES fn2_lo_punch F,B,F+LP activates fatality1, psycho stabbing, not body-suck.
Trials261/262 used that wrong command and are excluded from body-suck proof.
The actual fn2_hk_open checks elapsed l_lk >=080h and close range045h,
then dispatches fatality2 on HK release. The corrected physical controller
charges LK/HK before the natural KO and releases HK during Finish Him.
No input gate, health, AI or guest state was rewritten.

Trials263/264 reach the real body-suck path after two natural KOs. Kano's
trace ends at5540 with one illegal-opcode recovery row; Sonya reaches9000
and completion but uses invalid shape25293b3a. Completion alone is not
compatibility. BODY_SUCK_FAILURE_AUDIT.json pins current source/ROM/gfx,
stock MAME and exact frozen observers/traces. The ROM is unchanged from
the tested Kitana-inflation build; only physical diagnostics changed.

Next inspect native ingestion script/header/palette conventions and own
available reaction assets before authoring missing poses. Preserve original
rows and test original controls, both own actors and mirrored sides. The
shared Mileena attacker setup is not yet accepted. No release promoted.

## Measured native art contract

ingestion_contract.py reads the actual multipart scripts and MKSUCK.TBL
headers without extracting or copying any original character pixels.
INGESTION_NATIVE_CONTRACT.json pins the input hashes, component groups,
union bounds and animation-point offsets for every native reference frame.
Liu uses7 frames; the female-ninja reference uses8. Both terminate with
one zero; mframew uses4 fields/frame after24 fields of native shaking.
The eight-frame reference begins with an83x123 union at[-129,13,-46,136]
relative to the matched actor origin and ends with an18x10 fragment at
[-63,11,-45,21]. These changing origins matter: shrinking artwork around
an unchanged foot anchor would not follow the mouth trajectory.

Two unit tests verify number parsing, composite unions, component counts,
last-fragment geometry and timing. This is a geometry/sequence contract,
not replacement artwork, native integration or runtime acceptance.
Author dedicated own poses along this trajectory next, then check native
flipping, palettes, mouth alignment and completion with physical controls.

Dedicated source artwork now exists under assets/ingestion_draft, with
saved built-in prompts/provenance. generate_ingestion_sources.py produces
sixteen editable own-palette PGM frames under assets/ingestion. All16
alpha128 crop bounds have transparent margins; the indexed preview was
viewed. Unequal explicit atlas rows preserve standing boots and prevent
neighbor contamination. Each own frame fits the native geometry envelope
without copying original character pixels, preserving the mouth-side right
edge and vertical center through adapted origins. Artwork is still unlinked:
native-facing, mouth alignment, palettes and complete runtime sequence are
unqualified. No game code, active ROM or release changed in this asset step.

## First native ingestion integration:265/266

build_ingestion_assets.py encodes all16 editable PGMs as readable typed
KSINART.ASM groups/scripts and appends54,586 packed bytes after the exact
current inflation prefix. All pixels round-trip through the six-bit codec;
eight stock Wolf sockets re-interleave byte-identically. ingestion_source.py
guards IDs17/18 before sucked_in_anis and leaves its12 original rows/path
intact. No proxy character or custom emulator behavior is used.

The live source, preparation generator, explicit module order and PBUILD
now include this module. current_graphics.py and the gameplay harness pin
the new ingestion socket generation. The hidden compile succeeded in19.59
seconds without a window. Current lane hashes are
BF790FA54799DC404526D46A17875D3FECF7AFFC511F328C516B19B328531162
and C9FDD75F91DC53C92F012497C145B2827EC6D1D3FBCBCE590162123484D6F4E5.
Earlier different-link runtime reports are historical, not current gates.

Physical runs265/266 each reach9000 fields after two natural KOs. All eight
own poses are observed, followed by native invisibility and completion;
the earlier illegal recovery/invalid-pointer failures do not recur.
INGESTION_RUNTIME_QUALIFICATION.json validates all16 linked headers and
every packed palette index against the editable sources, current ROM/gfx,
stock emulator, frozen observers, identity and captures. It deliberately
keeps full acceptance false. Viewed phase0/phase2/phase7/disappearance
captures show own bodies moving toward Mileena, but initial vertical
placement/ground clearance needs comparison with an original reaction.
Mirrored cases, original controls and current-link clean rebuild remain.
No release promoted.

## Mirrored reaction and original ingestion controls

Runs267/268 mirror the own victim to physical P1, with Mileena as P2.
Together with265/266 all four runs reach9000 fields, two natural KOs,
all eight own poses, native invisibility and completion, without recovery
or invalid-pointer failures. Mirrored phase2 and disappearance captures
were viewed. INGESTION_RUNTIME_QUALIFICATION.json now pins four cases and
mirroredSidesVerified:true; finalMouthAlignmentAccepted remains false.

Runs269/270 select actual Liu1 and Kitana4 as victims of Mileena. Both
reach9000 fields, two natural KOs,283 native fatality fields and completion.
qualify_ingestion_original_controls.py matches compiled runtime group
component headers to every original MKSUCK.TBL pose: all7 Liu phases and
all8 female-ninja phases occur at4 fields/pose, followed by invisibility.
It also compares six original tables' typed values against the pinned
original ZIP. Viewed first-pose captures show the native victims already
lifted and leaning into Mileena; ordinary fighting floor alignment cannot
be inferred from this special reaction. INGESTION_ORIGINAL_CONTROLS.json
records this representative regression, not all original roster behavior.

The ROM/gfx are unchanged during these diagnostics. Current-link independent
rebuild, final own pose/mouth placement and broader gameplay qualification
remain open. No release promoted.

The current-link clean-rebuild gate has since passed; see
CURRENT_REBUILD_PROOF.md. All four clean program parts, independently
regenerated added graphics and all26 actual runtime chips match byte-for-byte.
Final mouth/pose placement and broader gameplay acceptance remain open.
