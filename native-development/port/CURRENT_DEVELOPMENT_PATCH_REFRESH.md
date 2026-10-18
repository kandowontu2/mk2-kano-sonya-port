# Current development IPS refresh

The existing development ZIP was refreshed in place, not published as a final
release or duplicated into another release archive. The packager initially
refused the stale all-ROM clean-rebuild proof. That gate was retained.

The ending append stage now regenerates from the independently rebuilt clean
morph prefix and original donor ROMs, then compares ASM, packed bytes and all
four previews. Temporary generation output is removed; only required clean
source/packed outputs remain. The rebuilt-ROM qualifier verifies the complete
prior chain plus the ending stage, clean program, clean sound and twelve
unchanged MKII art chips against the actual stock-MAME548 archive: all26 match.

Current development archive: MK2KS_NATIVE_DEVELOPMENT_IPS.zip, 5,548,595 bytes.
SHA256: 24F9919D3E343177499EE99A4BFB865DD3C36672E25A15EED1A961F2EB2C8828.
It contains14 IPS patches,12 original-chip copy operations,59 own ASM modules,
original-source diffs, ending/art generation references, patch instructions,
movelist and build commands. No complete ROM set, custom MAME/driver, host audio
samples or proprietary compiler/source tree is redistributed.

Both independent IPS decoders pass every target chip. The actual user patcher
round-trips the complete26-chip archive to the current program/sound/graphics.
Output archive SHA256: BF5216082B7C2DAE18FE75A91F4C773BB41057C3873693524D7DDA1C43FF7D17.
The existing local launcher points at this same refreshed roundtrip path.

Current game program remains the native cast/ending-enabled link
0F4B6A4EC965E3A3F7522D0B19A9A215533FD768537B2727F437EB935F1C65CD.
Full campaigns/bosses, earned ending/cast/credits runtime, full audio/mix,
broader gameplay acceptance and final release validation remain open. Neither
successful patching nor independent rebuilding proves those gameplay gates.

Run549 validates the current program without faults, but loses to Jax before
the new correctly identified Raiden counter policy can run. Preserve that
scope; do not describe it as a Raiden strategy test or campaign completion.

## Current F650 documentation/source-evidence refresh

The latest development ZIP is5564333 bytes, SHA256
D7CFEBE486052336781FA5851F8E0AC7F80F8203B253F72EA0373068169BBA45.
It adds the source guide and common-table linked evidence, with current
source-checked identity tooling. Native program/sound/graphics bytes remain
unchanged. Both IPS decoders and full26-chip patcher roundtrip pass; the
roundtrip archive SHA256 remains67F9E5539A821E9402C92828A5BF341F1D0DFB7CDA671185A2FE3FD455CD8469.
The previous generated ZIP was hash-validated and replaced, not retained as
an extra archive. No final release was published.

The stale PACKAGE_QUALIFICATION report was regenerated after correcting its
historical52-module/fixed-runtime assumptions. ZIP content hashes, all40
changed original-source diffs (actually applied against original bytes),
and all59 own ASM modules match the current build. Completed stock runs602
and603 have the same26 target chip bytes; their archive containers differ
because they also retain six verified unchanged, unselected clone entries.
The report records that distinction instead of claiming literal patched-ZIP
playback. This finite packaging/source proof does not certify full gameplay,
all runtime paths, completed campaigns, endings/audio or release acceptance.
