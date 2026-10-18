# Native Kano/Sonya source guide

This is a development snapshot, not a completed-game claim. The current
working program is 221919459A4129FFDB37C8A3E9EC7F9AA6210D99AED00A35BC3256842C5E1F5A.
This adds own detached-leg grounding to the prior native ending build. Twelve
current Cage/Scorpion/Sub-Zero cases verify the corrected opaque lower edge.
See `leg_ground_source.py` and `DETACHED_LEGS_2219_CURRENT.md`; the actual ASM
is in the MKDEATH changes in `native_source.patch`. Original IDs return unchanged.
Native static-page ending presentation is included. Sonya's earned full
route, both bosses, two story pages, added cast pair, sampled credits and
attract return have now been verified on current2219 in
`stock_wolf_2219_sonya_campaign`; see `SONYA_ENDING_2219_REVIEW.md`.
That finite run is not all-frame audiovisual acceptance. Kano's boss match
clear and earned ending remain unverified; complete acceptance is unfinished.
The game logic executes on the emulated TMS34010. Stock MAME 0.289 supplies
the existing `mk3` Wolf-unit hardware/socket definition; it does not supply
Kano/Sonya gameplay, replace selected identities or draw their assets.

## Where changes live

Paths below are relative to the development package's `source` directory.

| Area | Read first |
| --- | --- |
| Native engine integration | `native_source.patch`: changes to the original engine, roster tables, selection, reactions, AI, endings and sound dispatch |
| Character normals | `asm/KANOMOV.ASM`, `asm/SONYAMOV.ASM` |
| Move input gates | `asm/KSCMD.ASM` and the patched native command dispatch |
| Knife/Ring and Ball/Square Wave | `asm/KSPROJ.ASM`, `asm/KANOMOV.ASM`, `asm/SONYAMOV.ASM` |
| Blade/Bicycle/Choke/Leg Grab | `asm/KSBLADE.ASM`, `asm/KSBIKE.ASM`, `asm/KSCHOKE.ASM`, `asm/KSLEG.ASM` |
| Own throws and paired reactions | `asm/KSTHROW.ASM`, `asm/KSPAIR.ASM`, `asm/KSREACT.ASM` |
| Own fatalities | `asm/KSFATAL.ASM`, `asm/KSLASER.ASM`, `asm/KSKISS.ASM`, `asm/KSBUBBLE.ASM` |
| Friendship | `asm/KSFRIEND.ASM`; native sound integration and chicken generators |
| Selection navigation | `asm/KSNAV.ASM`; native selector changes in the diff |
| CPU actions | `asm/KSAI.ASM`, `cpu_action_source.py`, patched native drone tables |
| Ladder/endings/cast | `ladder_source.py`, `ending_source.py`, corresponding linked qualifications and explanatory documents |
| Typed artwork/animation data | Remaining `asm/KS*`, `asm/KANO*`, `asm/SONYA*` modules: named palettes, image records, pose lists and animation roots |

Generated `.word`/`.long` image records and animation pointers are ROM data,
not game opcodes hidden in an emulator driver. Read the named ASM routines
for control flow. The native-source diff preserves original eight-bit source
content; do not convert it through a lossy text encoding.

## Rebuild boundaries

The package is not a standalone TI toolchain or a redistribution of the
original game source. The matching user-supplied rebuild source, original
data and TI GSPA/GMAKE/GSPLNK/BIGSREC tools are required. Keep the original
inputs separate. Apply `native_source.patch` to the matching original `src`
tree after CRLF-to-LF normalization without character-set conversion; add
the supplied own ASM modules. `PBUILD.BAT` expects that resulting tree at
DOS `C:\SRCP`, TI tools at `C:\TI`, original data and the original ROM split
recipe. `MK2NEWW.CMD` describes the native link. Do not copy prebuilt objects
and call that a clean source rebuild.

Program, graphics and sound have separate build chains. Program assembly
alone does not regenerate graphics or DCS sound. The package's IPS workflow
reconstructs all26 playable chips from the exact hash-matched input ROMs;
it never patches the ZIP container itself. See `../README_PATCHING.txt`.
Independent local clean-build qualifications demonstrate byte equality,
not standalone portability of every developer script or gameplay completion.

## Tests versus shipped game

Developer Lua observers/controllers are not shipped game logic. They run
ordinary physical inputs and read bounded guest state on stock MAME; they
must not write health, selected identities, AI, difficulty or win state.
Campaign paid continues are logged. A controller losing a match is not by
itself a game bug, and one passing fixture is not all-victim coverage.

Sonya has an earned current2219 stock-MAME full campaign clear in
`stock_wolf_2219_sonya_campaign`, including Kintaro, Kahn2–0, the native
two-win gameover transition and later attract return.786/787 are older evidence.
Named captures show her two story pages and the added cast pair; finite
pixel checks support observed page stability, not every possible frame.
Current136-case normal/proximity contacts and the58-clip/29-chapter-per-actor
move showcases add finite action/damage/recovery and recorded-media evidence.
They do not substitute for campaigns or every-frame audiovisual acceptance.
Still open: Kano's earned boss clear/ending, final audiovisual acceptance,
remaining full-scene audio and final release review.
No full-port acceptance follows from this guide or the patch package.
