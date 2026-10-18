# ROM-side Wolf shadow bank fix

The original MKII shadow walker reads compressed row headers through the CPU,
using graphics bit address plus `02000000h`. Added fighter art lives at12MiB
and above; its resulting CPU addresses began near `08000000h`, outside the
stock Wolf CPU graphics window. Body DMA could render the same art correctly
while the CPU shadow walker read unrelated/unmapped bytes. Kano's black
horizontal lines persisted after thawing, so they were not a freeze-tint issue.

Stock MAME0.289 documents the hardware paths:

- [Wolf CPU map](https://github.com/mamedev/mame/blob/mame0289/src/mame/williams/midwunit.cpp): graphics reads `02000000h..06ffffffh`.
- [Wolf graphics reader and control latch](https://github.com/mamedev/mame/blob/mame0289/src/mame/williams/midtunit_v.cpp): system-control bits8–9 select8MiB CPU graphics banks.

`shadow_bank_source.py` integrates a Wolf-only reader into native MKDISP.ASM.
For each row-header byte it saves A0/A1/A2, selects the graphics bank, reads
the normalized CPU address, restores every original control bit, advances the
original bit cursor by8, and restores the registers. Field0 switches to16 bits
for latch accesses and back to8 bits for the compressed header read. The
expanded loop uses DSJ rather than out-of-range DSJS. The original T-unit read
and short loop remain in the non-Wolf assembly branch. No MAME driver changed.

Build passed hidden in20.73 seconds. Tests158/159 each ran9,000 fields with
physical Sub-Zero ice inputs; both retain true identity, freeze160 fields,
restore palette and return to stance. Captures at fight160 and320 show floor
shadows and no horizontal stripes. Against154/155 with identical controllers,
changed pixels are restricted to the added fighter's shadow area; none above
Y190 changed. Thirty-six translation/control-preservation model cases pass.
`SHADOW_BANK_QUALIFICATION.json` pins capture and source hashes.

The first expanded build failed its short-branch range check. Runs156/157
used the old ROM and are explicitly excluded. Coverage remains limited to
the captured arena/stances and freeze/thaw; other poses, both player sides,
all arenas, and broader gameplay still need qualification.
