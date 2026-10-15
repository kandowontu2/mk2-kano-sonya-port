# MK2 Kano/Sonya — native selector and ladder milestone (v38)

Historical milestone: the installed build is now v40. See `STATUS_2026-09-04_NATIVE_COMMANDS.md` for current hashes, native commands, remaining proxy removal and 24 final reruns (including default-view CMD tests). The selector/ladder implementation below is retained.

The reported selector/portrait leakage is fixed in the installed build. The complete character port is **not finished**: independent specials/effects, alternate outfits, audio, finishers, AI and full progression remain open.

## Installed build

- Active workspace: `C:\Users\kando\Documents\Codex\2026-08-29\i-ha\work\mk2port`.
- Executable: `mame-mkp\mkport.exe`.
- SHA-256: `BFB35379EEA1CE8547DD62C1F784C8763AF1A559EFA516D8CEA2222DF3A2380D`.
- Program chips and v36 animation payload are unchanged; native-table changes are applied to the loaded program ROM by `init_mk2ks_native_selector()`.
- Payload SHA-256 remains `52F04600688052C5D3FA8FC1294961A271F03B80AB1C50B8132B72DF296CEB4A`.
- The forwarding `PLAY_MK2_KANO_SONYA.cmd` in the current task folder resolves to this executable. Its `-verifyroms` check passes. Restart any already-running emulator to use the rebuilt executable.
- Build and `git diff --check` pass. This is still a custom-MAME port, not a ROM playable in unmodified MAME.

## Implementation

The virtual selector/input bridge and all host-drawn portraits, stance previews, background copies, cursor masks and ladder replacements have been deleted. The scanline callback no longer draws any added UI pixels. It only passes through native video and observes the existing combat grace period for shortcut commands.

Kano and Sonya are native top-row cells at portrait coordinates `(23,24)` and `(323,24)`. Their 55x70 portraits use the same 63x78 native cursor object as the stock roster: four-pixel edges, blinking native colors and centered player number. Native stance objects use their actual animation and palette tables. No copied backdrop exists to shift.

Native direction/index tables include IDs 17/18. Down from Kano goes to Sub-Zero; down from Sonya goes to Jax. A ROM movement trampoline derives displacement from cell coordinates, including those two diagonal moves. Confirmation, timer expiry, two-player selection, linked portrait cleanup and ladder scrolling are handled by MKII's own processes. The canonical ID is now correct on the selector, through the ladder and into combat; CPU writes that previously committed a different ID at combat setup are gone.

Native 35x45 ladder descriptors use their own palettes and image data. The existing art is indexed/resampled into native packed 7-bpp selector and 6-bpp ladder graphics. Confirmed portraits use dimmed native palette records. Unsupported custom announcement and stock-range CMOS usage-counter slots are explicitly skipped without changing identity.

Private DMA palettes derived from the global P1 selection have also been removed. Native converted fighter palette records now work for both players. Palette and victory callback tables were extended for selection. Two optional uppercut/knockdown callback tables were additionally extended after genuine P2 hit crashes were reproduced.

## Final verification — 32 cases

All final evidence is under `regression_native_css_verified_*`. Every case reports `pass=true`, with no logged host exception/fatal error. Tests use real inputs and no emulated-memory pinning or diagnostic character writes.

- Twelve button confirmations: `{kano,sonya}_{hk,lp,lk,block,block2}` and the two `_lifecycle` cases for HP. All exit selection at field 1114 and reach the HUD at 1547, with 556 checked pre-HUD fields retaining the actual canonical ID, a native ladder-table read and zero portrait leaks. Secondary Block is checked for immediate confirmation, not merely eventual timer expiry.
- Two timer-expiry cases: `{kano,sonya}_timeout`, 1,387 checked pre-HUD fields and 1,178 HUD-visible fields each, zero identity/name/leak errors.
- Recovery and next-round setup in the HP/lifecycle cases: Kano one recovery, Sonya two, one native reset each, zero identity/ground/position errors.
- `grid`: 31 directional checks across both new edges and the stock grid, checking canonical ID, native live stance ID and all 1,064 border pixels. Zero failures.
- `navigation`: ten visual checks; 1,064 border pixels, 66 player-number pixels, two blink colors, animated Sonya pose and zero backdrop shift.
- `{kano_sonya,sonya_kano}_win`: both real custom players take hits; P1 wins two rounds with native KANO WINS / SONYA WINS scripts. Each has 2,336 HUD-visible fields and zero canonical/live identity errors, stalls or traps.
- `{kano,sonya}_mirror` and `stock_sonya`: both-player selection/identity and idle-combat stability pass. These do not certify distinct alternate outfit colors or P2 specials.
- `{kano,sonya}_move0`: 20 basic animation checks each, 2,215/2,226 combat frames, zero errors.
- `{kano,sonya}_move{1..4}`: eight existing shortcut execution paths, 2,215/2,226 combat frames each, zero identity errors/stalls/traps. This verifies execution, **not correct complete move semantics or effect artwork**.
- `reptile_lp`: stock-selection control, zero leakage or stalls.

Screenshots worth inspecting:

- `regression_native_css_verified_sonya_lifecycle/snap/mk2ks/0001.png`: native Sonya selection/number/pose.
- Same directory, `0014.png`: native Sonya ladder icon; selector artwork gone.
- `regression_native_css_verified_kano_sonya_win/snap/mk2ks/0003.png`: native P2 Sonya highlight alongside selected Kano.
- Same directory, `0017.png`: Kano versus Sonya in combat with own names and no selector overlay.
- `{kano_sonya,sonya_kano}_win/snap/mk2ks/0021.png`: own native victory scripts/poses.

## Failures found and resolved during this milestone

- `regression_native_css_accepted_{kano_sonya,sonya_kano}_win` genuinely trapped on the first uppercut: table `FF8D60D0` indexed adjacent executable instructions as a callback. New normal-human entries fix this; `verified_*_win` are the final reruns.
- Earlier `_accepted_*_block2` reached combat only via timeout. The native low-port masks are now 7/70h, and the observer rejects a button confirmation taking 400 or more fields.
- A P2 live pointer is absent for one native next-round construction field, like P1. The observer permits only the bounded mode-6/full-health setup immediately after a real HUD-table read and logs `MK2KS_P2_CONSTRUCTING`. It never changes memory. Earlier `_fixed_*_win` identity failures were this observer issue, not a remaining trap.
- An earlier Sonya LK run logged a Lua teardown access violation after its passing game result. It is not accepted evidence. Observers now explicitly remove/release memory taps while Lua is live; final reruns have no exception logs.
- Native continue-screen shutters deliberately clip the old HUD after releasing the actor. Name-mask checks stop only for the already-verified native release/construction states; the actual gameplay name checks remain strict.

## Remaining work — do not mark the full goal complete

The existing shortcuts still run shared Liu combat routines. Effects need visual repair as well as independent behavior: `regression_native_css_verified_kano_move1/snap/mk2ks/0060.png` shows a body-shaped projectile, and the corresponding Sonya capture has dark ring colors. Both are wrong despite the execution tests passing. The donor sequence and effect-palette handling must be corrected; do not restore the global-P1 private palette to conceal P2 color problems.

Other open work: distinct alternate/mirror palettes, P2-specific special controls, full native command recognition, correct move timing/damage/hitboxes, finishers, unique announcements/voices, AI roster participation, complete later ladder/ending/continue/reselect/join behavior and remaining animation mappings. These were not certified by the 32 selector/stability cases.
