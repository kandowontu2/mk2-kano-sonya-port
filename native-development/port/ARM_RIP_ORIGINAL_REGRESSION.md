# Representative original-character arm-rip controls

No native program or graphics changed in this step. The physical test
runner now supports original victim controls for arm rip, and the read-only
observer additionally logs actual victim object ID/pose/palette/flags.
This is control selection, never a replacement identity for Kano or Sonya.

Stock MAME runs237/238 use original Liu Kang1 on both physical player sides.
Runs239/240 use original Mileena5 on both sides; this also exercises the
existing special arm-palette branch for female ninja2. All use precisely
the current Kano/Sonya port ROMs and current full added graphics.

Each run completed9,000 fields, won two natural Jax rounds and executed
four Block presses plus LP within native range. Each retained the actual
original victim ID, never used an own-fighter victim pose, spent147 fields
in native fatality state2 and reachedffff completion. No missing-art,
illegal recovery, Lua errors, game-memory writes or timeout. Captures239
and238 were visually inspected as representative original bodies/arms.
This is not pixel-by-pixel palette acceptance or all-roster coverage.

`qualify_arm_rip_original_controls.py` pins the exact current program/gfx,
stock emulator and read-only observer, actual object identities, two KOs,
absence of own-pose substitution and native completion. It writes
ARM_RIP_ORIGINAL_CONTROLS.json with representative coverage explicitly
separate from all-original-character/all-original-move acceptance.

Current lane hashes remain6BDCD94954D9AAECF1A4048C5CAD592C65DAAA12652E1EA303C3074F60968BDE
and A9B78FA921A15EEDB0F497677F8FE546E8B71B10A3E25451A8C6F65662FDCCDD.
Current clean rebuild, early drip placement, edge cases and broader gameplay
verification remain open. No release was promoted.
