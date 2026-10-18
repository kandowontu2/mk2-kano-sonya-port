# Native ending artwork preparation

Initial preparation produced four own-character photos for the native ending
renderer. The integration update below supersedes this preparation's unlinked
status. Earned ending runtime and release acceptance remain unverified.

Source photos are decoded from the user-supplied MK3 graphics ROM archive,
using the existing independently pinned original-picture decoder. The original
Kano picture starts at graphics byte 0x103599a, Sonya at 0x1000000. All twenty
donor graphics chip hashes are recorded. These are actual own-character photos,
not another fighter's art or newly synthesized pixels.

Each fighter receives a 124x163 portrait for the left-hand text page and a
280x119 wide image for the upper half of a second text page. Nearest-neighbour
crop/scale layout reproduces the existing native ending reference. Four fixed
reference hashes and visual inspection confirm the selected pictures.

build_ending_art.py emits generated_ending/KSENDART.ASM with separately named
image records and 256-word native RGB555 palettes. Pixels use ordinary eight-bit
uncompressed DMA image records, not a new compressed-picture format or emulator
decoder. Palette index zero is reserved; every photo pixel uses indices 1–255,
including nontransparent black. Actual native rendering is still unverified.

The append-only graphics image preserves all 2,305,615 existing bytes and adds
107,064 bytes, producing 2,412,679 bytes—within the existing six-MiB added bank
capacity. No graphics sockets or current playable ROM were replaced. Typed
source SHA256: 9CD0E37479F58E9B1A0A0B6E09D1B942158DDC139B9B41AE58BBF0453375151F.
Packed image SHA256: 191DF736504F6E2FC6D1F300B9A8377C430DFFFDA8326DE75540D323B69EE090.

test_ending_art passes both source-photo/typed-record and append-only tests.
These cannot establish palette allocation, DMA rendering, page transitions,
credits return or earned ending runtime. Next: add the ordinary native object
presentation using gso_dmawnz_ns/insobj2a8 and two text-page descriptors, then
integrate the generated module/graphics chain, independently compile, and test.
Do not promote the development release based on asset preparation alone.

## Native presentation integration and current build

ending_source.py now generates a two-page native object/text loop for each own
identity, preserving the entire original twelve-character ending fallback.
Each page allocates an ordinary gso_dmawnz_ns image object, positions/inserts it,
prints its own text with lm_printf, enables display, waits 12*64 fields, then
clears before the next page. A zero-terminated own table returns to the existing
ending caller after two pages. Cooperative A12 pushp/pullp storage retains the
row cursor and coordinates across calls/sleeps; no SP save spans a sleep.

KSENDART is now an explicit source module, PBUILD assembler target and final
link input. current_graphics extends the previous append-only chain with the
four photos and emitted stock socket bytes. Source staging changed only
UNZIP.ASM, KSENDART.ASM and the linker command; 505 unrelated staged files were
preserved. Existing proprietary originals are still provided as transformations,
not redistributed wholesale in a source bundle.

Working hidden compile: exit0, no window, 27.01 seconds. Independent clean
compile: exit0, no window, 91.57 seconds. Only 134 hash-verified old generated
outputs were removed (2,913,411 bytes); sources and rebuild inputs were retained.
Clean build freshly compiles 130 objects and all four program parts match the
working build byte-for-byte. Current interleaved program SHA256:
8769E42CDA4C9202C6C7301AAB07342399F997D3ABF40805ACF24398118A46C8.

qualify_ending_link.py verifies actual ROM pointers, sizes, eight-bit DMA
controls, all palette words and both own page rows/terminators. The regenerated
ending-source audit and 20 source/coordinate/CPU/boss/round/IPS tests pass.
A fresh independent append-stage art rebuild reproduces the ASM, packed bytes
and four PNGs exactly; temporary outputs are removed afterward.

Stock-MAME run 544 is a normal physical Sonya Friendship followed by selection
and a new fight, not an ending shortcut. It verifies all 26 actual current ROMs,
true identities, native completion and 600 live combat fields, 78,000 hardware
palette color comparisons and retired dance/completion contexts. It does NOT
render either ending. The generated ENDING_ART.json retains its original
preparation-time linked/runtime flags; ENDING_LINK_QUALIFICATION.json is the
newer linked-byte evidence. No final release or development ZIP was refreshed.

Still required: actual ending picture/text rendering, both page transitions,
native credits return and earned campaign runtime. Link/source/regression
checks must not be substituted for those remaining requirements.
