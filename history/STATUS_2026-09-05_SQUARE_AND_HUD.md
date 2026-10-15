# MK2 Kano/Sonya — square-wave and lifebar shadows (v41)

Historical milestone: the installed v42 build and current 64-case evidence are documented in `STATUS_2026-09-05_CANNONBALL.md`. Both lifebar shadows and all v41 regression coverage are retained.

This is a verified milestone, not completion of the full natural-roster goal.

## Installed build

- Active project: `C:\Users\kando\Documents\Codex\2026-08-29\i-ha\work\mk2port`.
- `mame-mkp/mkport.exe` SHA-256: `6210AFF61D58C50B6E3D8CC3DBECAD2186DEB244D6483DAC8E43C198830A6F97`.
- Payload and program chips are unchanged from v40. `mk2ks.mdata` SHA-256: `2F29937E0144FE54E490BB6D6C0BEBB99496CDF551F228C38F975F7EFEED31FF`; `mk2ks.ui`: `DBC1881B4696ACD33393D47DCBF626239B91EB6D8DB581003D4774A2F97483EB`.
- The forwarding CMD in the current task folder still launches this executable. Two lifecycle cases ran through that exact CMD; its `-verifyroms` check also passes.
- Build and `git diff --check` pass. No emulator processes remained after acceptance.
- v40 recovery executable: `regression_v41_square/mkport_v40.exe` (SHA-256 `94FA414EAF4778B4E68F8FDD90D852319F80B6038D831AFE94071A07B644933C`).
- This remains a custom-emulator port, not a ROM compatible with unmodified MAME.

## Lifebar name shadows

The user correctly reported that both added names lacked the stock dark shadow. The native HUD builder previously emitted only gold-face pixels. It now emits the stock HUD palette's dark pen 2 to the right and lower-right of the faces. Pen 2 is near-black maroon (`420000`), exactly the existing stock palette color, rather than transparent pen 0. Native palette fades remain in control.

Both 4-bpp name sprites reserve one extra column for the shadow. P2 placement accounts for this width; P1 positioning and the ten-row name height remain unchanged. No host-side drawing or persistent overlay was added.

The observer checks every expected shadow pixel against the rendered screen: Kano has 79 and Sonya 87. Both player sides pass; the one-player CMD tests also compare the custom name alongside stock Sub-Zero. These checks are opt-in with `MK2KS_ASSERT_HUD_SHADOW=1` and enabled in both current command runners.

## Sonya square-wave punch

**Forward, Back + HP** now has Sonya's own native command record, grounded/action-ready gate and action routine. It uses MKII's scheduler, movement, animation, collision, damage and landing primitives. No input injection, Liu-ID substitution or generic CPU character-table alias was restored.

The move rises at 12 pixels per field for eight fields (96 pixels), travels horizontally at ten pixels per field for up to 26 fields, then drops with native gravity into landing recovery. Contact ends the horizontal phase immediately, holds the contact pose for ten fields, and then drops. Damage is 27 on the tested airborne hit. A following native ring command proves return to action-ready after each case.

Important: this is an **anti-air** move. Lowering it to hit ordinary standing targets would not reproduce the original. Original MK3 rev 2.1 was run using real controls and read-only observation in stock MAME 0.289. The first square-wave in `diagnostic_v41_mk3_square_reference4` rises from Y=104 to Y=8 and makes 26 collision checks without damaging the standing target. In `diagnostic_v41_mk3_square_air`, the jumping target loses exactly 27 health, Sonya stops on contact and recovers. Only that first controlled move is the reference; later fixed-facing inputs after crossing are not independent acceptance cases.

The reference script is `mk3_square_reference.lua`; original routine is `FF9DF890`, special-animation index 3, attack descriptor `FFA5A930`. Its three flight composite lists match the port's converted flight lists exactly. The port uses its own descriptor with the donor hitbox/damage and compatible native MKII reaction indices; voices and exhaustive victim/reaction fidelity remain open.

Loaded main-program byte allocations (TMS = `FF800000 + byte*8`):

- `FF8E0`: facing-aware F,B+HP history record.
- `FF900`: parser; HP table entry `FF180 + 18*4` points here.
- `FF940..FFB3F`: Sonya-owned action code.
- `FFB40`: 18-byte native MKII hit descriptor; reserved through `FFB5F`.

## Final verification — 44 emulator cases, 3 asset tests

All listed emulator cases ran the `6210AFF6...830A6F97` build with unchanged payload. No emulated health, position, actor-ID or input-history writes were used. Existing optional diagnostic pinning in the older basic-action harness was explicitly disabled.

- **20 square-wave cases:** `regression_v41_square_{kano,sonya}_{ground,air,block,air_block,far,reversed,expired,wrong_button,airborne,with_block}`. Both Sonya player sides pass. Positive checks require exact ascent/height/fall timing, correct facing velocity, collision-read count, expected damage, contact pause, grounded recovery and a successful subsequent ring action. Negative cases require zero square entries/collision reads, no unexpected damage and later action recovery. Airborne targets take 27 damage even with Block held; standing/blocking/far targets are missed. Each case also checks shadows, display, identity, names, portrait cleanup and 1,243 combat fields without a stall or trap.
- **16 knife/ring cases:** `regression_v41_commands_{kano,sonya}_{native,legacy,chord,reversed,expired,wrong_button,airborne,with_block}`. Both players' valid commands deal damage; all seven negative classes remain rejected. Overall display/shadow/identity/stability assertions pass, not just the command check.
- **2 exact-CMD lifecycle cases:** `regression_v41_cmd_{kano,sonya}_lifecycle`. 556 pre-HUD identity checks, one native ladder entry, two recoveries, one next-round reset, native finish/continue actor release, 1,775/1,776 combat fields; zero leaks, name/shadow/identity/ground errors, stalls or traps. Automatic snapshot view was used; the real display target has no external art.
- **2 basics cases:** `regression_v41_basics_{kano,sonya}`. All 20 actions pass, 2,215/2,226 combat fields, zero roster/identity errors, stalls or traps.
- **2 victory cases:** `regression_v41_win_{kano,sonya}`. Two native wins each, own names/poses, correct lifebar shadows on both sides, 2,336 combat fields without errors.
- **Grid:** `regression_v41_grid`, all 31 directional checks, correct IDs and 1,064 border pixels.
- **Navigation:** `regression_v41_navigation`, ten checks, 1,064 border pixels, 66 centered-number pixels, two blink colors and zero measured background displacement.
- `python tools/test_native_projectiles.py`: three tests pass.

Reproduction: `tools/run_native_square.ps1 -CasePrefix NEW_PREFIX` and `tools/run_native_commands.ps1 -CasePrefix NEW_PREFIX`. Both refuse to overwrite evidence and verify the executable hash before/after each case. The command runner explicitly clears the square-test option to prevent cross-suite contamination.

Inspected images include `regression_v41_square_sonya_ground/snap/mk2ks/0019.png` (both shadowed names), `regression_v41_cmd_sonya_lifecycle/snap/mk2ks/0014.png` (native ladder icon, no selector leftovers), `0016.png` (Sonya versus stock Sub-Zero), and `regression_v41_win_kano/snap/mk2ks/0019.png` (own victory and both names).

## Earlier diagnostics are not acceptance

`diagnostic_v41_square_{kano,sonya}_hit` used an insufficient test that called activation a pass despite health staying 161/161. They are not hit evidence. The strengthened final tests above assert actual damage and recovery. The original MK3 reference first needed the full stock executable (the custom build does not include `mk3`), current notifier subscription retention, and sufficient P2 coins; earlier reference attempts did not exercise a controlled square-wave.

## Remaining full-goal work

Kano's ball/grab and Sonya's other specials, complete move/throw/victim semantics, voices, finishers, mirror alternate outfits, AI participation and all later ladder/ending/reselect/join routes still need implementation and verification. Square-wave crossing/interruption/boss-target behavior and audio need further coverage. Two imported body-palette compatibility hooks remain. See the v40 status for the removed proxy/CPU-table alias and the existing table repairs. Do not equate these 44 cases with completion of every character path.
