# Native Kano / Sonya ROM port

Kano and Sonya are native selectable characters with their own identities,
portraits, poses, ladder icons, names, floor shadows, normals, specials and
finishers. Shang Tsung can morph into both. Both have continuous stock-MAME
full-game clears with their own endings and cast/credits.

This replaces the withdrawn custom-driver approach: gameplay is compiled
native ASM in patched ROMs. The bundled MAME0.289 is the unchanged official
Windows x64 executable. The existing `mk3` Wolf hardware definition supplies
the extra graphics capacity; this is MKII gameplay, not MK3, and is not a
T-unit PCB drop-in.

## Downloads

- `MK2KS_NATIVE_WITH_STOCK_MAME.zip`: minimal player bundle, IPS patches,
  patcher, `PATCH.cmd`, `PLAY.cmd`, complete movelist and instructions.
- `MK2KS_NATIVE_SOURCE_AND_IPS.zip`:59 authored ASM modules,40 original-source
  diffs,14 IPS patches, rebuild instructions and patcher. No proprietary
  original source/toolchain or complete ROMs.
- `mame0289s.exe`: corresponding official MAME source archive. Not needed
  to play; supplied separately with the unchanged emulator's licensing notices.
- `MKII_KANO_MOVES.mp4` / `MKII_SONYA_MOVES.mp4`: demonstrations of normals,
  specials, fatalities, Friendship, Babality, stage finishers and Shang morphs.
- `MKII_KANO_CAMPAIGN_NATIVE.mp4` / `MKII_SONYA_CAMPAIGN_NATIVE.mp4`: complete
  earned campaigns, including bosses and ending sequences.
- `RELEASE_QUALIFICATION.json`: finished ZIP hashes and patching checks.

Supply your own MKII and MK3 revision2.1 archives matching the chip hashes
in `PATCH_MANIFEST.json`, and Python3.10+. Extract the player ZIP, run
`PATCH.cmd "C:\path\mk2.zip" "C:\path\mk3.zip"`, then double-click `PLAY.cmd`.
On first boot, acknowledge the native CMOS message with an attack button
(tested: P1 High Punch), then insert coin and start normally.

## Verification scope

Finite native checks cover136 normal contact cells,16 special/side cases,
112 lethal victim/side cases with fresh-match recovery, positive and negative
Friendship/Babality eligibility, stage finishers, transformed moves/finishers,
selection UI, grounding, shadows and clean rebuild equivalence of all26 chips.
Both final ZIPs independently reconstruct the exact tested ROM archive.
`RELEASE_EVIDENCE.json` records the reports and their narrower limitations.
No exhaustive every-input/arena/interrupt or subjective every-frame A/V
perfection claim is made. Interactive Windows renderer windows were not opened
during background-only tests. Both campaign recordings include native audio.

Public authored development/test source is in `native-development/`; canonical
compiled ASM/diffs and patch sources are in `native-rom/source/`. Historical
custom-driver experiments elsewhere in the repository are not used by this
native release. No game ROMs are distributed.
