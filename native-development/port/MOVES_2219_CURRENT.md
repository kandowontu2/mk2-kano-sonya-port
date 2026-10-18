# Current 2219 move verification

The current normal-contact aggregate now passes136 finite cases:
17 actual standing/crouching/jumping/proximity actions, both actors and
player sides, hit/block variants. `NORMAL_CONTACT_ACCEPTANCE_2219.json`
rechecks actual26-chip ROMs, terminal stock/no-write/frozen-input receipts,
native actions, exact source damage, recovery and guard. Newer recordings
also bind native p_hitby. Includes all14 ordinary attack types plus knee,
elbow and throw. Hyperspecific edge whiffs are retained separately, not
counted as hits. Sonya diagonal-punch contacts use220-gap physical approach;
other character/attack spacings are explicit in each receipt. No arbitrary-
spacing/all-victim/all-frame audiovisual or full-port acceptance inferred.

The mirrored normal run `stock_wolf_2219_normals_mirror_01` completed exit0
and also observes28/28 expected action/late-recovery cells: Sonya P1 and
Kano P2. Original28/28 requalified after inspector generalized actual role
mapping. Combined56 finite character/side/action/recovery observations do
not establish every normal's hit/block/damage behavior. Mirrored roundhouse
and uppercut screenshots were sampled. Full suite359 passes.

Dedicated `stock_wolf_2219_normals_01` now observes14 ordinary attack types
for both characters (28 finite actor/action/recovery cells), terminal exit0.
Per-field true17/18 identity, expected action tags and late stance recovery
checked against actual current26-chip runtime. See its
`NORMAL_MOVE_OBSERVATIONS.json`. Roundhouse/flying-kick images sampled.
This does not prove all damage/block behavior, facing/side variants or
every animation frame. Requested input alone is not counted as success.

Program SHA256: `221919459A4129FFDB37C8A3E9EC7F9AA6210D99AED00A35BC3256842C5E1F5A`.

After the explicit Kano/Kintaro jumpkick harness flag, the complete recorded
move-family requalification again completed exit0: ordinary16, own lethal8,
morph14, transformed lethal8, nonlethal16, stage16. Actual current-ROM and
evidence gates rerun; no emulator, ROM or frozen-recording rewrite.

Latest recorded-family requalification after the explicit Kano boss harness
flag completed exit0:16 ordinary special/side cells,8 own lethal/recovery,
14 morph cases/art cadence,8 transformed lethal/fresh-Shang,16 nonlethal
positive/negative,16 stage/chord/Pit/rejoin. Frozen runtime evidence and ROM
bytes were not rewritten. This does not upgrade historical6AE0 floor-shadow,
ordinary freeze-victim or audio observations to2219 runtime evidence.

The complete recorded-family refresh also exited0 after the remaining-human
campaign flag: ordinary16, lethal8, morph14, transformed-lethal8, nonlethal16
and stage16 cases/cells, no emulator rerun or frozen-recording rewrite.

After the Mileena-specific harness flag, the complete recorded-family refresh
`requalify_2219_moves.py` exited0 for ordinary16, lethal8, morph14,
transformed-lethal8, nonlethal16 and stage16 cases/cells. Actual current-ROM
and detailed evidence gates were rerun; no MAME or frozen-recording rewrite.

After the explicit neutral-uppercut campaign flag changed the harness,
all16 ordinary special/side cells, all8 own lethal/recovery cells and all8
transformed lethal/fresh-Shang cells were requalified from unchanged frozen
recordings against current source pins. Each coordinator/verifier exited0;
no emulator was rerun and no recording/receipt was rewritten. All14 recorded
base/late-throw/all-special morph cases and both-sided morph-art timing/
grounding also requalify. All16 nonlethal and16 stage cases/matrices also
requalify, coordinators exit0. Other proof families still require normal
pin-freshness checks before final acceptance.

The current native ROM has completed these hidden, sequential stock-MAME regressions:

- `stock_wolf_2219_special_01` through `_14`: all eight specials on both player sides (16 move/side cells). See `SPECIAL_MATRIX_QUALIFICATION.json` and each run's detailed qualification.
- `stock_wolf_2219_fatal_01` through `_08`: Kano extract/laser and Sonya kiss/bubble, each on both player sides against the other added character. See `OWN_FATALITY_MATRIX_QUALIFICATION.json`.

Each fatality run exited normally without timeout, observed native completion, and qualified 600 fields of fresh-match combat afterward with 78,000 hardware palette comparisons. The matrix checks the actual current 26-chip ROM contents, stock emulator hash, frozen controller, and detailed evidence pins. The fatality coordinator exited 0.

These are bounded runtime proofs, not whole-port acceptance. Arbitrary victim coverage, transformed finishing moves, nonlethal finishers, stage finishers, campaign completion, and full audiovisual acceptance must not be inferred from these two matrices. Previous-build evidence remains historical unless separately refreshed. No program, emulator driver, game rules, or AI was changed for these refreshes.

`stock_wolf_2219_morph_special_p1/p2` and `stock_wolf_2219_morph_late_p1/p2` completed and qualified; coordinator exit 0. These prove transformed knife/ring, actual own identities, automatic return, and paired throws overlapping nominal morph expiry on both player sides. The separate morph-art verifier passed forward/reverse pose order, four-field cadence, and grounding. They do not cover the other six transformed specials.

`refresh_morph_regression.py --all-specials` now plans ten sequential runs covering projectile, ball, square, melee, and grapple profiles on both sides (all eight specials). Its two new plan tests pass; this is scheduling coverage, not runtime evidence. Any repeat must use a fresh prefix and must not overlap another emulator run.

All eight transformed-fatality/fresh-Shang refreshes `stock_wolf_2219_morphfatal_{extract,kiss,laser,bubble}_rejoin_p{1,2}` qualified. The coordinator exited 0; see `MORPH_FINISHER_REJOIN_MATRIX_QUALIFICATION.json` and the individual runs. This covers each own lethal finisher while transformed on both player sides against the other added character, not arbitrary victims or nonlethal finishers.

All ten `stock_wolf_2219_morphall` runs qualified and the coordinator exited 0: knife/ring, ball, square, blade/bicycle, and choke/leg-grab profiles on both sides. Each checks actual current ROMs, own identities/poses, native action and damage, recovery and automatic return. Square also checks jumping-opponent launch and grounded-attempt rejection; grapples check contiguous paired owner/victim actions. Forward/reverse morph-art timing and grounding also qualify. One final transformed-Sonya stance screenshot was visually sampled; this is not whole-animation visual acceptance.

All 16 `stock_wolf_2219_nonlethal` runs qualified and coordinator exit is 0: eight positive Friendship/Babality cases with fresh-match recovery and eight punch-ineligible rejection cases, covering both characters and both player sides. See the nonlethal and negative-nonlethal matrices. All 16 `stock_wolf_2219_stage` cases also qualified, coordinator exit 0: Dead Pool/Tomb positives, missing-chord rejection, Pit cinematics and fresh-match recovery, both actors/both sides. See `STAGE_POSITIVE_MATRIX_QUALIFICATION.json`. This is own-pair coverage, not all possible victims/chords/edges.

The ingestion-reaction verifier now requires explicit unique current runs,
checks all 26 actual ROM chips, derives victim identity from recorded arguments,
rejects original-control profiles/duplicate role cells, and pins sources and
runtime evidence. Syntax compilation passed. A deliberate invocation on old
265/266 recordings rejected their non-current program bytes before producing
a new qualification; fresh 2219 ingestion runtime/visual review is still needed.
`refresh_ingestion_regression.py` is collecting those four own-victim/side
cases sequentially as `stock_wolf_2219_ingestion`. Its two role/path tests and
the full 308-test local suite pass; no ingestion runtime pass is implied.
