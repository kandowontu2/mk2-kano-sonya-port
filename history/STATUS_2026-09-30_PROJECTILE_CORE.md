# Projectile collision-core candidate — not promoted

The source and `diagnostic_v291_native_projectile_core` now correct a real
gameplay defect. Kano and Sonya had independent roster IDs and descriptor rows,
but those rows still contained Liu Kang's expanding fireball geometry. Actual
collision rectangles did not match their detached knife/ring graphics. Kano's
knife missed standing, blocking Sonya by one vertical pixel while still hitting
her idle pose, and the inherited rectangles could contact ahead of the artwork.

The first frame-envelope candidate fixed standing blocking but hit crouching
Sonya with the knife's glowing trail. It remains an unaccepted diagnostic;
`audit_v291_guarded_geometry_kano_miss_p1` and its P2 counterpart are retained.

Original MK3 input-only runs identified the actual travelling collision cores:

| Projectile | Original descriptor/core (edge, top, width, height) | Converted core | Port release origin |
| --- | --- | --- | --- |
| Knife | `FFA5B590`, Kano attack index 21: `35,-24,51,50` | `135,48,51,50` | `-12,-40` |
| Ring | `FFA5A9A0`, Sonya attack index 18: `108,35,36,11` | unchanged | `0,0` |

The knife converter already translates the frame pivot by +100,+72. Translating
its collision core identically and compensating its release origin preserves
the donor's +88,+32 flight placement relative to the fighter. The ring uses the
fighter origin. These are native descriptor/action operands, not Lua gameplay
writes, actor substitutions, host-drawn effects or collision exceptions.
MKII's native facing, 22-point hit damage, six-point travelling block chip,
reaction scheduling and cleanup remain in use. Stock attack-table/descriptor
bytes are verified against the original MKII ROM region checksum.

## Verified checkpoint

`audit_v291_projectile_core_checked_inputs/result.json` records:

- Twelve cold, real-challenger-join cases: both moves, both player slots, two
  projectiles each, against standing idle, standing guard and ducking victims.
- Every paired field across 601 frames, original health writes, actual child
  creation/owners, converted frame records, native rectangles in both facing
  directions, hit/chip/no-hit behavior, retirement and sustained ready recovery.
- Original MK3 knife/ring read-tap reference data, with no health/position writes.
- 440 reference tests: the previous 413 plus 27 candidate/evidence-rejection tests.
- Candidate and existing production CMD ROM checks; candidate source/build hashes
  and each cold case's archived launch scripts verified unchanged.

Sixteen current command/scene diagnostics pass their native command, selection
teardown, identity, name-shadow and no-stall/no-trap runtime gates. Fourteen also
pass the old overall gate. The two `native` cases remain **overall failed**:
their fixed-frame/crop knife-image checker samples the previous release location
or an already-retired projectile. They are not rewritten or presented as green.
Frame-aware rendered verification is still required; inspected current images
are useful evidence but do not substitute for that gate.

## Build and remaining work

Candidate executable SHA256:
`4197507C69DE7039082FD54C0AF5E70657FABBBCE28BA52F913613CE850E94D9`.
It uses the unchanged matched v277 payload. Source now matches this candidate,
not the historical source hash in the v277 build manifest.

`PLAY_MK2_KANO_SONYA.cmd` still launches v277. Its executable, payload, CMD and
the old v258 release ZIP remain unchanged. No final-release claim is made.

Next: frame-aware rendered projectile checks and authentic impact choreography,
then current-candidate full ending/restart/join and other-move/CPU regressions.
Broader unassisted gameplay, remaining finisher/victim fidelity, whole-game
audio/visual/play-feel QA and final launcher/release-ZIP promotion remain open.
The full natural-roster goal remains active.
