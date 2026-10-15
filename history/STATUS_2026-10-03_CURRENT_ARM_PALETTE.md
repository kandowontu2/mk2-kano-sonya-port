# Native detached-arm costumes verified in a limited test scope

Current experimental candidate: diagnostic_v1071_native_detached_arm_costume.
EXE SHA256: AD26399227274919A04D48B2C6F7201CC458F8BA3F6553D7F217829B4AFBE32F.
Payload SHA256: 5D78E543EA1E387461BD7EFF0958F9829565469CD51D5B2EE0A6CF1D90F0D322.
Native driver SHA256: 1DF1D1217776DBC3830F00ED078589A925A81F7C356F8EADE117907711A68CF6.
Installed EXE, playable CMD files and release ZIP are unchanged. NOT release-ready.

## Before diagnosis

The preceding turn was a status response, not implementation progress. This turn
revalidated all 11,025 checkpoint1067 pins. The only difference is the exact
declared native driver transition from29A023... to1DF1D...; its original source
is retained in audit_v1070_arm_palette_source_transition/input_sources and
independently hashed. Removing ONLY the inserted palette-router block reproduces
that original source byte-for-byte. No original artwork or other source changed.
No emulator remained running at the start or after the paired tests completed.

## Native costume path

The original Jax detached-arm constructor embeds a normal palette and overrides
only Mileena. The new96-byte native router in unused0FBC00 program ROM uses the
ACTUAL Jax victim actor's real17/18 ID and actual flag6 to select the corresponding
native alternate palette. It restores A1/A2, status and stack before invoking
the original FF841090 palette applier. Other victims and normal costumes retain
the original stock path, including Mileena's FF90DD00 override. No proxy ID,
health/timer patch or live diagnostic assistance is installed as gameplay logic.
The matched payload is unchanged from the verified1061 blood correction.

Independent1074 passes four ordinary physical-input Kano/Sonya runs in both
slots, original two collision KOs, original BBBB LP parser, native147-field
completion/continue, all six true-ID table consumers, ten body/arm poses,
native grounding, FIFO/DMA geometry, actual palettes and clipped presented pixels.
Independent1083 passes four EXPLICITLY CONTROLLED flag6 diagnostics, proving
body and BOTH native detached arms use the full expected alternate hardware
palette. This is NOT proof of natural alternate-costume selection. Failed1075's
65-entry-source/64-entry-hardware comparison is preserved;1083 bounds the
comparison to the63 representable nontransparent hardware pens.
Independent1079 passes two genuine Mileena cases and preserves her original
palette override, native timing and continue. These are not substituted victims.

## Unexpected image differences resolved, not ignored

Failed1080 tried to transfer previous normal whole-image equality. That assertion
remains rejected and its evidence is preserved. Read-only1085 observes ORIGINAL
RNG entry, the existing HCOUNT hardware read (never rereading/replacing it), and
the native rotated result, plus all native drawing FIFO records. Versioned1086
runs eight paired old/new physical-input cases with exactly the same observer.

Independent1087 proves all8 runs terminate at5198 with native147-field completion;
each replay reproduces ALL prior screenshots for its own build byte-for-byte:
1,224 replay PNGs across four old/new pairs. It reconstructs every original RNG
shift, overflow, carry and HCOUNT-controlled rotation:773 RNG calls per run.
Each pair first differs at serial89/actionage88, AFTER the new palette helper,
with the SAME seed and pre-rotation value but a different actual beam count.
This explains original native blood spray variation, not a costume/position bug.

All real fighter and owned-arm identities and native drawing fields match the
prior build; only scheduling FIFO addresses differ. Other native rendering is
also unchanged after accounting for free-list addresses of nonfighter objects.
Every changed pixel in612 actual paired scene PNGs lies on decoded nontransparent
ORIGINAL native blood pixels already drawn by that frame, including persistent
puddle/fade pixels. No arbitrary rectangle, altered fighter geometry or generic
visual-difference exemption is accepted. Original and new whole guest ROMs are
independently bounded to the96-byte helper and6-byte jump. Original RNG is intact.
Four1089 in-memory corruption checks reject wrong beam count, wrong seed,
one-pixel true fighter shift and an unrelated image pixel. Fixtures modify no files.

Main agent reviewed120 actual scenes:48 normal,48 controlled alternate,24 genuine
Mileena. Six previously viewed controlled/stock contacts are exactly reused in
1088; four normal contacts were viewed directly. Red blood, matching controlled
costumes and original stock override/completion presentation are accepted ONLY
in this scope. Actual camera-edge clipping is not unoccluded full-body proof.

## Still required for the unchanged full objective

Prove natural alternate selection and remaining victim variants. Replay the
established20 native regressions on THIS1071 candidate:1055/1056 remain1048
historical evidence. Finish Kung Lao split/other half and successful native hat
kill, remaining stock fatalities, all arenas/cinematics/audio, real towers/
Kintaro/Shao/continues/endings, final combined native CSS blink/borders/P1 numbers
and portrait teardown, owned ladder icons, names/name shadows, floor shadows/
standing height, complete moves and human/CPU play. Existing narrow proofs do
not waive any gate. Update playable CMD/ZIP after appropriate complete checks;
safe obsolete-build cleanup remains. No deletion occurred. Full goal stays active.
