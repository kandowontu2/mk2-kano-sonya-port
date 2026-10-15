# Native Pit first-pose repair — current test build, not a finished release

Run `PLAY_LATEST_TEST_BUILD.cmd` for `diagnostic_v680_native_pit_initial_cache`.
The production launcher and release ZIP remain unchanged. The previous v635
candidate remains available; its driver source and latest-test launcher were
preserved before editing under `audit_v680_pre_pit_initial_cache/sources`.

Actual displayed v678 captures exposed a real defect: the new Pit actor reused
the physical fighter's previous KO component cache. Its first native FIFO draw
published pose0 and briefly rendered the sideways knocked-down fighter before
the scheduled first falling copy. Earlier phase/state checks did not prove this
first visible field correct.

The v680 driver installs a synchronous native constructor preloader for true
IDs17/18 only, using their own first falling composite and the original complete
component copier. It preserves A1..A7, the actor, Main and SP, then executes the
displaced own coordinate-table MOVI. All other IDs bypass the copier. There is
no identity proxy, state override, renderer mask, special scene skip or custom
animation timer. The original twenty falling steps and impact retain cadence.

The complete actual 1,048,576-byte guest ROM comparison finds exactly57 changed
bytes, all within the six-byte constructor call and64-byte initializer. Every
other guest ROM byte is identical to v635, and the payload/graphics assets are
unchanged. The unused64-byte tail remains FF. All19 ID branches and register
masks have an independent instruction-model check; this is not a claim that
every stock cinematic has a new rendered replay.

Two fresh cold, input-only900-second campaigns each finish49,237 fields without
reset. Kano P1 completes one genuine Pit scene; Sonya P2 completes two. Every
observed scene has a bounded own preload,20 native falling copies, own impact,
native exit, real loss/paid continue/reselection and sustained next own-ID fight.
Sonya's second encounter has complete native state/cache proof, not a second
full raster capture. Post-first-Pit campaigns need not be identical to the old
build: changed rendering work changes later native timing/random decisions.

Both first scenes retain331 consecutive displayed fields. For each scene,
329 fields independently reconstruct every observed native drawing pass,
VRAM word and displayed pixel; their first visible field shows the correct own
falling pose. The two DMA-free opening flash/blank fields contain writes outside
the command recorder and are NOT called reconstructed. Instead their complete
VRAM, palette, display registers and PNG bytes must match the exact matched
pre-edit capture. The rejected all-fields-replay result is retained, with its
actual nonzero errors rather than relabeled zeros.

Original five-step/five-pixel camera shake, male/female voice groups and actual
serialized native DCS effect/voice commands verify. All411 native audio-update
blocks per scene match a timestamped matched WAV without best-sample searching.
Kano matches its historical recording. Sonya matches a fresh current-build
recording: the old recording differs during part of the post-Pit interval, so
it is explicitly not historical whole-interval PCM preservation. Correctness
of all voices/effects, subjective art/audio fidelity and all cinematics remain
unproven. Forty-one focused baseline/corruption regression tests pass.

Evidence: v681 cold captures, v682 verification/regressions (failed attempts
retained), v683 current Sonya native WAV, v684 whole guest-ROM comparison, and
the consolidated v685 checked-input checkpoint. The earlier v675-v677 recorder
failures and v679 stale-cache failure remain available and are not passes.

Still required for the full natural-character goal:

1. Complete individual fatalities and remaining cinematic/art/audio work.
2. Wider human/CPU interruption, miss/block/KO and rendered special coverage.
3. Secret stages and broader pose/camera/grounding paths.
4. Full towers, bosses, other finishers, endings and all character audio.
5. Final whole-scope regression and matching production CMD/release ZIP.

This update fixes one actual integration defect; full-port acceptance remains
false. Earlier v635 evidence is historical, not silently re-certified as v680.
No material files were deleted and no finished release was promoted.
