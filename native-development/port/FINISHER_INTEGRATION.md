# Native finisher work — incomplete

The candidate implements Kano's skeleton extraction in `asm/KSFATAL.ASM` and
Sonya's flame kiss in `asm/KSKISS.ASM`.
Her distinct Death Orb now lives in `asm/KSBUBBLE.ASM`, with typed controls in
`generated_bubble/KSBUANI.ASM`. Its two-sided Kano-victim and Liu-victim tests
plus a broken-Block-hold negative case pass (`qualify_bubble.py`). Active-list
observations verify both its multipart object and dummy process are retired.
Three finite 9000-frame physical-input tests cover both player sides against
Sonya and a Liu victim, including two natural knockouts and native completion.
`qualify_extract.py` records the bounded evidence. This is not acceptance of
all victims, native audio, fresh-match teardown or
the complete port.

Kano's distinct Eye Laser is now implemented in `asm/KSLASER.ASM` with typed
body/beam events in `generated_laser/KSLAANI.ASM`. `qualify_laser.py` verifies
176 fields, own victim reactions, native completion and explicit beam/dummy
process retirement against Sonya on both player sides and against Liu. A fourth
9000-field run rejects Block held through final HK. Exact audio, broader victim
art/timing acceptance, edges/AI and fresh-match cleanup are not yet qualified.
Earlier finisher receipts below are historical after this new full-game link.

Sonya's corrected flame-kiss tests are `stock_wolf_kiss_ground_03`,
`stock_wolf_kiss_mirror_06`, and `stock_wolf_kiss_liu_05`. Each physically wins
two rounds and verifies native completion in 9000 frames. `qualify_kiss.py`
checks all 60 orb fields point-by-point, eight frame descriptors, orb deletion
before the 116-field burn, unchanged victim origin, eleven performer/eight
salute poses and the 231-field native completion. Exact launch audio and mix,
all other victims/edges/AI and fresh-match cleanup are still unqualified.

`generate_finisher_assets.py` reads the supplied original MK3 program/graphics,
checks its program SHA256 and exports named image descriptors, palettes and
composites to `generated_finishers/KSFART.ASM`. It imports 48 composites and 83
frame descriptors needed for Kano's extraction/skeleton, Kano victim poses and
Sonya's burn. `KSFANI.ASM` exports the eleven-pose Sonya kiss performer sequence;
each referenced pose already exists in her ordinary typed art module. Its donor
sequence is checked only through the first terminator: the dispatch span also
contains composite data and is not an animation script that can be copied whole.

The new packed graphics preserve the entire 1328277-byte fighter/UI prefix and
append 154084 bytes. All eight ordinary Wolf sockets round-trip exactly. No
custom region, address interception or emulator patch is needed. Palette/DMA
appearance still requires actual native rendering and visual comparison.

To reproduce the isolated assembly check:

1. Generate into a fresh `generated_finishers` directory using the supplied ROMs.
   The generator refuses to overwrite an existing evidence set.
2. Copy `KSFART.ASM` and `KSFANI.ASM` into the existing `srcp` build directory.
3. Run `start_background_compile.ps1 -Target finish` (never visible DOSBox);
   it uses `dosbox-finish.conf`, `FASM.BAT` and the original
   TI assembler. Inspect `FART.LOG`, `FANI.LOG`, and the fresh `FOK.TXT`/`FFAIL.TXT`.
4. Run `qualify_finisher_assets.py`. Its receipt pins the source, object and log
   files and repeats the compressed-stream/socket/prefix checks.

The original isolated assembly check did not change the gameplay candidate.
The subsequent extraction integration now links KSFART/KSFANI, KSEXANI and
KSFATAL, KSKISS and KSKSANI through `PBUILD.BAT` and the native full-game linker
script. New runs use `generated_kiss` sockets, which preserve the earlier
graphics prefix and append 2910 bytes of original compressed orb pixels.
Older special test ROMs/receipts remain
historical; they do not certify the newly linked binary.

Next required implementation:

- Finish the remaining own native fatality actions and physical commands in ASM, using symbolic
  native setup/fade/takeover/completion calls. Implement both distinct fatalities
  per actor; do not alias two table entries to one action.
- Both native fatality tables now cover IDs17/18. Preserve original entries and
  replace each unfinished native null entry only when its actual distinct action
  is implemented and tested; a null entry is not completed gameplay.
- Broaden skeleton/Eye-Laser/flame-kiss/bubble acceptance to all victims and
  transitions, including exact new audio and timing/balance comparisons,
  stage/facing-aware victim placement, palette changes and owner/victim scheduling.
  No frame origin edits to synthesize flight and no persistent host overlays.
- Translate remaining source-derived performer/effect control sequences into
  named native commands; do not copy donor executable opcodes or callbacks.
- Continue linking all original and new objects together and building ordinary
  ROM chips with the combined graphics sockets. Keep the emulator unchanged.
- Win actual rounds using physical inputs, activate each finisher, verify own
  IDs/art, timings, audio, all victims, both player sides and subsequent match
  cleanup. Compile success and data round-trips are not gameplay acceptance.

Friendships, babalities, stage finishers, Shang morphs and the other full-port
acceptance requirements remain in scope.
