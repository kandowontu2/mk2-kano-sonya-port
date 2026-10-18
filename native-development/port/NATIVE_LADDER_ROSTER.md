# Native fourteen-fighter ladder integration

Audit found that all six original MKSEL opponent maps still excluded Kano and
Sonya. Dedicated mini portraits and selectable IDs alone did not satisfy
their official roster integration. This was an implementation gap, not a
campaign-controller timing issue.

`ladder_source.py`, integrated into `prepare_game_candidate.py`, now adds
ft_kano17 and ft_sonya18 before the hidden Smoke rung in every map. Original
fighters retain their relative order; none is replaced or used as a proxy.
Maps contain17 rungs plus the negative terminator. Smoke13 is still skipped
by the native identity-based advance check; Shang14, Kintaro15, Kahn16 and
the terminator remain ordered. Jade's last-regular trigger/return are shifted
to12/14. Two late-regular minimum-difficulty entries are inserted, retaining
all original entries and boss values. No native AI reaction or damage is
weakened to obtain a win.

Native mini frames are51 pixels tall (MKSEL.TBL). Spacing is51 without frame
overlap; bottom camera788 preserves first-rung portrait screenY156. The
coordinate/camera arrays cover all17 rungs. The final peak camera4 and116-pixel
boss step retain original final-boss framing. Visual pan inspection is finite,
not proof of all subsequent ladder transitions or boss positioning.

Only MKSEL.ASM, MAIN.ASM and MKTOAST.ASM were regenerated/staged;507 unrelated
files were preserved.38 source/tooling unit tests pass, including six maps,
original order, difficulty tiers, geometry bounds and secret progression.
Working native compilation succeeded in32.93 seconds, SDL dummy video/audio,
below normal priority,299 window checks, no created window. Interleaved
program SHA256:
F65002019A05D47400BD755B95C06546B9ADD104140472A111F1D107C3F6D512.

Stock-MAME run579's read-only ladder observer records the actual active map:
3,9,11,7,4,1,8,5,2,0,10,17,18,14,6,12,13,-1.
The captured initial pan at4040 visibly renders own Kano and Sonya portraits
in the opponent column. Frame4240 shows the first-rung alignment at camera788.
Both were visually inspected. Normal gameplay then runs with true player
identity17 and zero missing-animation markers, ending at18547 fields on a
Raiden loss. Old-build campaign wins must not be claimed as current-build
reproduction: this changed ladder timing/program and the run only reaches
map3. The wrapper reports no guest writes or custom driver, exit0, no timeout.

## Still required

Broader ladder/secret/boss transition verification, both earned campaigns and
ending/cast/credits verification, remaining audio checks, and refreshed ROM
patch/final-release acceptance. This document is not release approval.

## Independent rebuild and development patch validation

The fresh clean build imported no existing objects and assembled/linked130
objects. All four program parts match the working build byte-for-byte. The
hidden build took102.31 seconds with932 window checks and no created window.
Only135 validated generated outputs (2919050 bytes) were removed beforehand;
all source/rebuild inputs were retained. The full26-chip proof matches the
program, independently rebuilt sound/added graphics, and unchanged original
graphics against stock-MAME run579.

`qualify_ladder_link.py` checks the actual linked ROM bytes, not just source:
six roster maps and terminators,17 camera positions,18 box-coordinate words,
native frame dimensions, both own portrait pointers, all five difficulty
arrays, and actual compiled Jade/final-boss instruction immediates pass.
Ending and cast linked-record checks were rerun for this program as well;
their runtime acceptance remains false.

The development IPS package is refreshed for this candidate, with14 IPS
patches,12 unchanged graphics-copy operations,59 own ASM modules and the
ladder generator/qualification report. Two independent IPS decoders and the
actual patcher's full26-chip archive roundtrip match the tested ROM bytes.
It includes no complete ROMs or custom emulator/driver and is still explicitly
development-only, not a final GitHub release.

## Finite progression-source review

Current MAIN::adv_winner_map increments map_position, reads the next map
word and skips ft_smoke by fighter ID rather than an old literal rung.
MAIN::set_drone_ochar reads map_start+map_position*16 and recognizes the
native-1 sentinel as completion. MAIN::keep_at_minimum uses the same
position index for its difficulty table; the two added entries retain
the original later tiers. MKSEL's extra box movement likewise checks the
previous map word for ft_smoke, while camera/box positions use the expanded
tables. The final movement check uses16, consistent with the current Kahn
rung. No source edit was needed in this review.

Reviewed source SHA256 values:

* MAIN.ASM: EC1A576AE85E511510CB6405616968A56FA34DF4FD8144E7EDA10956A834E28B
* MKSEL.ASM: F0D79B1F7FD2FB804606C48FC2E7F838B39B7B2FC8AD2AB0AAE4AAE9A011C5D2
* MKTOAST.ASM: B8407AA8FE59D75C3B3131381785FB6D6C8EB55DFF1CF28D7C2BB89322DCB3C1

This narrows specific old-length/skip/sentinel source concerns. It does not
prove every caller/indexed load or actual earned later ladder, secret/boss,
ending or credits transitions. Those runtime gates remain unverified.
