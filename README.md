# Mortal Kombat II — native Kano / Sonya ROM port

The current development implementation is in **[native-rom/](native-rom/README_PATCHING.txt)**.
Gameplay and character data live in compiled ROMs, with readable native ASM
sources and per-chip IPS patches. It runs on unmodified stock MAME 0.289 using
the existing `mk3` Wolf-unit hardware/socket definition. This is MKII game code,
not MK3 gameplay. No custom MAME driver, host samples, identity proxy or
emulator-side gameplay injection is required by this implementation.

**Development snapshot, not a finished release.** Finite current tests cover
both added identities, selection transitions, normal/special moves, finishers,
morphs and fresh-match recovery. Sonya has an earned current-ROM campaign clear.
Kano's earned boss clear/ending and final audiovisual/release acceptance remain
open. Test counts and manifests are not a complete-playability certificate.

## Current source and patch instructions

- [Patching and stock-MAME launch](native-rom/README_PATCHING.txt).
- [Source guide and rebuild boundaries](native-rom/source/NATIVE_SOURCE_GUIDE.md).
- [59 added ASM modules](native-rom/source/asm/).
- [Changes to 40 original engine files](native-rom/source/native_source.patch).
- [Complete written movelist](native-rom/MOVELIST_NATIVE.txt), including
  fatalities, stage finishers, Friendship/Babality and Shang's added morphs.
- [Per-chip patch manifest](native-rom/PATCH_MANIFEST.json) and
  [snapshot file hashes](native-rom/FILES.json).
- [Native validation and reproducible patcher checks](docs/NATIVE_VALIDATION.md).
- [Current native developer/test source](docs/NATIVE_DEVELOPMENT.md), separate
  from the historical custom-driver tools.

Supply your own exact matching MKII/MK3 ROM inputs to the patcher. Original
game source, proprietary TI tools, complete ROMs and emulator binaries are not
included in this native snapshot. Rebuilding program, graphics and sound are
separate chains; read the source guide before attempting a source rebuild.
The snapshot is not a standalone replacement for those original build inputs.

## Historical custom-driver implementation

The older `mame-overlay/`, root `patches/`, `tools/`, `controllers/`,
`development/`, `history/` and root `SOURCE_MANIFEST.json` describe the withdrawn
custom-emulator work. They remain historical material, **not current native
build inputs or instructions**. The old readme is retained at
[docs/WITHDRAWN_DRIVER_README.md](docs/WITHDRAWN_DRIVER_README.md).
Do not compile that overlay to run the native ROM patches.

## Rights and provenance

This is an unofficial fan project, not affiliated with Mortal Kombat or MAME's
owners. Existing source-file licenses and copyright notices remain applicable;
see [licenses/](licenses/) and [MAME_COPYING](MAME_COPYING) for the historical
MAME/support-code licenses. Those licenses do not grant rights to original game
code, ROMs, artwork, audio, characters or trademarks. Do not interpret the
availability of patches or generated ASM data as a blanket license for the
underlying game assets. Nothing here downloads the original game data.
