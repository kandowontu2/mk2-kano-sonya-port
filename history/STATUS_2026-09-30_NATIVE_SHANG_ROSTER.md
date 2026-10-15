# Native roster current test candidate — not a complete release

Current test candidate is `diagnostic_v635_native_shadow_rows`.

Current 2026-10-02 update:252 fresh roster-wide human move fixtures,52 fresh
positive/block/miss fixtures, ten startup interruption/retry cases and four
KO/next-round cases pass on unchanged v635.54 corresponding regression tests
pass. Fresh all-nine-arena replay in BOTH slots matches1218 actual samples;
v658 pins full runtime artifacts and passes eight replay-boundary tests.
The five native crouching-turn roll contacts have a bounded RETAIN decision
based on actual original exposed sprite pixels; nine fit tests pass at v659.
Broader CPU/held-pose/rendered move/cinematic/audio/tower/finisher/ending and
release acceptance remain open. Full-port acceptance is false. See
STATUS_2026-10-02_CURRENT_GAMEPLAY.md; older summaries below are historical.

Latest v645: all four cold Kano/Sonya-vs-Kitana idle/mobility cases match the
stock sole/contact line in either player slot. All148 drawing passes match
actual VRAM/PNGs. Both new49,237-field P2 campaigns reach all nine regular
arenas with609 exact native screen reconstructions and271,271 verified
imported shadow copies. 71 tests pass. These are genuine losses/paid continues,
not tower clears. No game source/executable/payload/launcher was changed or
additional height offset applied. Wider P1/mirror/secret-stage grounding and
full gameplay/release acceptance remain open; v645 NOTES.md has full scope.

The original MK2 floor-shadow routine now reads the actual imported row data;
the custom whole-body projection is removed. v640 verifies 1,654 components,
43,197 native row copies and 54 fixed Dead Pool frames across both fighters/
slots/mirrors (14,155,776 VRAM words and 5,486,400 screen pixels, zero mismatch).
All four current CSS/ladder/first-match UI cases and 60 UI/row corruption tests
pass. Latest-test CMD selects v635; production v277/release ZIP v258 unchanged.
All-arena grounding, current Pit/gameplay paths and full-port acceptance remain
unproven. The original gameplay payload/driver/audio are unchanged, but native
shadow DMA busy timing is now real. Historical v602 reports below remain scoped
to that build. Its three changed live source inputs are preserved exactly in
audit_v634_pre_native_shadow_sources. Full current details and remaining work
are in STATUS_2026-10-01_FLOOR_SHADOWS.md.

Historical v602/v623/v631 floor checkpoint: both actual P2 campaigns naturally cover
all nine regular arenas with607 retained floor screenshots and unchanged
full gameplay timelines. Fifteen moving Sonya frames first prove the actual
native front-buffer binding, not a selected best buffer. Fresh P2 Dead Pool
samples then independently reconstruct all DMA/scenery/foreground/body and
projected-shadow writes from actual BEFORE-pass VRAM to the tested flip.
All7,864,320 indexed VRAM words and3,048,000 displayed pixels match in thirty
samples, including14,050 visible imported shadow pixels. v631 passes17
baseline/corruption tests with1,512 rechecked inputs; both screenshots viewed.
This is runtime copy/projection proof, NOT desired native-style geometry or
grounding, earlier inter-pass erasure, all-arena/P1/secret-arena acceptance.
Those remain open. v629 retains rejected models/disassembly/test boundaries;
no gameplay/source/ROM/executable/CMD/ZIP was changed. Five earlier audit
manifests were rechecked with zero changed inputs. Full acceptance is FALSE.
See STATUS_2026-10-01_FLOOR_SHADOWS.md for exact scope and next requirements.

Prior v617 checkpoint: both physical slots and actual P2 mirror victims now
complete native Pit scenes and genuine paid continues. Six real captures
cover seven episodes (including two in the Kano mirror run), no resets and
no guest-state assistance. Both mirror runs retain their prior full-run
input/health/fight/state chronology. Actual original constructor arguments
and full65-color reads prove native NORMAL-palette reconstruction even after
an alternate mirror costume, not a new costume bug or proxy.
87 asset/slot/mirror/raster baseline/corruption tests pass with1,757 rechecked
inputs;133 fixed-phase fall rasters match all675,841 opaque body pixels.
P1 mirrors, impact/shake/foreground/audio, five roll contacts, broader combat/
floor coverage and whole-game acceptance remain open. v602 gameplay/CMD/ZIP
unchanged; final production packaging is still pending.

Latest v605/v607/v609 checkpoint: dedicated true-ID Kano/Sonya Pit falling and
impact sequences plus own centered constructor coordinates are installed.
Both fresh unassisted P1 victims complete the native scene, pay a continue and
enter another actual own-ID fight, without the former reset. 43 Pit asset/state
tests, four fresh UI flows with 46 regression checks, and sixteen positive
human special-move command/contact/recovery cases (all eight moves, both slots)
pass. Latest-test CMD opens v602 and actually verifies one good ROM set.
Production CMD/ZIP remain unchanged; full integration is not achieved.
At that earlier checkpoint, other-slot/alternate Pit, five roll contacts, wider combat/floor coverage and
whole campaigns/finishers/endings/audio remain open. See the top checkpoint
in STATUS_2026-10-01_FLOOR_SHADOWS.md for exact evidence and retained failures.

Historical v545 findings follow (not the current v602 tested P1 Pit result):

Latest v594 finding: a genuine CPU Pit II fatality against Kano P1 resets the
unchanged candidate after six paid continues. Runtime/native instruction taps
prove its ID17 cinematic table lookup returns1 at16784; at16785 the original
sprite copier overruns both health globals and other gameplay RAM. The actual
reset vector is fetched at16955. Both scene operands still use FF85E6B0's
twelve-fighter falling-art table. Sonya's slot18 is also unextended and aliases
the original Kung Lao stream; her Pit execution was not observed. The new
16-test/243-input checkpoint proves the defect, explicitly NOT a fix or full
acceptance. Source/payload/executable/launchers/ZIP remain unchanged. Dedicated
own front-facing falling/impact art and both native table extensions are needed;
ordinary side-view knockdowns are not an equivalent substitute. See the latest
section of STATUS_2026-10-01_FLOOR_SHADOWS.md for exact capture/checker scope.

v552 verifies the one-pixel native roll-plane fit, Liu duck misses both slots,
unchanged 24/5 damage/recoil, 52 fresh human move cases, four full rendered UI/
ladder/first-match flows and 67 regression tests. Of 28 duck-roster captures,
23 misses pass; Kitana/Mileena both sides and Raiden P1 remain unresolved native
contacts. Root latest-test CMD now calls v545 and actually verifies its ROMs
(v553). Production CMD/ZIP remain unchanged; full integration remains false.
Fresh v545 v556 CPU dispatch/ring checks pass 47 tests; v559's ten interruption/
retry and four KO/next-round cases pass 30 tests. v565 verifies four full natural
CPU grabs through every held pose, native damage/flight and individual owning
ready cleanup, with 63 tests and 528 pinned inputs. Actual post-cleanup action
stores and live operands distinguish a legitimate NEW ordinary attack from
residual grab locks. v569 now proves three fresh complete special MISS
follow-ups: bicycle against Sonya, square-wave against Sub-Zero and blade
against Liu, for seven full natural grab cases and 178 tests/640 inputs. Earlier
v565 labels square/native-jump were incorrect; original entry addresses prove
bicycle/square-wave. The no-choke scout is still not a completed-grab proof.
v573 passes 220 combined tests/764 inputs, adding exact native-cache/DMA/palette
bindings and 81,122 visible-body pixel comparisons across 16 consecutive frames.
The initially suspected upside-down human block was misidentified: normal green
is P1 CPU finishing bicycle; alternate white is P2 human blocking upright.
No persistent inverted human block is proved here. This bounded display check
is not universal animation/game acceptance. No gameplay/build/launcher/ZIP
changed. See the current status
file also for v576's six fresh crouching-turn roll diagnostics: original stock
turn poses, actual ROM/cache components, first positive overlaps, five native24
contacts with complete rebound/controls and one separating-axis miss. It passes
255 combined tests/983 inputs/92 comparison images, but explicitly does NOT
approve the five contacts' authored fitting or claim a roll fix. All earlier
real input/gameplay evidence remains unchanged. See the current status
file for exact scopes and preserved checker failures. The v517 checks below
remain historical, not automatically current after the operand change.
The latest v580 checkpoint adds four fresh full P2-CPU/P1-human grabs (Kano
mirror; Sonya against Sonya/Kano/Cage), including one complete bicycle MISS
and three original ordinary next-action state/lock cleanup ledgers. It passes
403 combined actual tests with 1,344 inputs and independent physical-slot
bindings plus continuing native health ledgers. All 983 v576 inputs remain
unchanged. Eleven other scouts remain unaccepted as full-grab/follow-up proof;
CPU choices, IDs, HP, stage and RNG were not injected. No gameplay/build/CMD/
ZIP changed. See the current status for exact scopes and v579 checker failures.
See `STATUS_2026-10-01_FLOOR_SHADOWS.md` for current shadow verification and
remaining acceptance work. Current v519 verifies nine cannonball flight/rebound
cases but retains the Liu P1 crouch-contact counterexample; full acceptance is
false. Current v521 checks four Sonya ring/leg cases with actual ID18 in both slots.
The historical v479 audit covers continued Courtyard
palette/shadow correction, not fresh universal UI/campaign acceptance.
Fresh current v524 now covers 52 human positive/defensive cases; v526 covers
ten startup interruptions/retries and four KO/next-round cases; v529 covers
both characters in both selection/ladder/first-match slots, including actual
rendered borders/numbers/backdrops/cleanup/icons/name shadows. See the current
status file for bounded scope and retained checker failures. Root
`PLAY_LATEST_TEST_BUILD.cmd` launches v517 and passes actual ROM verification;
the older production CMD and ZIP are unchanged. Full acceptance remains false.
Current v539 observes all eight natural CPU routes, with four P2 CPU ownership/
recovery cases and two P1 Sonya ring block/duck cases: 47 tests, 399 pinned inputs.
The fresh knife cancellation trace proves original native hurt-list replacement
after damage while its already-created child completes; it is not an arbitrary
damage bypass. Full CPU contact/victim/slot/KO/art/audio/tower acceptance remains
open. v533's earlier diagnostic and v537/v538 checker failures are retained.
v542 pins exact paired crossover bounds/images for the unresolved Liu P1 duck
contact; four additional original donor spacing variations still miss in v544.
No gameplay build, production CMD or release ZIP changed in this checkpoint.
v517 changes only cannonball flight/rebound emission from v500; payload and
rendering are unchanged. The v400
executable and v425 checks below are historical, not current full acceptance.

Historical v484 additionally checks all eight human special commands, native
contacts/ready and ordinary follow-up from both slots: 18 real-input cases,
12,838 paired fields, 174 checked inputs and 18 reference/corruption tests.
Standing square-wave misses and genuine airborne hits are distinguished.
This closes the positive current-build activation matrix, not full native
choreography, all victims/interruptions/CPU/campaign/finishers/audio acceptance.
See the current status file above for exact evidence and retained failed checks.

- Historical v400 executable SHA256: `822CD6BC358854162A4769A9D6C09923D737ADA025201B64B6521988DF9837F6`
- Current `midtunit_m.cpp` SHA256: `B8542F4777E4F100EC4E86771AD70EC867522FE106DD51E6F164E408489722D3`
- Payload remains `82FE153FB56B46A6F9D42F493451AC3D59AD61713433714ACA7704E2881F8951`.

## v425 current native selection/ladder/first-match presentation (1 October 2026)

Current v400 game source, executable and payload unchanged. Four fresh, standalone
real-input campaign launches cover Kano and Sonya in BOTH human player slots.
Each repeatedly visits its adjacent stock cell, returns without skipping it,
uses the native down/up neighbors and commits the correct actual character.
The complete original twelve portrait records and seventeen stock ladder records
remain unchanged, with actual added entries for IDs 17/18 rather than Liu proxies.

Independent native-size image checks prove:

- Both unselected full top-row portraits equal the UI-source raster pixel-for-pixel,
  without persistent player numbers or colored selection hints.
- All four 4-pixel border segments and their blink colors equal phase-matched
  stock controls. Full original player-number masks/placement match in both
  slots: 66 pixels for P1 and 84 for P2; 34 cursor sample pairs in total.
- Selected native stances animate while the cursor blinks. Backdrop comparison
  finds zero X/Y shift against stock, with a large separation from +/-1/2 pixels.
- Every post-exit field lacks the old full-size portrait signatures. Captures
  from the first transition onward lack normal/dimmed icons and all distinct
  observed idle/confirmed locked poses. The native ladder reveal contains BOTH
  complete 35x45 UI-source icons, verified pixel-for-pixel in each launch.
- Every initial-match participant field retains actual ID/roster/controller/
  actor/Main ownership; the selected Kano/Sonya never becomes Liu. Thirty-two
  repeated name-face/shadow captures preserve the stock dark-maroon shadow pen.

`audit_v425_native_ui_flow_checked_inputs/result.json`: 46 new checks and 237
earlier current checks pass (283 total), 801 inputs frozen. Four traces contain
1,424 selection fields, 2,836 post-selection fields and 1,448 actual first-match
participant fields. All 136 v422, 357 v418, 184 v413 and 522 v409 inputs unchanged.
Injected visual regressions for the reported missing/thin/shifted/frozen/lingering
UI defects are rejected. The initial v423 Lua syntax failure and its original
source remain preserved/rejected; corrected v424 is a separate capture version.

These are first campaign transitions, not whole tower/continue/ending or every
ground-shadow/arena, move, victim, interruption/KO or audio acceptance. Those
remain required, followed by the final matching launcher and release ZIP.
Production CMD remains v277 and ZIP v258; no build/promotion in this checkpoint.

## v422 natural CPU knife/ring follow-ups (1 October 2026)

Source, build and payload still match v400. Three current, cold P2-only real-input
campaign captures now pass independent CPU projectile checks, without supplying
CPU choices, guest state, health, positions or RNG results:

- Kano mirror: original AI requests actual index 22; real Kano launches the
  knife. All 25 release/24 recovery fields, six stopped intro poses, full ten-pose
  flight cycle plus repeat, six four-field stopped impact poses, actual six-chip
  damage, child retirement and individual Main cleanup/ready/walk are verified.
- Sonya/Cage block: original index 23 selects the ring; all 15 release/35 recovery
  fields, short three-field flight holds, seven moving four-field burst poses,
  actual six-chip damage and both body/child cleanup pass. Contact occurs before
  the other two flight poses; this case does NOT prove a complete flight cycle.
- Sonya/Cage duck: genuine P2 Down after actual release; all four flight poses
  and repeat, every eight-pixel field, no impact/damage, original child retirement
  and full body cleanup/walk pass. The observer does not establish the precise
  bounds decision that causes retirement.

The independent verifier compares actual compiled release/create/variety programs
against the source-authored instruction model, and checks every published actual
actor/Main/controller/roster, typed native state/lock/health store and child field.
Ten clean native 2.5-pixel walk fields follow each individual CPU ready handoff.
Native guard checks flag bit zero: Cage can block while finishing get-up, before
the standing-block graphic/action 0700. Do not impose Kano's 0700 on that stock path.

`audit_v422_cpu_projectile_followup_checked_inputs/result.json`: 77 new tests
(including corrupted-trace/instruction/cleanup-order rejections) and 160 previous
current tests pass, 237 total. 136 inputs frozen; all 357 v418, 184 v413 and 522
v409 manifest inputs remain unchanged. Raw v419 duplicate-coordinate traces and
the v420 Kano no-knife trace remain preserved/rejected, not retroactively edited.
Representative native-size projectile/recovery images inspected; no exhaustive
collision rectangles, bootstrap visibility, pixels, audio or floor-shadow claim.

Next: broader natural CPU moves/victims/misses/interruptions/KO/both CPU slots;
complete current selection/ladder/tower/continue/finishers/art/audio/ground-shadow
acceptance; then matching final CMD/ZIP. Production remains v277, ZIP v258.

## v418 original Kano CPU roundhouse continuations (1 October 2026)

Current source, executable and payload remain v400. The longer actual Kano
trace resolves the previously unproven continuation after choke: this is
the ORIGINAL CPU roundhouse routine, not a delayed action assignment. Native
`FF9B9470` deliberately animates through `FF83C340`, skipping `FF83C320`'s
action-word store. Its old `0303` word therefore remains throughout the kick;
new body/Main locks come from original setup and are actually cleared afterward.
No artificial action write, identity proxy or gameplay change was introduced.

The current input-only cold Kano mirror repeats the full 70-held-field choke,
32 damage and both individual original cleanup/ready handoffs. Three ensuing
roundhouses now pass all native authored pose/loop/terminator fields (37,37,45),
actual attack-count/delay changes, original chip-health stores (6,6,9), original
early/late miss return branches and each owning Main's actual cleanup/handoff.
The first clean walk keeps Kano's native 2.5-pixel forward speed and five-field
cadence. A fresh original Baraka/Sonya roundhouse control passes the same native
37-field ordering and six chip damage, returning to its original three-pixel
forward walk. No CPU choices, health, ID, stage or positions are supplied.
The later blocked choke attempt is NOT claimed as another complete paired hold.

`audit_v418_cpu_roundhouse_recovery_checked_inputs/result.json`: 49 new and 111
prior current checks pass (160 total), 357 inputs frozen; all 184 v413 and 522
v409 inputs revalidated unchanged. Prior short traces stay short, not silently
upgraded to full recovery. Representative current native-size follow-up art was
inspected; this is not exhaustive pixels/audio/ground-shadow/whole-UI acceptance.

C: became full during one new capture. That incomplete v416 log/frozen launch
sources remain rejected and preserved. Only the project's regenerable compiler
cache `mame-mkp/build/mingw-gcc/obj/x64/Release/emu.h.gch` was removed (212,885,742
bytes, 203 MiB); no active compiler or frozen manifest referenced it. Source,
assets, ROMs, executables and saved evidence were retained. A corrected observer
extends stock health provenance; fresh v417 launches are terminal and matched.

Next: both CPU projectile continuations, wider natural CPU/KO and complete current
UI/ladder/tower/finisher/art/audio acceptance, then matched launcher/ZIP delivery.
Production CMD remains v277, ZIP v258. No game change, rebuild or promotion here.

## Historical v413 original Sonya CPU uppercut continuation (1 October 2026)

Game source, executable and payload remain v400. The prior unresolved Sonya
CPU walk `0303` -> uppercut `0106` is now proved as a NEW original action,
not lingering leg-grab locks. The original CPU setup writes body/Main locks
while the old walk action is still present, THEN writes `0106` in that same
field. Demanding `0106` in the earlier pre-write lock record was incorrect.
The old verifier and its rejected raw traces were preserved unchanged.

The fresh Sonya/Cage case proves all 46 held leg-grab fields, 35 damage,
both actual owning Main cleanup stores/ready handoffs, every intervening clear
walk field, the ordered original uppercut setup/action stores, all 21 attack
and 12 recovery pose fields, action `0600` -> zero, original lock cleanup and
subsequent clear walk through the terminal observation. An input-only stock
Baraka/Sonya control proves the same original action/recovery/store ordering
and cadence. Real P2 Block input keeps that control out of KO; neither CPU
choices nor health, IDs, positions or stages are supplied by the observer.

The new Kano mirror regression retains its full 70-held-field choke, 32 damage
and both individual cleanup handoffs. It starts another original action setup
while its walk state is still `0303`; this bounded observer ends before the
next action-word store. That later Kano action/recovery remains UNPROVEN, not
silently accepted as equivalent to the Sonya uppercut continuation.

`audit_v413_cpu_action_recovery_checked_inputs/result.json` freezes 184 inputs
and revalidates all 522 v409 inputs unchanged. All 49 new tests and 62 current
human/CPU-air regression tests pass (111 current checks). The 63-test frozen
historical suite still has one expected current-source-guard rejection: its
v379/v357 launch does not match current v400 source. Its full failure output
is preserved, not called a green current-build suite. The first unblocked
stock cut reaches KO without the observed cleanup and remains an incomplete
control; it was not relabelled full recovery.

Next: Kano's delayed next-action state/cleanup, both CPU projectile follow-ups,
wider natural CPU/KO cases, and full current UI/ladder/tower/finisher/art/audio
acceptance. Production CMD stays v277 and ZIP v258. No game code change,
release promotion, new build directory or further cleanup in this pass.

## Historical v409 current human air-height and original Jax controls (1 October 2026)

Current game code/build/payload remain v400, unchanged from v404. The height
correction now has fresh input-only human coverage: actual Kano/Sonya matches
in both attacker slots, with Block delayed eight or twenty fields after the
ordinary jump input. The actual catches occur at Y=32 and Y=-13 (floor=82):
50 and 95 pixels above the floor, not an imposed fixed height.

All four declared catches pass every 26-field Kano held-pose sequence at the
actual catch coordinate, the complete 41,-3 fixed-point grip, victim flight
and native rebound, one original 16-point health store, each actual owning
Main's clear/stopped/grounded ready entry, and its original body/Main cleanup
stores. Both fighters subsequently walk, perform the entire original 38-field
jump with the throw callback cleared, punch, block and return to clean control.
Sampled native selection/display and added-name shadow checks pass too; these
are not full current UI/ladder/bitmap/audio or post-ending acceptance.

Two fresh original Jax/Sub-Zero controls, one per attacker slot, pass the same
ownership/cleanup/recovery and ordinary-control requirements. Jax keeps the
original +32 downward movement, own falling phase, 58 owned throw-pose fields,
late victim release, original flight without Kano's callback/rebound, 32 damage,
64-field own recovery and original victim get-up. No Jax identity is substituted.

`audit_v409_human_air_height_checked_inputs/result.json` passes 28 new tests
plus the unchanged 34 current CPU tests (62 total), freezes 522 inputs and
revalidates all 484 v404 inputs unchanged. Six full cases contain 3,313 native
match fields. This is narrower than all victims, heights, interruptions, KO,
CPU Jax, artwork/audio or the entire natural-integration objective.

Earlier traces remain rejected as full catch/follow-up cases: the two-field
Block command reached its gate while grounded, then both ordinary jumps
completed with no damage; it is not a successful air catch. The first stock
fixtures incorrectly applied a Kano/Sonya-only HUD-shadow assertion to
Jax/Sub-Zero (zero applicable checks). Later inward-walking stock controls
triggered a legitimate close-range clinch rather than ordinary punch/block.
The current stock fixture instead walks outward using real inputs and checks
the original two-pixel backward-walk parameter. Neither old result was erased
or silently accepted as a complete normal-control case.

Native-size screenshots were inspected for representative held/flight poses,
not exhaustively compared against every original bitmap. Sonya's v402 CPU
walk `0303` -> punch `0106` ownership transition remains unresolved/rejected.
That and broader current whole-game QA are next. Production CMD stays v277,
ZIP v258; no release promotion or further cleanup was performed in this turn.

## Historical v404 natural CPU air throws and actual catch height

Kano's real-ID native LP/HP counter wrappers now have a 250/1000 native
chance to jump toward an airborne opponent within 96 pixels. Original RNG,
forward-jump movement and the per-field catch callback perform the choice and
catch; observers supply only actual P2 coin/start/selection/movement inputs.
Stock identities bypass the new chance call and keep their original counters.
Kano additionally checks that the opponent remains airborne at the catch gate.
Jax retains the original gate, arguments and fallback. No identity is aliased.

Live v398 catches exposed a real low-height bug: Jax's shared action shifted
Kano down 32 pixels and buried the held victim below the floor. Original MK3
Kano does not use that shift. v400 makes its height helper zero that movement
for actual Kano only, preserving Jax's original 32 and the other arguments.
This affects human catches too: their historical floor-minus-63 test is no
longer the right height expectation. At this checkpoint fresh human
both-slot/height and actual stock Jax end-to-end tests were still required;
the bounded current v409 cases above now provide those declared controls.

`audit_v404_cpu_air_runtime_checked_inputs/result.json` passes 34 new checks,
freezes 484 inputs and revalidates 4,655 unchanged historical inputs. Six prior
manifests' driver source changes are recorded explicitly, not called unchanged.
The compiled decoder exercises 460 counter/guard branches and 19 height routes.
Every other v357 build input and its morph payload remain identical.

Two current input-only P1 CPU catches pass independently: Kano/Kano and
Kano/Sonya, 65 paired fields each. Each includes all 26 owned held poses at
the actual airborne catch height, the 41,-3 fixed-point grip, 31 victim flight
callbacks through release and rebound, one native 16-point damage store, and
each actual owning Main's first clear/stopped/grounded post-cleanup ready entry.
The victim completes the native 24-field get-up. This observer does not prove
individual cleanup stores or all pixels/audio. The additional Sonya Y-store
control confirms the original `FF83D2F0` floor-word clamp, not a waived physics
error: it retains the fractional Y while restoring the integer floor at impact.

A fresh v400 Kano choke regression passes its complete native pair. A fresh
Sonya/Cage leg-grab trace has clear individual native cleanup and recovery but
FAILS the full verifier's later CPU action ownership check: original lock
setup occurs under walk `0303`, while completion observes punch `0106`.
It remains rejected; do not weaken the check or describe both close cases as
passing. That native action transition needs additional provenance.

Earlier projectile scouts, v396's missing guard NOP (executed `FFFF` word 15),
and v398's incorrect low height remain preserved, not promoted. Production
CMD still launches v277; release ZIP remains v258; generic emulator unchanged.
All broader evidence below is historical, not a full current-v400 regression.
The whole natural integration goal remains unfinished.

## Historical v390 CPU airborne eligibility checkpoint

The original CPU forward-jump callback at `FF9BEEF0` recognized only Jax (11),
so Kano (17) could not enter its native catch eligibility checks. v388 includes
his real identity without proxy substitution. Its router lives at `FFFC8700`;
stock opponent-state checks, both 0x60 gap checks, action and stack unwind
remain byte-identical. Jax keeps that path; every other identity, including
Sonya, retains the original ordinary jump-attack fallback.

`audit_v390_cpu_air_gate_checked_inputs/result.json` passes 15 new tests and
freezes 225 inputs. Actual compiled ROM dumps are independently decoded for
all 19 identity routes. Two input-only scouts contain 1,905 native gameplay
fields, but neither reaches the airborne callback or catch. This is compiled
routing proof, NOT a completed natural CPU air throw or stock Jax air-throw
control. Those end-to-end checks remain open.

Two fresh v388 natural P1-CPU/P2-human close regressions pass full individual
native recovery: Kano/Kano cycle 3 and Sonya/Cage cycle 2, with 236 paired
callbacks, 116 held fields and 46 victim-flight fields. The same schema-4
original cleanup/ready, grips, poses, damage and flight checks are retained.

The audit revalidates 4,431 unchanged historical inputs. Five prior manifests
point at the intentionally changed driver source; that explicit old-to-new
hash transition is recorded, not called unchanged. Other build inputs and
payload match v357. Older v357 evidence below is historical and is NOT being
relabelled as a full current-v388 regression pass.

v382/v385 compiler failures, v383's rejected overlapping allocation and v386's
incorrect short-branch target are preserved. v387's no-catch scouts do not
accept that incorrect router; the independent decoder rejects its word-10
landing. Production CMD remains v277, release ZIP v258 and generic emulator
unchanged. Whole natural integration is still incomplete.

## Historical v357 matched candidate

- Historical executable SHA256: `4E71EFACF4837B6D32A3FF92BBE9A28B6D56C2AEFD68E165D35D6D14D95383AD`
- Payload SHA256: `82FE153FB56B46A6F9D42F493451AC3D59AD61713433714ACA7704E2881F8951`
- Historical `midtunit_m.cpp` SHA256: `410C682822A858AE20328B09C1DEC3EA2887CDEF0C37D8DB7853725E36F3F7C9`
- Current `tms34010.cpp` SHA256: `87B5F2953B374D890CC97F041AA450D8E89DAC735C8299BF40F3E491E7E94AEF`

Production `PLAY_MK2_KANO_SONYA.cmd` still launches v277. The old release ZIP
is still v258. Neither was promoted to this candidate. The installed generic
emulator was restored after each build. No old failures or proofs were deleted.

## Historical v357 morph palette and repeated-cycle proof

Native transition palettes `FF0C0800` / `FF0C1000` fell inside the old imported
frame-descriptor compatibility range. At `FF80D3C0` the CPU compatibility hook
substituted Shang's ordinary colors on the way in and the current added fighter's
ordinary colors on the way out. Correct native palette-entry arguments did not
prove the colors actually copied to palette RAM or displayed. v357 exempts only
those two genuine native palette records in both CPU execution paths. Existing
imported-frame compatibility, alternate outfits and native timers are retained.
The build helper now hashes the CPU core source/header as well as driver inputs.

`audit_v358_fixed_morph_render_{kano,sonya}_p{1,2}` uses actual human commands,
native 400x254 snapshots and read-only component/DMA/palette observations. The
independent checker decodes original MK3 transition/body art and original MKII
restored-Shang art. Every four-field transition hold in both directions and the
first eight own-body/restored-body fields match at the fixed native two-field
display-buffer delay. All 320 component bitmap checks pass, including Kano's
legitimate alternate outfit against the other Kano. This does not prove every
game bitmap or every later animation frame.

`audit_v359_palette_fix_cpu_{kano,sonya}` contains two complete native random
morph cycles each: Kano 545 + 645 form fields, Sonya 526 + 630. All four cycles
have their own original forward/reverse stores, transition groups, timer,
ownership and 120 consecutive restored-Shang fields. Sonya actually performs
leg actions and finite native turning in the first cycle; the second does not
randomly choose that move. Leg/turn coverage is required across the fixture,
and every observed leg cycle checks its subsequent turn. A later stock morph
is required after the first restoration, not after every random repeat. These
CPU fixtures explicitly assist stage selection and P1 health, not morph choice.

Six current stock human morph cases (`audit_v360_palette_fix_*`) and four
current input-only blocked knife/ring render cases (`audit_v361_palette_fix_*`)
also pass. The stock targets are actual IDs 2, 3 and 4: Johnny Cage, Baraka and
Kitana. Earlier prose incorrectly called IDs 2/3 Raiden/Sub-Zero; the traces
and native-ID checks were unchanged, and no game identity was renamed.

`audit_v363_morph_palette_checked_inputs/result.json` freezes 1,969 exact
inputs and passes 132 reference/mutation tests. Its scope is four human morph
render cases (96 transition fields, 32 forward and 32 restored handoff fields),
six stock morph cases, four assisted CPU cycles (2,346 form / 480 restored
fields), and four unassisted blocked knife/ring cases (1,566 native component
draws / 332 bitmap samples). It does not relabel historical v345 evidence as
full current-build integration.

## Historical v357 stock projectile reaction regressions

`audit_v364_stock_reaction_*` tests Sub-Zero freeze and Raiden lightning hitting
Kano and Sonya in both human player slots, plus two original Johnny Cage P1
controls. Every case starts through actual selection and uses only controls,
without cheats, health, coordinate or identity assistance. All 1,301 fields per
case retain published actual actors/Main processes, IDs and human ownership.
Each case has four original native contact/health stores and original ready
returns. Freeze stores zero damage and lightning 22, as in the stock control.
Actual opaque RGB555 palette RAM matches original owned blue colors during
each reaction and original normal colors after recovery; cached normal palettes
need not enqueue another palette copy. Walking, jumping, punching and clean
grounded final control are independently checked afterward.

`audit_v365_stock_reaction_checked_inputs/result.json` passes 28 new mutation
tests and all ten cases, freezes 414 inputs and revalidates all 1,969 inputs of
v363. Owned coverage is 10,408 fields / 32 contacts; stock controls add 2,602
fields / eight contacts. Added-character display/name-shadow/stability checks
also pass. The old custom-name helper reports false with zero custom-name
checks for stock Cage; those checks are explicitly inapplicable, not claimed
as passing custom-name evidence. The independent stock reaction checks pass.
This is not all stock projectile types, hit/block/miss variants, every rendered
bitmap, audio, post-ending reaction coverage or an unassisted tower.

## Historical v357 natural CPU paired-contact proof

`audit_v372_natural_cpu_pair_checked_inputs/result.json` independently passes
five current v357 natural P2-CPU/P1-human cases: Sonya against Sonya, Kano and
stock Liu Kang, and Kano against Sonya and Liu Kang. These contain three full
leg grabs and two full chokes, with 596 consecutive paired callback fields,
278 original-derived held-pose fields and 116 victim-flight fields. Original
descriptor consumers, real actor/Main ownership, every held pose and grip,
damage stores (35 for legs, four eight-point choke squeezes), native release,
fixed-point flight and both native ready/grounded recoveries are checked.
Sonya's mirror case includes her legitimate alternate outfit. Human approach
uses real controls; CPU choices, IDs, health, stage and positions are not
injected. No guest-state assistance or game-code change was made for this audit.

The audit passes 35 new CPU reference/mutation tests and 35 historical human
pair-reference tests, freezes 435 exact inputs and revalidates all 2,383 inputs
from v363/v365. Historical reference tests are not current-build human restart
proof. Liu's inherited custom-name helper has zero applicable new-name checks;
its false summary is not claimed as passing custom-name evidence. Only each
declared uninterrupted completed cycle is accepted; earlier or later misses,
interruptions and extra entries are not silently counted as complete pairs.

v366 observer Lua errors, v367-v369 ambiguous duplicate-field logs and v370
missing data-descriptor provenance remain preserved and rejected. The observer
and independent checker were corrected, not the game's RNG or move behavior.
Scouts without a requested catch are not proof of a gameplay softlock. Native
snapshots were inspected, but this audit is not exact all-frame bitmap/audio
acceptance, every victim, P1 CPU, CPU air throws or interrupted/KO pair coverage.
Production CMD, release ZIP and installed generic emulator remain unchanged.

## Historical v357 opposite-order CPU paired-contact proof

`audit_v377_natural_p1_cpu_pair_checked_inputs/result.json` passes seven natural
P1-CPU/P2-human cases on the unchanged v357 candidate. The observer cold-starts
P2 alone using actual coin/start and character-selection inputs; it does not
join two humans, force a loss or write a replacement CPU identity. All selected
human identities hold through selection without errors, and first opponents
come from stage zero of the original-derived native ladder orders.

Accepted cases are Sonya against Sonya twice, Kano, Liu Kang and Sub-Zero, and
Kano against Sonya and Liu Kang. Five complete leg grabs and two chokes check
824 consecutive paired callbacks, 370 original held-pose fields and 162 victim
flight fields. Native descriptor-consumer PCs, true Main/actor ownership,
every pose/grip/shake, original damage, correct P2 velocity slot, complete
fixed-point flight and both native ready/grounded recoveries pass. Alternate
Sonya mirror art and Kano choking original Liu were visually inspected. This
is not all-frame bitmap, all UI, audio or all-victim acceptance.

The audit passes 52 new P1-CPU reference/mutation tests, 35 prior current P2-CPU
checks and 35 historical human pair-reference tests: 122 total. It freezes
1,107 inputs and revalidates all 2,818 prior v363/v365/v372 inputs. The initial
velocity mutation affected a startup stop instead of the final fling; the
checker now requires every actual victim velocity request to target P2, not
merely one matching release request. No native game code/build/payload changed.

Sixteen unaccepted v373-v376 scouts are frozen separately. Some start against
stock opponents or reach KO/another attack without the required clean paired
completion. Input-only recovered backsteps were tried, not forced positions or
CPU decisions. v376 Sonya/Cage records a completion after 347 fields but fails
the current under-300-field completion gate; it is not silently promoted. The
meaning of native guard/follow-up states and that timing gate needs further
investigation. These findings are not proof of a gameplay softlock and do not
establish every interrupted/KO pair as correct. Earlier/later entries remain
explicitly outside each accepted uninterrupted completed-cycle proof.

Production CMD remains v277, old ZIP v258 and installed generic emulator
unchanged. Current CPU close-contact evidence now exists in both player orders,
but the original full natural-integration objective remains unfinished.

## Historical v357 original individual ready handoffs and CPU follow-up

`audit_v380_native_cpu_recovery_checked_inputs/result.json` adds two full
natural P1-CPU/P2-human cases on unchanged v357: Kano choking Kano (cycle 3)
and Sonya grabbing original Cage (cycle 2). Both pass every original held pose,
grip, damage and flight check: 236 paired callbacks, 116 held fields and 46
flight fields. Earlier interrupted/re-hit/KO cycles are not counted complete.

The v378 read-only flag provenance narrowed the old failed cleanup gate: both
added CPUs and an original Baraka control use original body-lock setup
`FF838CD0` / Main-lock setup `FF877D30`, then original cleanup stores
`FF83EE90` / `FF83EFA0`. The observed post-store PCs are respectively
`FF838CF0`, `FF877D50`, `FF83EEB0` and `FF83EFC0`. CPU lock flags can be cleared
at its own ready return and set again for another action before the victim gets
up. A later busy field therefore does not by itself prove failed pair cleanup.
Nine complete original Baraka setup/cleanup cycles independently pass as a
generic native action-lock control, not as full stock-move/KO acceptance.

The new schema-4 observer records each actual owning Main at original
`FF861500`, after the original ready entry and cleanup calls. The checker
requires both actual handoffs: stopped, grounded, action zero, body/Main flags
cleared and trail detached, with actual original cleanup-store effects and
owner PCs in the same field. Kano's complete own recovery takes 13 fields from
release; Sonya's takes nine. Any later CPU busy state must have NEW original
body/Main action-lock setup under the same true actor/Main after its clean
handoff. This does not waive residual pair locks. Native code and bytes were
checked against the original MKII image; no gameplay change was made.

These are separate individual-handoff proofs, not relabeled simultaneous-idle
proofs. The old simultaneous-clean verifier and failed/incomplete traces remain
unchanged; the under-300-field bound is retained. New complete callbacks follow
the two real handoffs immediately (127 and 109 fields), rather than waiting for
a coincidental later clean pose. v379 Sub-Zero KO remains unaccepted as living
recovery. v379 Kano/Sonya's later knife changes native Main action from `0x117`
to `0x618`; its follow-up state-transition provenance is not yet checked and
the new checker rejects it, rather than exempting the mismatch.

All 185 tests pass: 63 new native recovery/control checks, 52 prior P1-CPU,
35 prior P2-CPU and 35 historical human pair-reference tests. v380 freezes 511
inputs and revalidates 3,925 prior inputs. Inspected mirror recovery and Cage
grip snapshots are not exact all-frame/art/audio acceptance. Current source,
candidate, payload, production CMD, old ZIP and generic emulator are unchanged.
The original full natural-integration objective remains incomplete.

## Native implementation

The original CPU morph uses the game's RNG with fourteen choices. The original
Shang-to-Mileena remapping is retained; the added outcomes are actual IDs 17
and 18, not renamed stock actors. A scoped forward lookup returns each added
fighter's own morph sequence without overwriting Shang's existing animation
slots 17/18. A separate reverse lookup selects the same own sequence for the
original native reverse routine. Actual identity, body palette, floor, elapsed
timer, scheduling and return-to-Shang stores remain game instructions.

The asset-only v323 payload adds the original three two-part MK3 transitions
for each fighter, preserving all twelve components' pixels, dimensions, pivots
and opaque RGB555 colors. The scripts use MKII's original palette callback,
native four-field holds and the fighter's own canonical stance group. Source
v300 payload bytes outside the reserved morph allocation are unchanged.

The failed Sonya restoration was narrowed to a missed CPU table consumer,
not established leg-grab memory corruption. The human turn lookup already used
the extended table, but CPU `FF9B5390` still pointed to `FF8702C0`. Its 17 rows
end just before `FF8704E0` code: ID 17 reads `76C00D3F`, ID 18 `000D09C9`, making
the next turn pose last thousands of fields. The shared guarded relocation now
includes both consumers. All stock rows and the existing added two-field
cadence/no-extra-hold values are retained. No move was disabled to hide this.

## Historical human-command implementation and evidence

Shang's copied native LP/Block/LK event rows now call actual added-target
parsers. Kano is Back, Down, Back + Low Kick. Sonya is Down + Low Punch +
Block: the donor's Run chord is adapted because MKII has no Run button.
Both commands use the original airborne/busy gate and native morph routine,
not a proxy character or a host-written identity. Rejected inputs tail into
the original corresponding Shang parser. The relocated event rows must be
bound after their source tables have been copied during initialization.

`audit_v349_human_*` proves both target commands in both slots, plus Sonya's
redundant Block input and LP-first/Block-first ordering. Every successful
added-form case performs its own knife/ring release and child creation,
blocks for six damage, completes its full body release/recovery holds, then
restores Shang through the original timer and identity store. Post-restore
walking, jumping and punching work. The lifebar correctly remains Shang's
name during a native morph, as with stock targets.

`audit_v348_human_*` tests twenty actual invalid cases: incorrect/expired
Kano history, wrong or extra buttons, missing Sonya chord components and
genuinely airborne inputs, in both slots. All remain actual Shang bodies.
`audit_v350_human_*` verifies six stock fallbacks: Johnny Cage on LP, Baraka on
LK and Kitana on Block, including native restoration in both slots. All
36 human cases use real coins, selection and gameplay inputs with no guest
memory, health, position, identity or timer assistance.

`audit_v351_cpu_*_human_bindings` repeats both genuine CPU random morph
chains on the exact current v345 executable. The stage-14/P1-health fixture
remains explicitly assisted: 1,071 form fields plus 120 restored fields per
fighter, active CPU movement and later stock morphs. It is not a tower win.
`audit_v353_human_binding_mobility_*` repeats twelve cold CPU starts/real
challenger joins: cannonball and square-wave hit/block/miss, both slots,
full recovery and follow-up, 7,212 joined fields without memory assistance.

`audit_v354_human_morph_checked_inputs/result.json` independently passes all
36 human cases (36,036 gameplay fields), both assisted CPU chains and the
twelve unassisted mobility cases. It freezes 1,074 exact inputs and passes
81 reference/mutation tests: 32 human-command, 37 morph asset/CPU and 12
mobility tests. Mutations reject proxies, wrong native stores/gates,
missing inputs/fields/children/recovery/contact, incorrect palettes/groups,
non-airborne negative fixtures and broken post-restore controls. Current
CMD/installed emulator remain unchanged. This scope does not prove every
rendered pixel, every CPU contact, finishers, audio or the full objective.

## Historical v336 runtime evidence

`audit_v338_shang_kano_full_roster_table` and
`audit_v338_shang_sonya_full_roster_table` use genuine P1 selection and native
CPU RNG decisions. They explicitly select the stage-14 fixture and assist P1
health. They are NOT unassisted tower completion. No morph target, actor ID,
process, pose or coordinate is selected by the observer. Its separately logged
health fallback performed zero writes in both cases; the base helper's P1
assistance remains declared in the logs.

Kano: native ID-17 store at frame 1470, 545 callback fields in the added form,
original restoration entry 2003 and native ID-6 store 2015. Sonya: ID-18 store
1471, 526 fields, restoration entry 1985 and native ID-6 store 1997. Sonya
performs leg actions, ordinary attacks and finite two-field turning in this
window. This does not prove all paired contacts or all CPU specials.

For each fighter the independent verifier checks the actual RNG call/choice,
scoped sequence lookup, original transition palette, all three group holds
forward and reverse, original identity stores, every added-form callback,
120 consecutive restored-Shang fields, native floor 87, active CPU movement
and a later ordinary stock morph. It also reads back both timing consumers,
both new timing rows and all 17 unchanged original rows from the running ROM.

`audit_v339_native_shang_roster_checked_inputs/result.json` passes 37 tests
(10 asset tests and 27 runtime/mutation tests), 147 frozen inputs, 1,071 form
fields and 240 restored fields. The mutation checks reject missing or forced
identity stores, missing restoration, wrong owner/roster/floor, disabled Sonya
leg actions, the original CPU timing overrun, missing fields/groups/palettes,
broken later stock morphs and undeclared fixture scope. Candidate ROMs verify.

`audit_v340_current_mobility_*` contains twelve new cold native CPU starts,
real challenger joins and input-only hit/block/miss cases for Kano's cannonball
and Sonya's square wave in both player slots. Full trajectory/contact, damage,
recovery and follow-up are independently checked. No memory assistance or
cheats are used. `audit_v341_native_roster_mobility_checked_inputs/result.json`
rechecks the exact v336 executable/payload, frozen launch inputs and all twelve
cases: 7,212 joined fields, 600 checked inputs. The existing twelve mobility
verifier tests pass after making expected build identity an explicit caller
parameter; historical v300 defaults and frozen evidence are preserved.

## Preserved failed/insufficient prototypes

v355: scaled 400x300 captures are useful diagnosis, not native pixel proof.
v356: native-size pre-fix cases fail original morph palette/pixel comparison;
the new checker continues to reject all four old traces. v362: the aggregate
stopped on the old exactly-one-CPU-cycle assumption despite two actual complete
cycles. It remains a failed audit, not overwritten or promoted. v363 repairs
the verifier and adds 17 repeated-cycle mutation checks; random moves and test
duration were not changed to satisfy the old assumption.

v324/v329: forward-only morph prototype lacks the correct reverse lookup.
v330/v331–333: Kano restoration works, but Sonya's CPU turn still uses the old
table. Observer exit/stability summaries alone were insufficient to prove
restoration. Later RGB555-like action values occur during fade/teardown and
are not evidence by themselves of leg-grab corruption.

v334/v335: an initial separate timing allocation conflicted with the existing
guarded human-table relocation and failed initialization. v336 fixes the
existing relocation's missing CPU operand instead. These failures remain
preserved, not relabeled as passing cases.

v342: compile failure from a copied range-loop pair. v343/v344: new copied
event rows were checked/bound before their initialization copy and fail
closed at startup. v345 fixes that ordering. v346: the test driver read LP/LK
from the wrong I/O port and repeatedly raised Lua errors despite emulator
exit zero; it is failed evidence, not a successful human morph. v347 establishes
the morphs but sends the wrong Kano knife follow-up; v349 corrects that input
and checks actual own projectile action/creation instead of inferring it.

## Still open — full original objective unchanged

Human-triggered added morph commands are now verified in the bounded matrix
above. Original arcade random-selection behavior still needs investigation;
the inspected native CSS polling path has no established RNG call. Do not
invent a console-only random-select feature or patch its 12-field debounce
as a roster count. Asset equality and later screenshots alone do not prove
every displayed frame. The bounded morph holds
and early handoffs now have direct pixel proof in v363; wider animation/artwork
coverage remains open. Five natural P2 CPU close-contact cases now pass v372;
seven opposite-order P1 CPU cases pass v377. v380 additionally proves two full
original individual ready handoffs with new native CPU action setup. Remaining
victims and projectile/walk-to-punch follow-up state transitions, wider CPU air
throws (both slots, more victims, misses), wider human air-height/Jax/KO controls and
interrupted/KO pairs, remaining
stock projectile types and block/miss/post-ending variants, full finisher/victim,
artwork/audio QA and wider unassisted play remain. Prior v300 close/air/ending
and projectile checkpoints are historical, not a full v357 retest. A final
matched launcher/release ZIP remains required. Neither checkpoint establishes
that Kano and Sonya are natural game members in every aspect.
