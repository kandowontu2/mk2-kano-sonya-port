# Own initial arm-rip grip pose

The T-pose did not meet Jax's bent-forward grip. The built-in image tool
revised only the two first-column poses so both hands extend toward the
opponent and down toward waist height. Selected source and exact prompt:
assets/arm_rip_draft/body-grip-atlas.png and GRIP_PROMPT.md. The other18
indexed frames are not regenerated from the new atlas.

`apply_arm_grip_sources.py` converts just those crops to own palette-index
PGMs. Initial runtime trials225/226 revealed the reaction's actor mirroring
turned the hands away from Jax. `normalize_arm_grip_facing.py` therefore
normalizes these editable indices to the native convention and reflects
their foot origins too, preserving world-space grounding. This is a data
orientation conversion, not another character or proxy body.

`build_arm_rip_assets.py --refresh-grip-pixels` verifies the previous outputs
and permits changes only to those two source frames. All existing socket
hashes are checked before regenerated physical-socket bytes replace them.
The old1,856,309-byte prefix is unchanged; the complete own arm-rip addition
is now74,429 bytes. No duplicate build tree or8-socket folder was created.
Final hidden compilation passed18 seconds, no window.

Current stock MAME runs227–230 each completed9,000 fields, two natural KOs
and147-field native arm-rip activation followed byffff completion. Both
fighters on both physical player sides retain their true IDs, five body
phases and two own detached-arm objects through all five arm frames, with
no missing-art, illegal recovery, Lua errors, guest writes or timeouts.
All four first-pose captures were inspected: the hands now meet Jax's hands
and the feet remain grounded, instead of forming a T-pose or pointing away.

ARM_GRIP_QUALIFICATION.json compares the actual earlier runtime221 program
headers and interleaved gfx with the current sources: exactly two image
payloads changed and all other18 images are identical. It also verifies
the facing reflection and reflected foot origins, and pins all four viewed
captures. ARM_RIP_RUNTIME_QUALIFICATION.json verifies20 compiled headers
and the physical sequence. Current program lanes:
D66CC53901C1503ABDBB3A5C5B91E5BFE9C847FEE8AD07DE0F12DB10AB0E186B and
D339E6F43D8CB9B6AEE5EFCB9940C2FF0869940ECA58CBAF86041B71C1BCE3ED.

This accepts only the captured initial grip contact. Blood placement,
entire-animation visual polish, edge cases, original-character controls,
current clean rebuild and broad gameplay/release verification remain open.
Source preparation has243 files and zero structural-token differences,
not current-link independent compiler proof. No release was promoted.
