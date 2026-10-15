# Blade lifecycle and emulator shutdown follow-up

Candidate: `diagnostic_v44_lifecycle_candidate/mkport_lifecycle.exe`, SHA-256
`6D592F4D9B47F8D1A44BD61363D7DCEEBA4CD1BCBFFA5F60F1303E502A4BA18F`.
Required v44 payload: `91001C2E6551CB850F919971D67806DE31D5F34D97C6CE0D9764B4F367F19DB3`.

Nine terminal real-input tests pass: both Kano player sides against Sonya,
Kano, Kitana and Sub-Zero, plus another P1 Kitana run. Each performs seven
blade swipes to a KO and an eighth after the native next-round transition.
They check pose phases, one strike, blood/effect ownership and cleanup,
native wins/HUD reconstruction, true IDs, mirror palettes, names/shadows,
display cleanup, traps and stalls. The exact cases and log hashes are in
`diagnostic_v44_lifecycle_candidate/verification.json`.

The preceding feedback executable passed the combat checks in
`regression_v44_blade_rounds_side1_kitana` but crashed during shutdown. That
case remains failed. Disassembly of the actual executable traced the crash
to destruction of a retained Lua load result after its Lua engine had already
been destroyed. `mame_machine_manager` now releases `m_autoboot_script` before
`m_lua`. The new candidate contains that lifetime-order correction; gameplay
source is unchanged from the feedback candidate. The older 102-case suite
does not count as testing this new executable.

Installed CMD stays v42. Both released ZIPs are unchanged. This milestone does
not complete remaining specials, full victim semantics, voices, finishers,
AI participation or complete progression.
