# Separate deep-freeze statue treatment

The first own-body implementation reused the normal frozen/lightning tint,
leaving dark clothing visible. Dedicated statue palettes now map each own
primary palette's luminance into bright cyan-white RGB15:
`(8+23L/31,24+7L/31,31)`, L=(3R+6G+B)/10. Only index0 is transparent;
opaque black clothing becomes cyan instead of remaining dark. All65 indices
and each character's own silhouette stay unchanged. No Jax or other body.

`statue_palettes.py::build` regenerates readable data appended to KSICEPAL.
Fresh `generate_frozen_palettes.py` includes the same block. The one-time
extension verified the old generated/module bytes against the prior
manifest before appending1,400 bytes; no new graphics ROM bank is required.
`superfreeze_source.py` selects these palettes only for the final own statue
and own shattered legs. Initial flashes, ordinary freeze and lightning keep
their original own frozen palettes.

Hidden compile passed23.5 seconds without a window. Stock MAME runs203–206
completed9,000 fields each: two natural KOs, deep freeze and native shatter
completion for each character on each physical side. Qualifiers verify
compiled65-entry data, unchanged ordinary frozen palette bytes, distinct
statue palette transitions, own legs using the same palette, true identity,
no missing-art/illegal recovery and native fatality completion. Reports:
SHATTER_VICTIM_QUALIFICATION.json and STATUE_PALETTE_QUALIFICATION.json.

Captured full statues203/204 were inspected and now read as cyan-white ice
instead of dark blue clothing. This is palette-based surface treatment,
not newly authored crystalline facets; pixel-perfect final-art acceptance
remains false. Original-character controls and ordinary freeze/lightning
runtime regressions on this link remain open. Source regeneration has
zero structural-token differences, not a fresh byte-identical clean build.
Older program-link reports are historical. No release was promoted.
