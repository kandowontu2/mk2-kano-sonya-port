# Current Kano/Sonya port — rendered CPU grab checkpoint

The playable candidate remains `diagnostic_v635_native_shadow_rows`.
Run `PLAY_LATEST_TEST_BUILD.cmd`. No game code, executable, ROM/payload,
player launcher or release ZIP was changed by this checkpoint.

Five fresh, cold-start, real-input CPU paths now pass both their complete
native paired-state/recovery contracts and their sampled rendered composites:

- Kano choke versus Cage and Raiden, followed by ordinary native recovery.
- Sonya leg grab versus Sonya, followed by a complete bicycle miss/recovery.
- Sonya leg grab versus Kano and Liu Kang, followed by complete square-wave
  misses/recovery. The mirror and imported victim use their actual fighter IDs.

The v669 captures contain 428 exact displayed samples: 43,484,800 screen pixels
and 2,461,860 independently identified fighter pixels. All 3,559 body DMA
draws and 8,109 cached component checks match actual original/imported ROM
composites, offsets, flips, queue arguments and native DMA. Each distinct held
CPU pose appears in an exact displayed sample. Thirty-six nonvacuous regression
tests pass, including wrong ownership/queue cursor, missing body classification,
corrupted composites, same-palette effects and wrong rendered palette.

Evidence: `audit_v670_current_cpu_pair_display_checked_inputs` and its five
`audit_v669_cpu_queue_*` captures. Native drawing-queue provenance replaces a
rejected palette-only ownership assumption; the initial failures and captures
are retained and explained in checkpoint NOTES. No game failure was waived.

This is sampled current CPU grab/follow-up verification, not every rendered
field, artistic fidelity, every move/victim/slot, CPU KO or full-port acceptance.
Every other requirement and earlier verified scope remain as described in
`STATUS_2026-10-02_CURRENT_GAMEPLAY.md`, which is preserved unchanged because
it is an input to the previous frozen checkpoint.

## Still required

1. Wider CPU move/contact, block/duck/miss, cancellation and KO coverage;
   remaining human interruption/KO cases and rendered special-move frames.
2. Current Pit impact/shake/foreground, cinematics and audio.
3. Secret stages and wider pose/camera/grounding paths.
4. Complete towers, bosses, finishers, endings and audio on the current build.
5. Final regression and a matching production CMD/release ZIP.

Full-port acceptance remains false. The goal remains active.
