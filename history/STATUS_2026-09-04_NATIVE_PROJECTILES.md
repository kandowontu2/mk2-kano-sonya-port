# MK2 Kano/Sonya — native projectile assets and command-table repair (v39)

Historical milestone. The installed build is now v40; see `STATUS_2026-09-04_NATIVE_COMMANDS.md` for current hashes and 24 final cases. That audit found and removed a remaining P1 **table-read alias** (even though canonical IDs were intact here), removed shortcut injection and implemented native knife/ring commands. The v39 claim of explicit table entries below must not be taken as proof that the old CPU always consumed those entries.

This is another verified milestone, **not completion of the full natural-roster goal**. Selection/ladder integration from v38 remains intact. Independent special semantics, final native commands, finishers, audio, alternate outfits and full progression remain unfinished.

## Installed build

- Active workspace: `C:\Users\kando\Documents\Codex\2026-08-29\i-ha\work\mk2port`.
- Executable: `mame-mkp/mkport.exe`, SHA-256 `AE64503FC4CBFBB228376540858EA2EE701EA6208DDB18F04AD419001518C74B`.
- Installed payload: `roms_v22_clean/mk2ks/mk2ks.mdata`, SHA-256 `2F29937E0144FE54E490BB6D6C0BEBB99496CDF551F228C38F975F7EFEED31FF`, CRC `44421fbb`, SHA-1 `55a18f010bc7598de254a060772ca5f38c1c7c47`.
- Combined program/chips unchanged from v35; combined SHA-256 `2444C00C201F849D4242A51D9FE85585C8A7AFCCF3145391F270F80C6F1CA0E8`. UI payload unchanged.
- Both direct ROM verification and the current task's forwarding `PLAY_MK2_KANO_SONYA.cmd -verifyroms` pass.
- A two-second headless boot through that same forwarding CMD, using the installed default ROM path, exits successfully. No emulator processes remain running.
- Build and `git diff --check` pass. This still requires the custom executable, not unmodified MAME.
- Recovery copies of v38 are `regression_v39_native_effects/mkport_v38.exe` and `mk2ks_v38.mdata`. They must be restored together, not mixed with v39.

## Actual changes

Kano's low projectile animation was accidentally mapped to his blade-swipe body. It now maps to detached knife flight frames. Release sparks and impact bursts are excluded from the travelling object. Sonya's release now uses actual donor main animation 36, not crouch animation 4.

Changing those mappings alone still produced malformed effects. `tools/build_native_projectiles.py` now decodes the original Wolf-unit skip-form pixels at build time and emits ordinary full-copy 6-bpp MKII graphics, 18-byte frame descriptors and independent native palettes. Kano uses the 24-color knife palette at donor `FFC96600`; Sonya uses the five-color ring palette at `FFC973C0`. The palette count is a 16-bit word followed by colors including transparent index zero. The unused entries in each native 64-color bank are explicitly zeroed.

All ten knife flight frames and four ring frames are converted. Main-39 and special-1 references in all six animation blocks point at these records; the old high-fireball graphics preservation is removed. Native DMA handles both players, facing direction, palette allocation and cleanup. No host-drawn effect or global-P1 palette was added. The CPU's forced Sonya palette-slot/self-loop escape was deleted, and the old imported-metadata suppression explicitly excludes the converted native-data range.

The retained Block+HP convenience path now requests the standing projectile, rather than the low-fireball spawn height. Normal real-input `F,F+HP` also works for both players. This remains a compatible shared move handler, **not the final independent Kano/Sonya command/move implementation**. Other shortcut states still have incorrect move semantics even when their stability tests pass.

The first both-player projectile test exposed an actual native-command dispatch crash: P2's forward input indexed beyond the 12-playable-character table at `FF8620D0`, jumping into instructions and trapping at `FFA1E800`. Twelve command tables (all callers of shared dispatcher `FF861D70`) now have explicit entries for native IDs 17/18, including release/airborne paths. Existing indices 0..16 are preserved. The new entries currently use compatible existing Liu handlers without substituting canonical/live character IDs. Earlier P1 success did not prove this table safe: adjacent-table data happened to be executable on some inputs.

## Allocations

Native effect payload addresses are relative to the 2-MiB mdata window at `FE800000`:

- Byte `1C0000`: `KFX1` header, pixel source offset/length and destination gfx address.
- Byte `1C0100` / `1C0200`: native knife/ring palettes (`FF600800` / `FF601000`).
- Byte `1C0400..1C0517`: fourteen 20-byte slots containing 18-byte native frame descriptors (`FF602000..FF6028BF`).
- Byte `1C4000..1C6FF7`: 12,280 bytes of native packed pixels, copied once at initialization to gfx byte `1E04000..1E06FF7`. Prior selector/ladder pixels are below `1E04000`.
- Native data at `FF600000+` is excluded from legacy donor-palette CPU handling.

New loaded-program command tables occupy byte `FF180..FF53F` (12 tables at stride 50h). Operands/sources are enumerated in `init_mk2ks()`, after native selector and effect installation. All allocations check unoccupied storage and supported original operands before writing. Prior v38 allocations end at `FF14B`.

## Verification — 16 final emulator cases, 3 asset tests

All final emulator cases ran executable SHA-256 `AE64503F...518C74B` with the installed payload hash above. Inputs are real; diagnostic fighter/health/roster writes remain disabled. Every final case reports `pass=true`, no host exception/fatal error, and no observed game trap or stall.

- `regression_v39_commands_{kano_sonya,sonya_kano}`: both custom players perform direct F,F+HP. Each records eight native projectile-table reads per player, 823 converted-frame reads and 2,337 HUD-visible combat fields. Zero identity errors or selection-art leaks. Both directions and both independent effect palettes are visibly exercised.
- `regression_v39_verified_{kano,sonya}_move{0..4}`: ten cases, 2,215/2,226 combat fields each. Both move-0 cases pass 20 basic-action checks. Both move-1 shortcut cases read 792 native effect words and show the corrected standing projectile. Other move cases certify execution/stability only, not complete correct semantics.
- `regression_v39_verified_{kano,sonya}_lifecycle`: one-player native selection, ladder and recovery. Both retain native IDs throughout 556 checked pre-HUD fields, consume their native ladder entry, and show zero portrait leaks. Kano: 1 recovery, 1 reset, 1,780 combat fields. Sonya: 2 recoveries, 1 reset, 1,776 combat fields. Zero name, ground, position or identity errors.
- `regression_v39_verified_navigation`: ten checks, 1,064 border pixels and 66 number pixels, two blinking colors; zero failures.
- `regression_v39_verified_grid`: 31 real-input directional transitions; correct native canonical/live IDs and full borders, zero failures.
- `python tools/test_native_projectiles.py`: three tests pass. Verifies allocation/header safety, every converted pixel against the independent donor decoder, native palette/index ranges and rejection of occupied storage.

Useful captures:

- `regression_v39_verified_kano_move1/snap/mk2ks/0053.png`: standing knife release, no portrait overlay.
- `regression_v39_commands_kano_sonya/snap/mk2ks/0073.png`: P2 Sonya's pink rings striking Kano.
- `regression_v39_commands_sonya_kano/snap/mk2ks/0073.png`: P2 Kano's spinning knife while Sonya reacts.
- `regression_v39_verified_sonya_lifecycle/snap/mk2ks/0001.png`: native Sonya selection; later ladder/scene captures in the same directory verify teardown.

## Failed/intermediate evidence — do not count as acceptance

- `regression_v39_mapping_*` only changed mappings and still rendered malformed/dark effects.
- `regression_v39_native_*` introduced correct native effects but still used the wrong low-projectile spawn for the shortcut.
- `regression_v39_high_*` used real standing commands; their old observer incorrectly required an unused skin-variant root, so they report false despite no trap. The observer now requires actual converted-frame reads instead. They are not final acceptance runs.
- `regression_v39_projectiles_*` genuinely trapped on P2 input at `FFA1E800`; the twelve command-table extensions fix that. Final reruns are `regression_v39_commands_*`.
- `regression_v39_shortcut_*` preceded the command-table repair and are superseded by `regression_v39_verified_*_move1`.

## Next work

Replace the retained input-injection shortcuts and compatible Liu parser/behavior with independent native Kano/Sonya command records and correct move handlers. Native command dispatch is now mapped: `FF861D70` indexes by the real live ID; high-punch dispatch source `FF8628A0` has Liu handler `FF86ADB0`, which uses command sequence `FF87B0D0` and handler `FF86FB60`. The other eleven sources/operands are in `init_mk2ks()`. Trace the actual command-record format and native common projectile/attack helpers rather than writing IDs or masking failures.

Also still open: move timing/damage/hitboxes and impact/recovery semantics, mirrors' alternate outfits, finishers, announcements/voices, AI roster participation, complete later ladder/ending/continue/reselect/join behavior, and remaining animation mappings. Do not mark the full natural-roster goal complete.
