# Sonya leg grab — stock-body contact and command fidelity

This is an **unaccepted v43 candidate**, not a completed character port. The installed CMD and portable release ZIP remain on v42. This note supersedes the contact-candidate details in `STATUS_2026-09-05_LEG_CANDIDATE.md`; that file retains the earlier builds' evidence. A subsequent mirror-palette build is documented in `STATUS_2026-09-05_MIRROR_PALETTES.md` and must not inherit these executable-specific counts.

## Exact current build

- Executable: `diagnostic_v43_jump_candidate/mkport_leg_contacts2.exe`, SHA-256 `95759BDF19B42D5A546AFD6E9C8CD56EB2E5BB5CC03C4FBE1AE79508CCA3EDEA`.
- Required payload: `diagnostic_v43_jump_candidate/roms/mk2ks/mk2ks.mdata`, SHA-256 `31B89318C7D9C6A15706063A1A953D80E5F426AF6EC980009B5040626CAE206B`.
- Stock-contact matrix harness: `mk2ks_selector_exit_test.lua`, SHA-256 `60D3F5A4927CB24D9E3983C27B90EC12F4A8B38A1C0506DBF30A6403A7FFC11B`.
- Installed v42 executable remains `413855890FCE3BECAC9B24E11699FAD1CE465ACCBE4B27A93F2DD5819D13A891`, with payload `2F29937E0144FE54E490BB6D6C0BEBB99496CDF551F228C38F975F7EFEED31FF`. Its recovery copy is `diagnostic_v43_leg_candidate/mkport_v42.exe`.

Working C++ now includes the subsequent mirror-palette change, not this contact-only executable or installed v42. Continue staging builds separately and restoring the verified installed executable. Do not mix candidate executables with installed payloads or silently inherit acceptance from a different executable hash.

## Actual animation changes

The previous candidate assigned Sonya's victim-origin offsets to every stock body. Different native composite origins made those bodies float too high during the flip. `tools/leg_contact_points.py` now records visually authored waist pivots on each stock character's own original pixels. Per-body offsets place those pivots on the original Kano victim's waist path. These are adaptation measurements, **not original MKII-authored throw coordinates**. Kano and Sonya retain their exact original five composites and offsets.

Female ninjas also need a different pose sequence: their forward-flip list has an extra near-upright lean. The intermediate `mkport_leg_contacts.exe` passed 60 mechanical diagnostics but visibly used that lean instead of the forward bend. The current executable uses native list indices `0,2,3,last` for Kitana/Mileena/Jade, as Shang already required, and recalculates the two affected female pivots. Other stock bodies use `0,1,2,last` after their initial upright lift. No sprite art, actor identity or input state is replaced.

`diagnostic_v43_contact_pivots_final` contains the final gridded original-pixel sheets and selected-composite inventory. Current runtime Kitana captures `regression_v43_contacts_sonya_vs_kitana_near/snap/mk2ks/0035.png` through `0037.png` were reviewed across inversion, rotation and release. Raiden, Shang and Sub-Zero's inversion captures were also reviewed. This does not establish exhaustive corner, interrupt, or alternate-palette fidelity.

## Tests and original input evidence

All 14 current asset tests pass: three projectile tests, three typed leg-coordinate relocation tests, three native jump-phase tests and five independent victim/contact tests. The latter decode original ROM lists, verify the original Kano offsets, require every authored stock pivot to lie on an opaque body pixel, preserve the waist path on both facing directions and match all 60 runtime/C++ stock offsets to the authored data. `git diff --check` passes.

All **172 cases** in the `regression_v43_contacts` matrix completed successfully. The exact expected case list was checked against individual terminal JSON results and logs, not just a directory count. It covers all 12 selectable stock humans from both grabber sides in near/standing-block/duck/duck-block/air modes (120 cases), plus Kano and Sonya victims from both grabber sides in all 13 control modes (52 cases). Explicit `MK2KS_LEG_SIDE` now permits an actual P2 Sonya mirror grabber. Each result records executable, payload and harness hashes; the runner refuses a changed harness or overwritten evidence.

Original unmodified MK3 real-input runs `diagnostic_v43_mk3_command_{block_first,lp_first,down_last}` completed in stock MAME. Down+Block four fields before LP and Down+LP four fields before Block both enter the native leg animation at frame 3902 and deal 35 damage (166 to 131). LP+Block four fields before Down never enters the leg animation and deals no damage. The reference script records exact input times, native animation reads and both live actor IDs.

The corresponding **20 port cases** `regression_v43_input_order_{sonya,kano}_vs_{kano,sonya}_{block_first,lp_first,down_last,block2_first,lp_first_block2}` all passed. Both grabber sides and both custom victims retain exact 46-field choreography, damage and follow-up checks. The redundant MKII Block button also works in either staggered order; Down-last correctly never enters the move. These use updated selector harness SHA-256 `A2334AAD16845D3BA80805E5FA0C0B5297FDB35C35E6B7BCBFB344304D4D209E`.

Another **66 cases** passed on this same contact executable: 20 `regression_v43_contacts_ball`, 20 `regression_v43_contacts_square`, 16 `regression_v43_contacts_commands`, and ten `regression_v43_contacts_core` cases (both basics, jumps, lifecycle, wins, plus grid/navigation). `tools/run_native_roster.ps1` isolates candidate paths, disables both legacy memory-writing diagnostics, protects evidence, and checks executable/payload/harness hashes. Lifecycle tests launch the candidate directly; they are not fresh installed-CMD tests. Total on this contact-only executable: **258 runtime cases**, not evidence for the subsequent mirror executable.

## Still required

- Test release/retrigger, corners, interrupts, KO and excluded bosses. Staggered primary/redundant Block orders now pass for both sides/custom victims.
- Keep whole-roster and existing-special acceptance tied to the eventual final executable before promotion. The contact-only build's full rerun above cannot establish later builds' acceptance.
- Finish the full requested roster integration: remaining moves/grabs and victim semantics, native voices/audio, finishers, mirror palettes, AI and all progression/ending/reselect/join routes. This milestone does not narrow that goal.
