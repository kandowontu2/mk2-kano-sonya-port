# Current recorded-evidence refresh

After the physical campaign-controller changes, the existing completed current
6AE0 recordings were requalified against current verifier sources. Runtime CSVs,
frozen Lua controllers, execution receipts and ROM archives were not rewritten.
No emulator or compiler was launched for this refresh.

- Fourteen explicit special fixtures cover all eight specials on both player
  sides (sixteen actor/move/side cells). Detailed checks and
  SPECIAL_MATRIX_QUALIFICATION.json pass with current evidence hashes.
- Eight explicit lethal finisher/reselection fixtures pass detailed finisher,
  fresh-match recovery and OWN_FATALITY_MATRIX_QUALIFICATION.json checks.
- Eight explicit positive nonlethal/reselection fixtures and eight explicit
  punch-history-ineligible command fixtures pass detailed checks and both
  nonlethal matrices. Sonya Friendship lifecycle checks are refreshed too.

The ordinary lethal and positive nonlethal matrices previously checked detail
pins and the recovery-report file hash, but not every evidence pin inside that
recovery report. They now call recovery_evidence.verify, requiring mandatory
receipt/controller/verifier pins, current recovery-verifier bytes, and every
additional recorded recovery-evidence hash. Matrix reports pin the helper too.
Tests first accept an untouched fixture, then reject changed cleanup evidence,
a stale verifier digest and an omitted mandatory pin.264 local tests pass.

requalify_recorded_finishers.py is an explicit requalification-only entry point
for these24 existing named fixtures. It checks exact recorded arguments and
terminal successful receipts before rechecking actual ROM bytes and traces.
It does not create replacement runtime evidence or launch MAME.

The subsequent requalify_recorded_stage_morph.py refresh also passes all36
explicit current recordings:16 stage/chord/Pit-rejoin cases,4 base morph/
late-throw cases,8 extended morph special cases, and8 transformed lethal/
fresh-Shang cases. Detailed checks, stage and transformed-finisher matrices,
and morph-art trace checks pass against current source pins. Exact completed
fixture arguments are checked before requalification; failed earlier melee
attempts are not selected. This entry point does not launch MAME or the compiler.

The eight explicit transformed nonlethal recordings now also requalify with
current complete ROM and evidence hashes: Kano-morph Friendship/Babality
positives and Sonya LP-morph native punch-history rejection cases on both sides.
See MORPH_NONLETHAL_REFRESH.json and requalify_morph_nonlethals.py.

Not every older interaction report is current. The spear report was still
hardcoded to165-era runs, so four new9000-field stock-MAME tests were recorded:
stock_wolf_6ae0_spear_{17,18}_p{1,2}. All complete normally and pass actual
26-chip verification, expected8HP damage, own victim pose identities, pull from
208 to64 separation,110/111 contiguous stun fields and return to stance.
The verifier now requires four explicit run names and pins current source,
receipts, frozen observers and traces.266 local tests pass. A single decoded
Sonya-player1 spear180 PNG was visually inspected, not a whole-animation review.

Other historical interaction reports still need current-ROM refresh or review.
Finite other-own-victim
coverage is not arbitrary-victim, edge/interruption, whole-game audio or full
campaign acceptance. Kano's earned campaign/ending remains unverified. The
production ROM and development IPS ZIP are unchanged; releaseReady stays false.
