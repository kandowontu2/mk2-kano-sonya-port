# Current Kano/Sonya port — playable test build, not a completed release

Current candidate is `diagnostic_v635_native_shadow_rows`. Run
`PLAY_LATEST_TEST_BUILD.cmd` to open it. Production CMD v277 and the existing
release ZIP v258 have not been promoted. No game source, executable, gameplay
payload, ROM or player launcher was edited during this continuation.

## Newly verified

- Eleven fresh current CPU fixtures now pass their declared contracts: two
  natural campaigns and nine complete CPU choke/leg contact/recovery sequences.
  The paired checks cover 987 fields, including 462 held-animation fields,
  native damage, release/fling, both individual Main cleanup handoffs and the
  actual following ordinary attack or complete square/bicycle miss recovery.
  Kano choke passes versus Cage/Raiden; Sonya includes true Kano/Sonya victims
  and a mirror. Ninety regression/corruption tests pass. All 38 attempted CPU
  captures, including non-passes, are retained at
  `audit_v665_current_cpu_contacts_checked_inputs`. Wider CPU acceptance is
  still false; this does not prove every CPU move/contact, rendered frame or KO.
- 252 fresh real-input move fixtures cover all eight signature moves, all
  fourteen selectable opponents and both physical slots, including actual
  imported/mirror opponents and airborne square-wave contact. Grounded square
  wave is an expected anti-air miss. Native damage, true IDs/Main ownership,
  complete paired field chronology, recovery and ordinary walk/jump/punch
  follow-up pass. All eighteen Sub-Zero controls retain their original complete
  timelines. Fifteen baseline/corruption tests pass. Evidence: v656 captures and
  `audit_v657_roster_human_contacts_checked_inputs`.
- 52 fresh current-build fixtures cover positive, airborne, block, duck/far
  miss and leg crouch-block outcomes for all eight moves in both slots versus
  Sub-Zero, including cannonball flight/recoil and finite repel. Nine tests
  pass. Evidence: v652 captures and `audit_v654_current_human_matrix_checked_inputs`.
- Ten fresh startup interruption/retry cases cover blade, bicycle and leg grab
  in both slots with Kano/Sonya victims and mirrors. Four actual blade/bicycle
  KO/next-round cases check native animation cursors/cadence, cleanup and round
  health. Thirty tests pass. Evidence: v653 captures and
  `audit_v655_current_interrupt_ko_checked_inputs`.
- Four genuine loss/paid-continue campaigns reach all nine regular arenas in
  both slots. Fresh independent reconstruction matches all 1,218 samples:
  319,291,392 VRAM words and 123,748,800 screen pixels. All 30,451 imported
  components/763,757 native shadow copies verify. Actual P1 Sonya CPU/mirror/
  alternate-color paths are included. Eight saved-pass boundary tests pass;
  logs, VRAM/palette/PNG files, reports and models are pinned in
  `audit_v658_both_slots_native_floor_artifacts`.
- The five questioned crouching-turn roll contacts have actual original
  head/hat pixels inside the attack and native hurtbox. The explicit bounded
  decision is to retain the current box, not add target-ID immunity or a global
  height correction. The sixth opposite-side Raiden case is a genuine miss.
  Nine tests and full runtime artifact inventory are retained at
  `audit_v659_roll_fit_runtime_artifacts`. This is not universal collision-fidelity
  acceptance or original-MK3 matchup equivalence.

Earlier current-v635 checks also verify all four selection/ladder/first-match
UI flows (portraits, blinking border/player number, stance, backdrop, clearing,
own ladder icons, true fighter IDs and name shadows). Stock/imported idle soles
match in both slots in the Dead Pool reference, with 148 exact mobility drawing
passes. The original native shadow routine is used; custom whole-body shadow
projection was removed. No further global height offset is supported.

## Still required

1. Broader current CPU move/contact/paired choreography, cancellations and
   recovery; human blocks/misses/interrupt points and KO beyond the tested set.
   Successful outcome/recovery does not prove every held victim pose or every
   rendered special-move frame.
   Current CPU projectile block/duck scouts did not reach the requested shot;
   other retained captures include unaccepted KO/immediate-action/later-cycle
   paths. They still need explicit verification, not replacement by old passes.
2. Current Pit impact/shake/foreground/art/audio and other cinematic paths.
   The observed native Pit episodes are not complete cinematic acceptance.
3. Secret-stage and wider pose/camera/grounding checks. Saved-pass replay does
   not model unsaved inter-pass erasure/CPU writes; native arena 6's shadow
   gating is preserved, not counted as visible-shadow proof.
4. Complete towers, bosses, finishers, endings and audio on the current build.
   Loss/continue campaigns are not tower clears.
5. Final regression and matching production launcher/release ZIP.

Floor and full-port acceptance remain false. Failed diagnostic/checker attempts
are retained and explained in checkpoint NOTES; no gameplay/pixel failure was
waived. The previous three status files were preserved under v657/previous_status
before updating their current summaries. No material data was deleted.
