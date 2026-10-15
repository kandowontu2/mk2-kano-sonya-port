# Current playable test build and genuine Sonya CPU coverage

Run PLAY_CURRENT_V1411_TEST_BUILD.cmd. It launches the matched native grab-audio
candidate diagnostic_v1411_native_grab_audio, without diagnostic inputs or cheats,
with isolated play settings. EXE SHA256 is
01EF3950691A890BAA41723D99935E44A28B09A7431EA78EC5DBF8E0E90630C3;
payload SHA256 remains
5646E839C73C4DB89BCF7CC87ECADBDA94B1E0D30EB1C0D2ED50A21A5524E23D.
This is a development playtest, not full release acceptance. Older CMDs remain
unchanged and still launch their explicitly named older builds.

## Accepted evidence

- audit_v1435_grab_audio_human_matrix_checked: all 52 actual human fixtures
  pass (18 positive, 34 defensive). Every prior native event matches current
  v1340, and all 156 complete before/recovered/final screens are byte-exact.
- audit_v1433_grab_audio_ui_checked: all four character/slot selection,
  immediate teardown, native ladder portrait, actual first-match identity and
  lifebar black-shadow checks pass. This is not full campaign acceptance.
- audit_v1434_grab_audio_ground_shadow_checked: all four tested Dead Pool
  mobility/owned floor-shadow cases pass, not all arenas or special phases.
- audit_v1437_current_launcher_checked: normal two-second CMD boot from a
  different working directory passes without checksum warnings or autoboot.
- audit_v1454_sonya_cpu_display_checked: real Sonya CPU leg grabs against human
  Kano and Sonya in physical CPU slot 2, and against human Sonya in physical
  CPU slot 1. Complete held phases, native damage, each actor's own ready
  handoff, subsequent ordinary continuation, full CPU body/Main/action store
  ledgers and original store instruction words pass. All 264 sampled native
  scanouts, full-body composites, palettes, graphics, FIFO, VRAM and DMA match.
- audit_v1458_physical_cpu_counterexamples: all three unchanged real baselines
  pass; 43 in-memory state/physical-role/pose/health/instruction/cleanup and
  ordinal corruptions are rejected. Actual captures are unchanged.
- audit_v1464_repeated_sonya_cpu_display_checked: genuine physical P1 Sonya
  CPU versus P2 human Kano completes two consecutive leg contacts, 35 damage
  each. Each has all five phases, 46 held fields, native fling and individual
  CPU/victim recovery. First complete is frame2746; second complete is2856;
  terminal is2886. All 121 retained full native scanouts and both pairs' held
  pose coverage pass, along with the whole native flag/action/health stream.
- audit_v1465_repeated_cpu_counterexamples: ten additional in-memory
  second-pair/ownership/health/cleanup/ordinal corruptions are rejected.

The CPU character/order, health, positions, RNG and stage were never assigned
by an observer. New physical-slot-2 controls use the already-tested real P1
UI navigation. The physical-slot-1 route reaches Sonya using boot-frame605
actual coin/start timing, original ladder order FFFA3780 and stage zero.
The current guest/source/assets did not change during this turn. The audio
fix was built previously; this turn promotes it and extends actual coverage.

## Preserved diagnostic failures and their resolution

audit_v1441 preserves the first explicit-P2 state-model rejection of a native
ordinary hit-to-recovery publication (0106 -> 0600), earlier attack cleanup,
and a later real second entry. Successors check the actual native opcode,
operands, complete action/body/Main store history, individual handoffs and
entry chronology; no game state or rendered evidence was changed.
audit_v1447 preserves a counterexample helper's duplicate ready-clear-row
error. audit_v1455 preserves a verifier local-variable naming collision;
v1456/v1457 separate actor-field and instruction offsets. v1458 passes.

audit_v1450 correctly rejects a second real paired contact as an ordinary
follow-up. The shorter v1446 capture ended before that victim's recovery.
The new v1459 observer preserves actual controls but waits for both full
paired recoveries, retains each completion snapshot separately, and records
the longer real native display window. audit_v1462 preserves an initial
model's incorrect assumption about the pre-entry callback ordinal. v1463
derives it from actual prior entry instructions, including ordinal zero
before the first action. v1464 and v1465 pass on unchanged v1460 evidence.

## Full goal remains open

Sonya CPU leg integration is now verified in both physical slots for these
actual opponents, including the repeated pair. This does not establish the
full AI repertoire or all opponents. Remaining move choreography/audio,
interruptions and KO paths, finishers/native animation consumers, other
arenas/shadow phases, genuine towers/bosses/continues/endings/secrets/cinematics,
final packaging and obsolete-build cleanup are still required. No release ZIP
was updated and no material files or old build folders were deleted this turn.
The objective remains natural integration in all aspects, not a narrower
passing test subset.
