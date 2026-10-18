# Kung Lao vertical split: missing own victim data

Latest: six fresh2219 cases and six cleanup traces now qualify.40 own pose
scenes and eight transition samples were individually reviewed; tested split
placement/continuity and clean late transition are accepted. See
SPLIT_2219_REVIEW.md for exact scope and report pins. No native ROM/art change.

Current note: the missing-data narrative below is historical. Current native
source has dedicated own split components and synchronized separate-half
scripts. Six fresh2219 runs are active as `stock_wolf_2219_split`: four own
roles plus original Liu1/Kitana4 controls. The verifier no longer silently
uses297..302 recordings; explicit roles, all26 actual ROMs, stock emulator,
frozen observer and source/runtime/PNG pins are required. Plan tests pass;
current runtime/visual/cleanup results remain pending. No ROM/art change
was made for this test refresh.

MOVES hhlk3 accepts F,F,F+LK at96..128 pixels. Controller trials293/294
started too close: physical forward motion brought release distance to88,
so they did not activate and prove no victim defect. Trials295/296 back to
180 first, then use two-field forward pulses. Fatality activates at113,
inside the unchanged native gate, after two natural KOs.

Both true own victims enter f_death1 for77 observed fields, then fail.
Kano telemetry stops at5202; Sonya leaves valid selected/health/PC state
and telemetry ends5950, including PCs outside the program ROM range.
Neither reaches native completion. MAME process exit0 is not gameplay
success. LAO_SPLIT_FAILURE_AUDIT.json pins current ROM/gfx, stock emulator,
frozen physical controller, range, identity and traces. No guest state was
forced and no game code was changed for these diagnostics.

MKDEATH split_in_2_tab has17 pointers and no17/18 entries. Own lookups read
the following script's words as animation roots. A correct fix requires
dedicated own split reaction data, not another actor or a clamped index.

Native r_split_in_2 consumes three initial together poses, then a zero.
After the hold it creates a second multipart object from the first main0
stance pose, handling optional ani_ochar_jump roots. It then restores the
primary peel pointer and copies that pointer into A11: the stance script
does NOT drive the second half during peeling. The original sequence uses
the same seven peel poses on both objects, one flipped. The prior claim
that own stance scripts needed a conditional split path was incorrect.
Own stance poses are valid construction inputs and need not be replaced.
Dedicated own split artwork is still missing; explicit separate synchronized
peel scripts can preserve asymmetries such as Kano's one-sided facial plate.

Next inspect complete native scripts, component/palette/animation-origin
contracts and available own sources, then integrate and test both sides,
original controls and late lifecycle. No release promoted.

split_contract.py now extracts all ten native Liu/female-ninja pose unions,
typed component origins and script sentinels without copying original
pixels. SPLIT_NATIVE_CONTRACT.json records three together poses, a zero,
seven peel poses and a second zero; first pose hold64, following together
poses5 fields, transition hold16, synchronized peel poses6 fields. Source
assertions verify the restored-pointer copy, and two unit tests verify both
parts and every component union. Runtime artwork/integration is still open.

A built-in-generated split draft is now saved in assets/split_draft with
prompt/provenance. inspect_split_draft.py validates its RGBA alpha and
identifies all34 bounded components from the20 pose scenes:6 whole frames
and28 separate body halves. Source rectangles and hashes are recorded in
SPLIT_DRAFT_LAYOUT.json without altering the artwork. Review Kano's chest
disk and facial-plate continuity before native conversion. This draft is
not yet packed, linked or runtime accepted; no game ROM changed.

generate_split_sources.py now converts34 editable PGM components under
assets/split. All components use the own native palette, one common scale
per actor and baseline131/132. Native reference bottom trajectories are
adapted relative to that baseline. Primary and secondary peel sources remain
distinct; secondary pixels are reflected into canonical native orientation
so the existing flipped object can display the intended asymmetric half.
Three tests verify hashes/pixel ranges, all34 dimensions, common scales,
initial ground origins, trajectory origins and matching seven-pose halves.

The native-layout preview was viewed. It still needs costume review:
Kano's split chest disk appears duplicated across the halves, and late
facial-plate continuity is not yet accepted. Source/manifest gates remain
costumeContinuityAccepted:false and runtimeVerified:false. Do not link
this draft merely because its indexing and geometry tests pass.

The continuity revision is now assets/split_v2, sourced from
split_draft/split-atlas-v2.png for the fourteen Kano halves only. The twenty
other components are hash-proven byte-identical to the first indexed set.
The revised preview was viewed: chest markings now meet the cut edges as
partial disks. Four source tests pass. Late face-plate display, final
costume acceptance and runtime alignment remain open. No ROM changed.
