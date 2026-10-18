MKII KANO / SONYA - NATIVE ROM PORT

Real native ASM and ROM patches, running on unmodified stock MAME0.289.
No custom driver, proxy character, host samples or complete game ROMs included.
Both characters have continuous full-game clears, own endings and credits.

PATCH AND PLAY
1. Extract the player ZIP to a writable folder, not inside another ZIP.
2. Install Python3.10+ if necessary. Supply your own MKII and MK3 revision2.1
   archives. Internal chip filenames AND SHA256 hashes must match the manifest.
3. Open Command Prompt in this folder and run:
     PATCH.cmd "C:\path\mk2.zip" "C:\path\mk3.zip"
   Or run:
     python patch_native_roms.py --mk2 C:\path\mk2.zip --mk3 C:\path\mk3.zip --output roms/mk3.zip
   Original archives are not modified. Existing output is never overwritten.
4. Double-click PLAY.cmd. Stock MAME is included in the player ZIP.
   Patched-ROM checksum warnings are expected. Do not substitute original ROMs.

FIRST BOOT
A fresh configuration can stop at the native CMOS initialization message.
Press an attack button (tested: P1 High Punch) to acknowledge it. Then insert
coin and press Start normally. This is not a selection softlock. No prefilled
NVRAM or test controller is included. Use MAME's Tab menu for input assignments.
PLAY.cmd ignores unrelated MAME INI files and keeps settings in .\config.

This is MKII game code on stock MAME's existing mk3 Wolf hardware/socket
definition, NOT MK3 gameplay. The extra Wolf graphics space is intentional.
These patches are NOT a drop-in for an original MKII T-unit PCB.
For a renderer fallback, run from this folder:
  mame.exe mk3 -noreadconfig -rompath .\roms -window -video gdi

MOVES AND SOURCE
MOVELIST_NATIVE.txt includes normals, specials, fatalities, other finishers
and Shang Tsung morph commands. Read its input/eligibility notes.
The separate MK2KS_NATIVE_SOURCE_AND_IPS.zip contains59 authored ASM modules,
40 original-source diffs, the14 IPS patches, patcher and rebuild instructions.
Original proprietary source/toolchain/assets are not redistributed. Supply
the inputs documented in source/NATIVE_SOURCE_GUIDE.md when rebuilding.
All authored development/test tools are published at:
https://github.com/kandowontu2/mk2-kano-sonya-port

VERIFICATION AND VIDEOS
RELEASE_EVIDENCE.json records finite test scopes and the tested media hashes.
Both full campaign videos and both complete move/finisher/morph demonstrations
are separate optional downloads, not duplicated inside this player ZIP.
Finite testing is not a guarantee of every possible input/arena/interaction.
The per-patcher fullPortVerified:false field means byte verification does not
itself certify gameplay. Release tests and their scopes are recorded separately.

MAME LICENSES AND SOURCE
The player includes the unchanged official Windows x64 MAME0.289 binary,
COPYING, its legal notices and font. Corresponding official MAME source is
the separate mame0289s.exe release asset (source archive, not needed to play).
SHA256:6243EAC3A80DF6BE602BF0AF7889305691737BC26C2DED1433EC11B7C6A3C7B9
https://github.com/mamedev/mame/releases/tag/mame0289
Keep the applicable notices and corresponding source available when sharing.
