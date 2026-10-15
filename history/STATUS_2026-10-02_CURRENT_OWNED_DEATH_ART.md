# Owned death artwork and native floor placement; full port still incomplete

This is the preserved v901 artwork checkpoint. The current experimental build
is v918; see STATUS_2026-10-02_CURRENT_STOCK_FATALITY_PATHS.md for its native
victim-table repairs, current Reptile regression and outstanding artwork.
The build and hashes below describe the original v901 checkpoint.
EXE SHA256: 3B61536489FABDD30C7888149434360B96B8364FECB0C5038E732C1E9EE52DC1.
Payload SHA256: CC4F29043DE71AEEB0820D15E5A449A14073CDFBFA3F58B756751C92073964DF.
Current driver SHA256: E287C4CE155434E9BA512FA5324DD4115977A501F96A0232B6098A7CC0DF000B.
Installed executable, existing CMD launchers and release ZIP are unchanged.

## Actual changes

Custom headless collapse and detached-head artwork is encoded from the
built-in image_gen outputs preserved in art_native_death_v893. These are
custom assets, not original ROM sprites. Complete prompts/review are in
art_native_death_v893/prompts-and-review.json, with the reused Sonya body
prompt linked to the earlier art_native_death_drafts_v875 manifest.

tools/build_native_death_art_v900.py converts immutable PNGs by component
isolation, uniform downsampling within their source-scale groups, existing
owned palette quantization, and native six-bit pixel packing. No painting,
costume editing or runtime host overlay is performed by that codec.

The unused payload area 160000..180000 contains 28 native descriptors and
49,228 aligned packed-pixel bytes. The driver validates/copies descriptors
to program FAA00..FAC30 and pixels to graphics 1EC0000. Seven dedicated
main60 group lists per fighter now point to owned headless bodies; the first
seven main61 words point to owned detached heads. Original sequence control
words, separators, repeats, loop token and self-pointer remain intact.
Stock characters, normal movement descriptors and palette data are unchanged.

The first v894/v896 art candidate copied Liu's varying collapse anchors,
making Kano's prone body clip the bottom edge. v900 instead retains each
added fighter's existing ordinary ground-contact plane: Kano 139, Sonya 140.
Reptile's table positions victims relative to Reptile's physical Y. Their
owned native floor differences require Y=-3 for Kano and Y=-4 for Sonya;
X, animation, pose offset and all original stock rows remain unchanged.

## Current genuine runtime evidence

audit_v904_{kano,sonya}_p{1,2}_native_death_grounding are cold physical-input
two-human games. The unchanged v887 scenario earns two real Reptile wins,
322 native collision damage and two KOs, then enters Back, Back, Down, LP.
Observers do not write HP, actor identity, position, native state or RNG.

All four runs exit0 at field5198. Native action occurs at 3135; head creation
is age129 and original completion remains age187. Actual heads now use
FFFD5460 (Kano) or FFFD5D20 (Sonya), not Liu's FFB4A4B0. All seven headless
body poses feed the actual original FIFO and hardware DMA. There are 1,950
owned body passes plus 104 detached-head passes (2,054 total). Normal palette
assignment remains genuinely owned by the physical victim and separate head.

Every observed physical headless body stays at its own native floor:
floor = stageY - 134 (Kano), or stageY - 135 (Sonya). For every body DMA,
its last pixel row equals stageY + 5 + displayY - cameraY - page - 1.
The ground therefore moves through raster rows 228, 233 and 238 during
MK2's real win camera transition, rather than staying at one screen row.
The actual custom art stops at field3752, well before terminal continuation.

tools/verify_native_death_grounding_v907.py independently passes all cases,
full 1MiB guest equality against the previous v873 plus only 28 descriptors
and the two owned Y words, exact initialized packed graphics, owner/FIFO/DMA
binding, all pose coverage, native health/command/timing/cleanup and real
400x254 screenshots. The 124 current snapshots and all original scenario
input/state/fatality records are byte-identical to the preceding v902 runs;
adding camera instrumentation did not change the game.

audit_v907_owned_death_grounding_checked stores that verification.
audit_v908_owned_death_grounding_units passes 25 baseline/corruption methods,
including proxy identity, health, command, head fallback, missing poses,
foreign ownership, native floor/camera, dimensions, missing FIFO, lingering
art, bad wrap timing and cache overwrite rejection.

Real Kano P1 standing/prone and Sonya P2 prone screenshots were inspected.
The final corpses are fully visible, with no attached head or Liu head.

## Preserved diagnostic failures and scope limits

The v902 checker assumed a constant screen ground row, incorrectly rejecting
the genuine win-camera movement. v905 recorded the camera but initially
omitted the 256-row double-buffer page subtraction. Both failed reports
and unit runs remain preserved. v907 uses the same measured native projection
as the earlier floor proof, including page; no gameplay failure was waived.

Only Reptile's sequence, normal costumes, both true IDs, both physical slots
and this actual Dead Pool presentation are accepted here. Reptile consumes
the first head sprite: it does not exercise all seven rolling-head frames.
Generated head angles, alternate-palette runtime, other stock head-removal
finishers, full rendered-pixel/costume review and other arena/state variants
remain unaccepted. Whole-port and full-native-death-art flags remain false.

## Remaining full goal

Exercise/fix the other stock fatality victim paths and rolling-head frames;
verify alternate costumes, arena/state/cinematic/art/audio variants; complete
genuine towers through Kintaro, Shao Kahn, continues and owned endings; rerun
integrated selection, ladder, names, floor shadows, human/CPU moves and combat
regressions on the final matched build. Then update the actual play CMD and
release ZIP and clean obsolete build data. Earlier v786/v873 proofs remain
historical exact-build evidence, not blanket v901 acceptance. Goal stays active.
