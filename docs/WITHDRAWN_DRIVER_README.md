# Withdrawn custom-driver snapshot — historical documentation

This document describes the old implementation, not the current native ROM
port. Its release was withdrawn. Start at the repository README and native-rom/.

Source for the custom MAME integration that adds Kano and Sonya as distinct
MKII roster entries, with their own selection portraits, ladder presentation,
combat, finishers, morphs, voices, shadows, and endings.

This is an unofficial fan project. It is not affiliated with the owners of
Mortal Kombat or MAME. Game ROMs, ripped graphics/audio, generated character
payloads, release binaries, and gameplay recordings are **not included**.

## Start here

- [Change guide](CHANGES.md): what changed and where to read it.
- [Build and asset boundaries](BUILD.md): upstream revision, overlay,
  compiler command, and limitations of the historical asset-building tools.
- [Full movelist](MK2_KANO_SONYA_MOVES.txt).
- [Test methodology](TESTING.md): what the checks establish and what they
  do not establish.
- [Source manifest](../SOURCE_MANIFEST.json): every exported source file's hash,
  upstream revision, and the matched release EXE/payload identifiers.
- [Exact historical driver integration diff](../patches/native-integration.patch).

## Repository layout

| Directory | Contents |
| --- | --- |
| `mame-overlay/` | All 15 exact canonical compile inputs for the released custom emulator, relative to the upstream MAME checkout. |
| `patches/` | Tracked-file changes against the pinned upstream commit. The new picture-codec header is in the overlay, not this tracked-only diff. |
| `tools/` | Retained builders, extractors, analysis, tests, qualifications, capture and packaging scripts, including historical revisions. |
| `development/` | Retained top-level Lua drivers and supporting launch scripts. |
| `controllers/` | Prepared, source-only test controllers. No runtime dumps or generated media. |
| `history/` | Dated technical development notes. Their “current” labels refer to their original checkpoints. |
| `licenses/` | Upstream license texts. |

The repository is a **source snapshot**, not a reconstructed chronological Git
history. Numbered filenames identify development revisions/cases; they are not
a count of separately compiled releases. Historical scripts can depend on old
workspace paths and evidence that is deliberately not published here. Do not
run arbitrary historical scripts as a build recipe.

## Licensing

Existing source-file license headers and copyright notices are retained.
The custom MAME changes retain the licenses of the files they modify, generally
BSD-3-Clause. MAME as a whole is GPL-2.0; see [MAME_COPYING](../MAME_COPYING).
Original support scripts and documentation without another license notice are
provided under [GPL-2.0-only](../licenses/GPL-2.0).

These code licenses do not grant rights to Mortal Kombat ROMs, artwork, audio,
characters, or trademarks. Supply your own game data separately; nothing in this
repository downloads it.
