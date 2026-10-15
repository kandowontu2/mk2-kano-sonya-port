# Bicycle round transitions and startup interruptions — v46 follow-up

The current v46 candidate passes 90 refreshed runtime cases, 37 asset tests
and one new input-driver test. A separate candidate CMD also passed its ROM
audit and an additional actual P2 Sonya mirror-match/bicycle smoke test.
This is continued integration work, not completion of the full roster goal.

## Current artifacts

- Executable: `diagnostic_v46_bicycle_asset_candidate/mkport_candidate.exe`
  SHA-256 `FCA7B8174C7D019236835ECFBEB8E8254622CE4405CA8842CAD04782F47FE96A`.
- Required payload: `diagnostic_v46_bicycle_assets/roms/mk2ks/mk2ks.mdata`
  SHA-256 `5CA9EE80B2737F7A295554C22BF3D4068C2552F90C744BA1D125B41251945D55`.
- Refreshed exact inventory and checksums:
  `diagnostic_v46_bicycle_asset_candidate/lifecycle-verification.json`.
  Its one-shot audit is `tools/verify_bicycle_lifecycle.ps1`.
- Unit-test log: candidate `lifecycle-asset-tests.log`, 38 tests with no skips.
- Separate WIP launcher: candidate `PLAY_CANDIDATE.cmd`. It uses the matching
  v46 data and separate settings/saves, without an injected test script.
  `launcher-audit.log` and
  `regression_v46_bicycle_candidate_cmd_side2_sonya/result.json` verify it.

There were NO gameplay-source, executable or payload changes in this follow-up.
The normal `PLAY_MK2_KANO_SONYA.cmd` remains on installed v42, and both delivered
release ZIPs remain unchanged. The cleanup request was withdrawn as old context;
no further cleanup was performed. No candidate promotion or release packaging occurred.

## What the repeated tests found

The original P1 Kano-victim nine-cycle case passed. The remaining initial matrix
passed all three other P1 victims, but failed all four P2 victims after their
first bicycle. In those cases there was no second action entry or damage.

The shared selector driver listed P1 High Kick but omitted P2 High Kick from
its per-frame `clear_value()` list. Thus the first P2 press remained held for
the rest of the run. This was a driver defect, not a player-side game fix.
`mk2ks_selector_exit_test.lua` now clears that field symmetrically; its hash is
`023ABF4B0EC92A8566AE76AD86B7D44736E82B0AB7E11B7EC2B8719B5E7CC9C5`.
The new `tools/test_selector_input_driver.py` checks all ten combat controls
for each side belong to the clear list. All 78 previous runtime cases were
rerun with the corrected driver, rather than treating earlier P2 tap tests
that inadvertently held HK as proof of release-sensitive input behavior.
The earlier manifest/logs remain historical and were not overwritten.

## Exact new coverage

Eight `regression_v46_bicycle_rounds_inputfix_side{1,2}_{kano,sonya,kitana,sub_zero}`
cases each execute eight ordinary B,B,D+HK commands to a real knockout, then a
ninth command in the actual next round. Checks require nine native entries,
nine bounded paired flights/releases, exact 22-point/clipped damage, true IDs,
native Sonya HUD/win records, restored health and grounded state, and full
custom/mirror palettes. That is 72 completed bicycles over eight real round
transitions. Repetition naturally reaches an edge, but is not a substitute
for dedicated left/right corner choreography tests.

Four `regression_v46_bicycle_interrupt_verified_side{1,2}_{kano,sonya}_delay{9,8}`
cases counter an already entered bicycle with an ordinary crouching uppercut.
The hit arrives two fields after entry for P1, one field after entry for P2.
Sonya takes exactly 40 damage, the opponent takes none, and no collision query,
paired tick or release runs for the interrupted startup. After native recovery,
a fresh B,B,D+HK performs one complete 48-field paired flight, one release,
and exactly 22 damage. Both fighters recover grounded with their own identities,
no attached object or paired-state residue, and intact mirror palettes.

The initial counter timings 17/16 and P1 timings 12–14 were too late: the
uppercut missed the displaced startup and the bicycle caught its opponent.
P1 timings 8–11 then proved real interruptions, before the four final cases
used fixed 9/8 timings. Those exploratory results are retained separately,
not counted in the final 90. These are startup interruptions only, not
projectile collisions or cancellation while the fighters are already paired.

The other 78 cases consist of 50 bicycle input/victim cases, 12 core roster
cases, 12 leg-grab near/corner regressions, and four choke regressions, under
`regression_v46_bicycle_inputfix_*`. All 90 terminal processes exited zero.
Applicable display cleanup, native identity/name/shadow, stall, trap and leak
checks passed. The CMD smoke is separately recorded, not included in that 90.
P2 Sonya mirror counter, retry and recovered-stance screenshots were inspected.
All functional captures remain 400x300.

The new launcher initially used a quoted Windows path ending in a backslash,
which swallowed following arguments instead of performing the requested audit.
Using `%~dp0.` for its INI directory fixes that quoting error. The final audit
requires the actual ROM-verification output, not just exit zero, and the
subsequent headless real-input CMD smoke verified argument forwarding.

## Remaining scope and next work

Dedicated bicycle corners, projectile/boss/CPU interactions and comprehensive
other-special regressions remain. Move-specific impacts/voices/screen shake,
original fighter voices/announcements, full stock-body contact/throw/victim
artwork, finishers, AI roster participation, full ladder progression/endings,
and final release/installed-launcher acceptance are still unfinished.

Read-only preparation for bicycle feedback identified original MK3
`FF9E6040`: a process+250 countdown invokes `FFAA6680` on the first paired tick
and every seven fields thereafter. This has not been implemented or validated
against a corresponding MKII sound primitive yet; do not claim audio completion.
