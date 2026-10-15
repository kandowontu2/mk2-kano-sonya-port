# Native Kano/Sonya current checkpoint — not a finished release

Current test candidate: `diagnostic_v635_native_shadow_rows`.
Run root `PLAY_LATEST_TEST_BUILD.cmd`, or its own `PLAY_TEST_BUILD.cmd`, for this
candidate. The older root production CMD is unchanged.
The latest-test CMD's actual `-verifyroms` invocation found one good ROM set.
The production launcher remains v277; the existing release ZIP remains v258.

## Current update, 2026-10-02 (v654–v659)

All252 fresh roster-wide real-input move fixtures pass, covering eight moves,
fourteen selectable opponents, both slots and genuine airborne square wave.
The52 current positive/block/miss fixtures, ten startup interruption/retry
cases and four actual KO/next-round cases also pass. Their54 baseline/corruption
tests are green. No game build/ROM/launcher changed.

Fresh arena replay now covers both slots: all1218 samples across all nine
regular arenas match319,291,392 VRAM words/123,748,800 displayed pixels, with
30,451 components/763,757 native shadow copies verified. Actual P1 imported
CPU/Sonya mirror/alternate-color paths are included. v658 inventories the
actual runtime files, not just launch inputs; eight pass-boundary tests pass.
Unsaved inter-pass erasure/CPU writes remain explicitly outside this proof.

The five known crouching-turn roll contacts now have a bounded RETAIN decision:
actual original exposed head/hat pixels lie inside the attack/native hurtbox.
No global height correction or target-ID immunity is justified. v659 pins
all six current/earlier comparison captures and reruns nine fit tests.
Full contact fidelity, wider grounding and full-port acceptance remain false.

See STATUS_2026-10-02_CURRENT_GAMEPLAY.md for authoritative current scope and
remaining CPU/choreography/cinematic/audio/tower/finisher/release requirements.
The earlier checkpoint sections below retain their historical boundaries.

## Latest native idle reference and all-regular-arena checkpoint (v641–v645)

The v635 executable, gameplay source, payload and launchers remain unchanged.
Four cold input-only two-human Kano/Sonya-vs-Kitana cases cover both physical
slots and real idle/jump/crouch/walk through age480. All148 fixed drawing passes
match38,797,312 actual VRAM words and15,036,800 displayed pixels exactly.
All44 idle samples place imported and stock soles on row228, at the same -1
native ground offset. Both fighters land on their own physical floors. This
provides an actual idle reference, not a reason to globally lower the sprites.

Both new49,237-field P2 campaigns reach all nine actual native arena IDs0..8,
retaining330 Kano/279 Sonya frames. Every159,645,696 VRAM word and61,874,400
display pixel matches native ordered reconstruction, including1,778,983 body
pixels and266,834 surviving imported-shadow pixels. All10,501 imported
components/271,271 native row copies verify independently. No reset/ending;
these are genuine losses/paid continues, NOT cleared towers. Arena6 has no
surviving imported shadows (rendered stock Baraka also has none); those frames
are not visible-shadow proof. The observer's old seen_stages label reads a
ladder variable; coverage uses actual01061AC0 arena reads and raster records.

v24 saves only displayed prior-field pre-pass buffers: a15-sample control
remains pixel/timeline-exact with17 buffers rather than137. No old files were
deleted. The body-only v642 model, unobserved mutation helper, missing-base
test fixture and rejected LRSKIP geometry are preserved. Native source skip
advances data, not destination X; v3 independently models this and matches all
609 arena passes. The final71-test suite passes. v645 freezes detailed proof,
models and hashes; its NOTES.md records boundaries and retained failures.

Still open: P1 all-arena/mirror/alternate/secret-stage paths, wider grounding,
current Pit cinematic/art/audio, five roll contacts, broader combat and full
towers/bosses/finishers/endings/audio, then matched production CMD/release ZIP.
Floor acceptance and full-port acceptance remain FALSE.

## Native shadow input repair and prior checkpoint (v632–v640)

The original MK2 shadow routine previously read imported compressed-row headers
from unmapped CPU addresses and received FFFF. Its source pointer then walked
backward. v635 exposes the correct imported graphics bytes at the routine's
native CPU address, permits its original one-row shadow copies, and removes
the custom whole-body projection. The gameplay payload, original instructions,
driver and audio inputs are unchanged. The three changed source files are the
map, video implementation and public video header; exact pre-change bytes are
preserved in audit_v634_pre_native_shadow_sources.

Current-build cold input-only captures verify 1,654 owned components and 43,197
original shadow copies across both fighters and both slots, including actual
Sonya mirrors. Independent full-body compressed-row decoding verifies every
source, four-row advance, final repeated row, count, command, copy X/Y cadence,
palette, color and native caller. No oversized/negative-length rows occur in
these observed components. Three P1 components initially lacked full body data
at the capture-window boundary: v638 retains that incomplete evidence. Fresh
read-only v639 captures supply complete component streams; the entire original
INPUT/HEALTH/FIGHT/STATE timelines are unchanged by the expanded observation.

All 54 fixed Dead Pool samples reconstruct exactly from actual pre-pass VRAM
and native ordered writes: 14,155,776 indexed VRAM words and 5,486,400 displayed
pixels, including surviving imported shadows. Both slots' normal/mirror bodies
are observed, not forced IDs. Four current UI cases pass full portrait/cursor/
number/animation/backdrop/clearing/ladder-icon/first-match-ID/name-shadow checks.
The 60-test UI/row baseline-and-corruption suite rejects the reported UI failures
and altered row sources, coordinates, commands, width/height, palette/color,
caller, ownership and cache evidence. Current executable/source/payload hashes
are checked by tools/verify_native_shadow_v635.py and the v640 checkpoint.

This is NOT all-arena shadow/idle-foot acceptance or full-game acceptance. Native
DMA busy timing is now real, so older v602 gameplay chronology is historical,
not an asserted identical current-build baseline. Earlier v602 checkpoints
below remain evidence for that executable only; their three live source files
have intentionally changed, with their original hashes preserved in v634.
The latest-test CMD now selects v635, with an isolated configuration and no
cheats/assistance. Production CMD v277 and release ZIP v258 remain unchanged.
Remaining: native geometry/idle-foot reference across arenas/slots/secret paths,
current-build Pit/gameplay revalidation, five roll contacts, broader combat,
towers/bosses/continues/finishers/endings/audio, then matched production/release.
Floor acceptance and full-port acceptance remain FALSE.

## Historical v602 floor coverage and drawing-pass checkpoint (v620–v631)

The v602 gameplay source, executable, payload and launchers remain unchanged.
Both fresh input-only P2 campaigns reach49,237 fields and all nine regular
arenas, retaining607 floor screenshots (328 Kano,279 Sonya). Their entire
INPUT/HEALTH/FIGHT/STATE timelines equal the corresponding prior v610 runs.
These are real losses/paid continues, not cleared towers or forced arenas.
v623 passes11 baseline/corruption tests with1,561 checked inputs. Fifteen
moving Sonya Dead Pool frames bind all1,524,000 displayed pixels to actual
native TMS display-start writes, VRAM and palette. EFFC/F010/001C selects
VRAM row256,column56: the previous field's completed buffer, not the current
field's drawing buffer. No best-buffer/pose/position search is permitted.

Fresh v630 input-only P2 Dead Pool captures for both fighters each terminate
at3556 fields and retain15 fixed samples. Their full gameplay chronology
equals the corresponding v620 prefix. Version20 observes actual pre-pass
VRAM immediately BEFORE the first DMA, every original triggered command,
owned body components and the actual native flip. The independent replay
decodes all native scenery, shadows, bodies and foreground in write order.
It never initializes from the tested display-flip state. All7,864,320 indexed
VRAM words and3,048,000 displayed pixels in the thirty tested samples match
exactly, including88,710 imported body pixels and14,050 surviving imported
floor-shadow pixels. Both actual screenshots were viewed. v631 passes17
actual-baseline/corruption tests with1,512 rechecked inputs; source/pose/X/
palette/ground/foreground/event/pixel changes are explicitly rejected.

This proves the bounded drawing-pass execution, NOT that shadow geometry or
grounding is correct everywhere. Earlier inter-pass erasure, native-style
projection/idle-foot reference, P1/alternate/secret-arena paths and all-arena
pixel verification still require proof. Current sampled native Baraka poses
are mostly attacks/walking, so their lowest pixel is NOT a universal stance
reference and does not justify globally lowering Kano/Sonya.

v618/v619 preserve rejected graphics-end/padding and clip-label boundaries.
v622 preserves the incorrect current-buffer/carry model. v624–v628 and v629
preserve the later inter-pass erasure gap: an initial whole-window replay
retains stale pixels actually absent from the game. Ordinary VRAM-write taps
found no writes, and a broad PIXT scan did not establish the erasure path.
Read-only v626 disassembly proves FF816380/F800 is an MMTM extension, not
a PIXT instruction; PC=address+16 alone does not establish an opcode boundary.
Actual-register DMA merging retains exactly the same23,812 observed commands,
so a stale mirrored busy flag did not explain that gap. Pre-pass anchoring
keeps this unproven erasure mechanism OUTSIDE the accepted copy contract,
rather than silently treating the whole trace as verified. The first new
test helper also expected the wrong exception type for rejected corruption;
its original source is retained and only that helper was corrected.

The v605/v607/v609/v617/v623 manifests were rechecked: zero changed inputs.
Floor acceptance and full-port acceptance remain FALSE. Remaining work is
desired native-style floor/grounding across both slots/arenas, P1 mirror/Pit
impact/audio/art, five roll contacts, broader combat, whole towers/bosses/
finishers/endings/audio, and final matched production CMD/release ZIP.

## Both physical slots and actual P2 mirror Pit checkpoint (v610–v617)

The current v602 gameplay source, executable, payload and launchers are unchanged.
Fresh v610 unassisted P2 captures each reach49,237 fields. Kano's fall/impact
lookups37435/37494 complete at37496 and continue into actual Kano at38628.
Sonya's37468/37527 complete at37529 and continue as Sonya at38661. Each has
twenty original-cadence fall draws, one impact and42 bounded component reads
in the actual P2 cache0105F230, with no reset or proxy identity.

Actual boot timing, not forced IDs/arena/RNG, also produces CPU Kano vs P2 Kano
and CPU Sonya vs P2 Sonya. Fresh v615 mirror captures each run49,237 fields;
the entire INPUT/HEALTH/FIGHT/STATE chronology equals its prior v9 replay.
Kano has TWO native Pit episodes:17636/17695/17697, then39024/39083/39085,
each followed by a genuine paid continue and another own-ID mirror fight
at18829/40217. Sonya has39788/39847/39849 and continues at40981.
The versioned v11 observer records every exit, not only the first one.

The original Pit constructor explicitly clears A1/A2 before FF906EF0.
Its A2=0 path selects the NORMAL palette, even for a preceding alternate
mirror victim. Actual v615 argument, palette-table-load and full65-color
source observations prove this unchanged native behavior for both fighters.
Kano uses his ownFFFED000 record; Sonya uses her ownFFFED800 record.
The actual combat bodies prove alternate human/normal CPU with native
costume bit40; bit10 is also present on normal combat bodies and is NOT a
valid costume discriminator here. No forced palette or costume correction.
Both reconstructed falling bodies and Sonya's post-impact raster were viewed.

`audit_v617_native_pit_slots_mirrors_checked_inputs/result.json` passes87
asset, physical-slot, mirror and raster baseline/corruption tests with1,757
rechecked inputs. Six actual captures cover SEVEN native Pit episodes.
For133 fixed-phase falling screenshots, all675,841 opaque body pixels match
the packed own sprite, fixed centered position and exact normal palette.
The first white flash and impact/shake/blood/foreground frames are explicitly
outside that pixel contract; no best-pose/palette/position search or tolerance.
This is not whole artistic, impact-raster or audio acceptance.

The initial v10 palette tap self-read was reentrant, producing repeated
observations; v614 remains diagnostic, not accepted. v11 has a read-only
reentrancy guard and exactly one actual palette observation per scene.
v616 retains failed test helpers that targeted an earlier stock bridge draw
or incorrectly assumed adjacent log tokens. Their corrected tests target
actual own scene records; no gameplay/capture was edited to make tests pass.

Remaining: P1 mirror coverage and broader Pit impact/audio/art acceptance,
the five roll-contact fitting decisions, wider opponents/contact/interrupt/KO/
CPU coverage, all-arena floor shadows/grounding, complete towers/continues/
bosses/finishers/endings/audio, and final matched production CMD/release ZIP.
Full acceptance remains FALSE. Prior UI/special checkpoints below are retained.

## Dedicated native Pit fall, position and continuation checkpoint (v595–v609)

v602 adds own front-facing five-frame falling loops and one impact pose for
each actual ID17/18. The two original scene operands now use an extended
table; the original animation cadence, camera, impact/crack/blood, native
completion and actual victim identity remain intact. No proxy actor, skipped
finisher, renderer-copy cap, reset suppression or forced campaign state.

Visual inspection of the first v597 fix found a SECOND missing table: the Pit
constructor's character-indexed X/Y rows. Kano inherited (128,176), clipping
his body below the screen, while Sonya inherited (224,32). v602 gives each
131px impact pose its own (192,64) origin. All original table/coordinate rows
remain unchanged. v597 and its incorrect-position captures remain diagnostic
evidence, not accepted native presentation. P1 falling and post-impact v602
screenshots for both characters were viewed: bodies are centered and visible.

Fresh unassisted v603 captures each run 21,883 fields with no reset. Kano's
actual fall/impact lookups occur at16784/16843, native mode9 exits at16845,
and the paid continue enters another actual Kano fight at17977. Sonya's own
lookups occur at17027/17086, exits at17088, and continues as actual Sonya at18220.
Each retains twenty original-cadence fall draws, own impact and 42 bounded
component/zero-terminator reads. Before the first lookup, actual input/health/
fight/state records equal the corresponding original diagnostic replay.
These are real losses and paid continues, NOT cleared towers or P2 Pit proof.

`audit_v605_native_pit_checked_inputs/result.json` passes 43 native asset and
actual-scene baseline/corruption tests with 382 rechecked inputs. v604 retains
the initially overstrict checkers: stock bar refill legitimately writes FFFF
then4 to BOTH health cells in one field; original arena intro uses mode13.
The corrected verifier checks those exact original physical targets/PCs and
paired refill sequence, rather than allowing arbitrary high health values.
Actual ROM table read taps are 16-bit: value1000/1200 is the LOW HALF of the
full FF181000/FF181200 pointer, corroborated by full runtime table readouts
and actual own A9/group execution, not a malformed full pointer.

Four fresh v606 UI flows and v607's 46 regression checks pass for both fighters
in both slots: native portraits, navigation, blinking border/player number,
backdrop/animation, clearing before ladder, own icons/IDs and name shadows.
v608/v609 additionally pass sixteen fresh real human signature-move entry,
contact and recovery cases, all eight moves in both slots. These are positive
ground-command smoke cases, not a new complete block/miss/interrupt/CPU audit.
Exact source-delta checks confirm only dedicated Pit initialization changed
in the gameplay driver; video/ordinary combat and payload outside its new
allocation remain unchanged. New executable/payload hashes are recorded in
`diagnostic_v602_native_pit_position/build-info.json`. Root latest-test CMD
now opens v602; production CMD/ZIP and the installed recovery EXE are unchanged.

Dedicated raster sources were generated using built-in image_gen, corrected
for Sonya's costume, copied into `diagnostic_v595_pit_sprite_drafts`, then
uniformly reduced and encoded into existing normal/alternate body palette
indices. The source sheets and final prompt set are preserved there; native
preview/report are in `diagnostic_v601_native_pit_position_assets`. These are
provisional custom art, not discovered original arcade assets. Broader visual,
alternate-costume/audio and other-slot acceptance remain open.

At that v609 checkpoint, still required: actual P2/alternate Pit paths, the five roll-contact fitting
decisions, wider opponents/contact/interrupt/KO/CPU coverage, all-arena floor
shadows and grounding, whole towers/continues/bosses/finishers/endings/audio,
and final matched production CMD/release ZIP. Full acceptance remains FALSE.

## Historical v545 checkpoint (superseded by v602 for latest playtest)

## New release blocker: genuine Pit II cinematic lookup/overrun (v584–v594)

The unchanged v545 candidate reproducibly resets when the CPU knocks the actual
Kano P1 (ID17) into the Pit II after six genuine paid continues. This is NOT a
normal game-over return, an assisted tower, or a selection/identity substitution.
Native mode2 becomes9 at field16666 under the falling Kano actor01034020/Main
01069590. The screenshot at16770 was viewed: the Pit II bridge/chasm, falling
Kano and victorious green Sonya are visible. In the cinematic, a newly allocated
drawable0102D6F0/task0106AA60 retains the actual victim ID17.

Fresh v592 observes the exact native lookup at16784: FF83B840's original
32-bit character-table load reads FF85E6B0+17*32 = FF85E8D0 and returns1.
Both actual scene operands FF85C330/FF85C4A0 still name FF85E6B0. The valid
front-facing falling-animation table has twelve ordinary fighter rows; the
bytes at later indices are already animation data, not added roster entries.
All nineteen observed runtime values match the original MKII ROM. At16785 the
scene consumes stream1, obtains the unmapped group9F9F9F9F and enters the
unbounded original component copier FF838790. The source advances32 bits and
the component cache advances112 bits each iteration. FF838A10 then overwrites
BOTH physical health globals with7E7E, amid the wider gameplay-global overrun.
The actual reset-vector fetch at16955 follows; it is not inferred from a repeated
autoboot message. v584, v585 and v592 retain the same reset chronology.

Sonya needs a dedicated entry as well: the observed slot18 instead contains
FF85E830, which is the original Kung Lao falling-animation stream. This is a
verified runtime table alias, NOT an observed Sonya Pit execution or a claim
that Sonya has the same reset. The fresh input-only Sonya-P1 v592 scout reaches
49,237 fields, 22 actual selections and 21 paid continues without an observed
reset, but remains at stage0 and never executes this Pit path or an ending.
It is not proof of a cleared tower or universal campaign stability.

`audit_v594_pit_lookup_checked_inputs/result.json` verifies the bounded defect
with 16 actual-baseline/corruption tests and 243 frozen, rechecked inputs.
It explicitly reports defectEstablished=true, fixed=false, full acceptance
false. The preserved v593 checker boundary shows two mutation selectors
accidentally matching human_slot=1 as well as physical slot=1; v2 uses delimited
physical-slot fields. No gameplay or capture was changed to pass the checks.
The v581 harness errors and v582 duplicate callbacks remain rejected evidence;
the v583+ host reentry guard only prevents duplicate observers after a real
reset and does not suppress or repair the game's reset.

The next fix must extend both cinematic lookups with dedicated Kano/Sonya
falling and impact art, retaining the original native scene timing/camera and
both actual IDs. v586 inspected the original front-facing Pit poses against
ordinary MK3 side-view knockdowns: those are not equivalent replacements.
v587–v591 are preserved asset-search diagnostics, not accepted cinematic art.
No proxy fighter, skipped finisher, CPU disable or blanket sprite-copy guard
was installed. Gameplay source, payload, executable and both launchers/ZIP
remain unchanged. The earlier 403-test combat checkpoint remains bounded
historical evidence; it does not cover this newly reproduced cinematic defect.
All other full-goal requirements remain open as listed below.

## Latest opposite-slot full CPU-grab checkpoint (v578 / v580)

`audit_v580_p2cpu_pair_checked_inputs/result.json` passes 403 actual tests with
1,344 pinned inputs: the previous 255 checks plus 148 new actual-baseline and
physical-slot/phase corruption checks. All 983 previous v576 inputs remain
unchanged. Four fresh cold P1-human/P2-CPU full grabs pass: Kano versus Kano,
and Sonya versus Sonya, Kano and Cage. These add 442 paired callback fields,
208 held-pose fields and 92 victim-flight fields. Every held pose/offset, native
32/35 damage, release/flight and individual owning ready cleanup is checked.

The observer uses real coin/start/selection and human movement/block inputs;
CPU choices are never supplied. Independent physical-slot-global bindings for
both actors/Mains/IDs/human-or-CPU state/health agree with EVERY callback through
the terminal observation. All raw/integer coordinates and adjacent original
health-store transitions are crosschecked. No IDs, health, stage, RNG, guard,
velocity or readiness were injected. Captured Kano/Sonya paired screenshots
were viewed; that inspection is not universal floor/pixel/animation acceptance.

Sonya's mirror leg grab is followed by a complete actual native bicycle MISS:
all startup/cycle/fixed-point rise and fall fields, independent stage ground,
first own ready and cleanup pass. The other three captures additionally verify
original next-action state/body/Main lock ledgers and cleanup, NOT complete
ordinary-move pose or damage fidelity. Stock kick recovery states 104->60C and
106->600 are verified against the original MKII instructions; they are not new
port state aliases. Sonya-to-Cage clears its ordinary kick at field1969 and then
walks cleanly until the first observed shared ready at2000. Replaying every
actual flag store against every callback prevents treating that later no-op
ready as the meaningful attack-lock removal.

v579 preserves failed checker boundaries: omitted native kick recovery states,
an incorrect assumption that the executing health-store A8 must be the victim
(ordinary collisions execute under the attacker), and four mutation tests that
targeted CPU trail rather than victim vtrail. Corrected checks retain exact
native instructions, physical targets, live registers, continuous state/health/
lock ledgers and nonvacuous mutations. Gameplay/captures were not modified for
a passing result. Eleven other v577/v578 natural scouts remain explicitly
unaccepted as full-grab-plus-continuation proof. Some selected stock opponents
or never produced a grab; Kano-to-Sonya completed a grab then chose another
choke whose full miss continuation is not covered by the accepted profiles.
These scouts do not independently establish a softlock or universal stability.

No game source, payload, executable, playtest/production CMD or ZIP changed.
Full acceptance remains FALSE. Still required: the five roll-contact fitting
decisions, wider actual CPU/victim/contact/interrupt/KO coverage, all-arena
floor shadows/grounding, full towers/continues/bosses/finishers/endings/audio,
and final matched production CMD/ZIP. Native-looking whole-game integration
remains the goal; this bounded checkpoint does not redefine completion.

## Current v545 correction and integration checkpoint (v552 / v553)

The roll attack plane moves upward by one pixel, from top9 to top8. Hitbox
size72x31, actor/sprite/floor position, ten-pixel flight, 24/5 damage, native
collision/block/damage/recovery and every other emitted gameplay instruction
remain unchanged. The canonical source comparison verifies exactly one operand
change from frozen v517. This is native roster fitting, not a character ID,
held-Down or action-state immunity rule. Native CMPXY rejects shared edges;
the checker verifies the original rejection instructions instead of treating
zero-area contact as overlap.

`audit_v552_roll_integration_checked_inputs/result.json` passes 67 tests with
fresh current-build evidence: 52 human positive/block/miss/recovery cases for
all eight moves in both slots versus Sub-Zero, and four complete rendered
selection/ladder/first-match flows. Liu's held duck now misses in both slots,
including the formerly failing P1 crossover; hit/block recoil is unchanged.
Across 28 current ducked-roster captures, 23 misses pass the complete native
flight/recovery/ordinary-controls contract. Five contacts remain unresolved:
Kitana/Mileena both sides and Raiden P1. These are retained actual native24
contacts, not accepted misses or proof that every croucher must be immune.
Other crouch phases, victim fitting and broader natural gameplay remain open.

The fresh 46-case UI regression suite retains strict portrait, stock blinking
border/number, neighbor navigation, unshifted animated backdrop, full normal/
dimmed portrait and pose cleanup before ladder, both ladder icons, actual IDs
and lifebar-name shadow checks. The Kano-P1 actual fight screenshot was viewed.
v551 retains a failed checker attempt whose redundant instruction-time motion/
defense records were not crosschecked with callback fields; the new checker
requires that agreement. Captures/gameplay were not changed to obtain a pass.

Executable SHA256: `C0778D6A8199D9582A50A0B1AD7DBE1B33016D2E388035914BA3191266DC656B`.
Gameplay source SHA256: `217D08ED8CB6F4D03D1A6F24C3E43555204B9FA7B52B63C43FE8E5421157ED35`.
Payload and video remain the v517/v471 bytes. The installed/recovery emulator
was restored unchanged after building. `PLAY_LATEST_TEST_BUILD.cmd` now calls
the matched v545 playtest; its actual -verifyroms call in v553 finds one good
ROM set. The older production CMD and release ZIP are not promoted/replaced.

Earlier v526 interruption/KO and v539 natural CPU evidence has now been refreshed
on v545 in v559 and v556 respectively, within the same bounded scopes below.
The v479 continued-arena floor checks remain historical, not fresh universal
v545 acceptance. Full CPU contact/choreography/victim/slot coverage, arenas/floor
shadows, full tower/continue/boss/finishers/endings/audio and final production
CMD/ZIP remain open. No material data was deleted. Full acceptance remains false;
the complete original goal is still active.

## Current v545 CPU, interruptions/KO and full-pair checks (v556 / v559 / v565)

v556 passes 47 regression tests with six fresh natural CPU captures and 400
pinned inputs. All eight CPU move routes were observed; four P2-CPU runs check
owned entry-to-ready and original projectile child lifetime, including a native
knife cancellation. Two P1-Sonya CPU runs check ring block/chip and held-duck miss,
child retirement and clean AI walking. This is not all CPU contact choreography.

v559 passes 30 tests with ten fresh startup interruption/retry captures and four
KO/next-round captures: 21,164 paired fields and 483 pinned inputs. Blade, bicycle
and leg interruptions in both slots and bounded blade/bicycle KO paths retain
original health stores, cleanup, animation cursors and native round-two refill.
Other victims, move phases, CPU and KO combinations are not proved by this set.

v565 passes 63 nonvacuous current baseline/corruption tests with 528 pinned
inputs. Four actual natural P1-CPU/P2-human complete grabs pass: Kano choke versus
Kano, and Sonya leg versus Cage, Kano and Liu Kang. Across 446 paired fields,
208 held-pose fields and 92 victim-flight fields, the checker verifies every
authored pose/grip, native damage/release/flight and each owning ready cleanup.
The current Kano choke and Sonya-to-Cage leg screenshots were visually inspected.
That inspection is not universal floor-shadow or pixel acceptance.

The new read-only observer records Main action stores, actual A0/A1 values and
live instruction operands. The checker replays those stores against every
post-handoff callback. Sonya-to-Cage clears its grab, then begins an original
ordinary attack while Cage recovers: native lock setup precedes the original
sequence consumer's walking-to-attack publication in the same field, and the
new attack later clears normally. Kano's same-state ordinary setup retains
the strict existing NEW native lock provenance instead of requiring an action
publication the original engine does not perform. v563 preserves both failed
checker boundaries; gameplay and runtime captures were not changed for a pass.

At v565 four additional v564 natural scouts were explicitly unaccepted. The
original prose/JSON mislabeled two follow-ups: fresh instruction-entry evidence
in v568/v569 proves Sonya-to-Sonya starts bicycle, and Sonya-to-Sub-Zero starts
square-wave (the latter uses a generic native jump state). Kano-to-Liu starts
blade. Those three complete special continuations now pass the stronger checks
below; the frozen v565 report retains its original labels with corrections in
v569, rather than silently rewriting evidence. Kano-to-Sonya produced no choke
within the bounded run, so it is not a completed-grab proof; CPU choices were
never forced. These findings do not alone establish a gameplay softlock.

No gameplay, build, root launcher or release ZIP changed in this CPU-pair pass.
Complete special follow-up provenance now has bounded evidence below. Broader
victims/opposite CPU slot, unresolved roll contacts and full-game scope remain.

## Current full special follow-ups and rendered identity check (v569 / v573)

v569 passes 178 tests with 640 pinned inputs: the four previously accepted
natural grabs plus three fresh full grabs and their complete owned MISS
continuations (Sonya bicycle versus Sonya, Sonya square-wave versus Sub-Zero,
Kano blade versus Liu). The new observer/checker follows actual routine entries,
native action stores, every pose/fixed-point motion field, independent stage
ground, first original ready and real trail cleanup. This proves seven bounded
full grab cases and three complete special misses, not every hit/block/victim.

An initial visual review incorrectly called an upside-down human Sonya block:
it reversed the mirror-match identities. Fresh v570/v571 read-only display
provenance independently binds actor, cached components, native DMA and palette.
The green normal-palette fighter is P1 CPU, finishing its bicycle; the white
alternate-palette fighter is the P2 human, blocking upright. The native ready
instruction is field1961; the CPU retains its final cycling cache in field1962,
publishes ordinary upright animation in field1963 and appears upright in the
double-buffered rendered field1964. Original new high-punch setup follows at
1970. No persistent inverted human block is established by this evidence.

`audit_v573_sonya_display_checked_inputs/result.json` passes 220 actual tests
(63 paired, 115 special follow-up, 42 new visual/provenance corruption tests),
with 764 pinned inputs. All 16 consecutive frame-done captures match EVERY
visible fighter-composite pixel against previous-field native DMA and the actual
independent palettes: 81,122 exact pixel comparisons, one fixed scanout offset.
128 paired display-owner samples retain exact ROM-to-cache descriptors/offsets/
flip bits. Missing/shared palettes, wrong owners/poses, injected Y-flips,
mis-timed images and even a single changed actual body pixel are rejected.
The failed first checker scope is retained in v571/v572: it incorrectly required
walking even after a new original high-punch setup; the corrected checker proves
that setup and its actual high-punch dispatch instead of accepting stale locks.

No gameplay, payload, executable, playtest/production launcher or ZIP changed.
The suspected block defect was corrected as a diagnosis, not patched into the
game. The 640 earlier v569 inputs remain unchanged. Full port acceptance is
still FALSE. Wider CPU/victim/slot/contact/interrupt/KO coverage, the five roll
contacts, all-arena floor shadows, full towers/continues/bosses/finishers/endings/
audio and final matched production CMD/ZIP remain required. The next work is
wider actual gameplay evidence, not a build change for the misidentified pose.

## Current native crouching-turn contact diagnosis (v574 / v576)

Six fresh current-build input-only runs reproduce the five held-duck contacts
and the opposite-side Raiden miss. Every original v547 real input, participant
callback, health store, collision register and recovery event is unchanged.
The new read-only observer correctly labels actor+1A0 as the cached sprite list,
Main+210 as process flags and actor+160 as body flags; v1's misleading labels
are not reused. Original MKII main10 dispatch proves the contact poses are stock
crouching turns: FF94B660 for Kitana/Mileena and FF9699B0 for Raiden. Every cached
component/source/dimension/offset/flip equals its actual original ROM descriptor;
the Kano composite equals the actual imported ROM descriptor, with no Y flip.

The native24 store occurs at the FIRST positive comparator overlap: Kitana and
Mileena P1 overlap12x1 pixels, P2 overlap2x1; Raiden P1 overlaps9x6. All earlier
comparisons have a separating axis. Raiden P2 has twenty genuine comparisons
and no damage; when its crouching-turn bounds rise, horizontal separation is
already sufficient to reject contact. All five hits retain the complete
42-field native rebound with five-pixel signed recoil, original gravity,
individual ready, expired short repel suppression and actual walking/jumping/
high-punch follow-up. This establishes the mechanic and pose behind the
contacts, not approval that the authored roll plane fits every crouching phase.
The original MK3 reference fixtures here contain Liu/Sub-Zero, not these target
characters. Do not infer universal duck immunity or a direct target-specific
donor comparison from them. No target-ID/held-Down immunity was added.

`audit_v576_roll_turn_checked_inputs/result.json` verifies the diagnostic,
explicitly retaining contactFidelityAccepted=false and planeCorrectionClaim=false.
It passes 255 actual tests (the prior220 plus35 nonvacuous native-turn/provenance
corruptions), with983 pinned inputs, 5,460 participant callback records,
92 independent comparison observations and92 next-frame-done native-size images.
The P1 Raiden/Kitana contact rasters were viewed. Snapshot timing is explicitly
next-frame render, not a claim of instruction-time pixels. v575 retains the
failed comparison between instruction-time X and pre-integration callback X;
the corrected checker requires independent GEOMETRY agreement AND the exact
native ten-pixel integration. Game and captures were not changed for a pass.

No gameplay, payload, binary, root launcher or release ZIP changed. All764
earlier v573 checked inputs remain unchanged. The five contacts still require a
contact-fitting decision; broader CPU slot/victim/choreography, all-arena
shadows, full-game/finishers/endings/audio and final production artifacts remain
open. Full port acceptance remains false.

## Historical v517 integration checks (v524 / v526 / v529)

`audit_v524_full_human_matrix_checked_inputs/result.json` verifies 52 fresh
current-build human cases: 18 positive and 34 block/miss/recovery paths for
all eight moves, both slots, versus Sub-Zero. It checks 46,178 paired fields,
eight corruption tests and 384 pinned inputs. Square-wave actual airborne
hits and standing misses, leg standing/duck block distinctions, and Kano's
correct current roll flight/recoil are included. The bounded matrix passes;
full acceptance stays false because wider roster geometry and full-game scope
are not proved by this fixture matrix.

`audit_v526_interrupt_and_ko_checked_inputs/result.json` verifies ten fresh
startup interruption/retry cases for blade/bicycle/leg in both slots and four
blade/bicycle KO/round-two cases. The actual native health writers, identities,
owners, cleanup, authored animation cursors and real next-round refill pass:
21,164 paired fields, 30 regression tests and 483 pinned inputs. This does not
prove every move, victim, interruption point or CPU collision outcome.

`audit_v529_native_ui_checked_inputs/result.json` verifies four fresh Kano/Sonya
campaign-slot runs through selection, ladder reveal and first match. Complete
source-authored top portraits, stock-matching four-pixel blinking borders and
player numbers, stable horizontal/vertical neighbors, animated stances with
unshifted backdrops, no retained normal/dimmed portraits or idle/locked poses
after selection exit, both ladder icons, actual fighter IDs17/18 and lifebar
name shadows all pass. The 46 regression checks include rendered corruptions.
Native-size Sonya-P2 selection/ladder and Kano-P1 fight images were also viewed.
The initially insufficient checker sampled vertical visits but missed one
corrupted intermediate field; `audit_v528_ui_checker_gap` preserves that failed
checker/log. The strengthened checker requires every settled navigation field;
neither the game nor frozen capture was edited to obtain a pass.

New root `PLAY_LATEST_TEST_BUILD.cmd` forwards to the matched v517 test CMD.
Its actual `-verifyroms` run in `audit_v530_latest_test_launcher` finds one good
ROM set. It is explicitly a playtest, not a release; the older production CMD,
release ZIP, game source, executable and payload are unchanged in this pass.
All newly verified capture/checker inputs are pinned and historical evidence
remains intact. No material data was deleted.

Two additional original MK3 Liu duck-start timings, 4040 and 4060, are retained
in `audit_v522_original_liu_duck_phase_*`. Both pass the original full-flight,
20-rectangle, zero-contact and grounded-recovery contract. The port's Liu-P1
duck contact still remains under review; this is not a newly fixed collision.

## Current bounded native CPU checkpoint (v539)

`audit_v539_current_cpu_native_checked_inputs/result.json` now passes 47
baseline/corruption tests and pins 399 inputs. All eight move routes are observed
on the actual unchanged v517 build, not relabeled historical CPU captures.
Four P2-CPU runs check native identity/ownership, entry-to-ready and original
projectile release/child lifetime. Two P1-Sonya CPU cases independently check
ring block impact/chip and held-Down miss, child cleanup and clean AI walking.

The fresh `audit_v536_cpu_knife_interrupt_callers` capture proves the disputed
knife interruption: child birth8999, native22-damage9010, five four-field original
hurt-list draws9011..9027 and native ready9031. Actual stack callers FF83C370 and
the owned fallback router FFFC1370, original instruction bytes and native flags/
poses are checked. The already-created knife still completes its original child
intro/travel/retirement. This is one explicit native cancellation path, not an
unconditional damage exception or proof of every cancellation point.

The new checker first requires every original release hold; only an actually
replaced release can use the explicitly proved hurt path. Damage at the end of
an otherwise complete release does not require a fabricated cancellation trace.
All baselines must pass before mutation tests run. Retained v537/v538 checker
failures document pre-entry mutation targeting and that release-boundary issue.
Game source, executable, payload, production CMD and release ZIP are unchanged.
Full CPU collision/choreography/victim/slot/KO/tower/art/audio acceptance is still
open; observed dispatch coverage is not full character integration.

## Current crossover diagnosis (v542 / v544), collision still unresolved

The two fresh v540 detail captures reproduce every original v518 real input,
paired field, native rectangle and health event exactly. v542 pins the diagnostic
and all 34 native-size next-callback screenshots. At Liu's crouching-turn pose
FF9236D0, P1 has nine-pixel horizontal and one-pixel vertical overlap and takes
native24 damage; P2 has a one-pixel horizontal gap and takes none. The original
donor P1 fixture also has vertical overlap when its bounds rise, but a three-pixel
horizontal gap. This distinguishes crossover geometry from blanket duck immunity.
The v1 detail observer's two incorrectly named list fields actually read opponent
Main pointers; the checker explicitly excludes them and claims no animation-list
provenance from them. Screenshot association is next callback, not instruction-time
raster state. The P1/P2 crossover screenshots were visually inspected.

Four additional original MK3 real-input spacing variations (one left walking
field, one/two/three right fields before release) all retain twenty rectangle
comparisons, zero damage and complete recovery in v544. No identity, health,
position or RNG was injected. Neither these captures nor v542 justify changing
the hitbox simply to pass a fixture. Native crossover/pose fitting remains the
next collision investigation; no collision fix or release promotion is claimed.

## Historical v533 CPU diagnostic — superseded only in the bounded scope above

Four fresh 180-second input-only natural ladder captures are retained in
`audit_v532_cpu_*`; actual selected schedules/IDs, health and CPU state were
not injected. The v2 launcher additionally tracks every actual build input,
transitive selection Lua and shared ROM/artwork files.
`audit_v533_current_cpu_diagnostic/result.json` pins their current verification
and 297 inputs.
Kano actually performs knife/ball/blade/choke; Sonya performs bicycle/leg/square.
CPU ring was not observed in these runs and is not counted as verified.

Three cases pass the independent native ownership/entry-to-ready and complete
projectile child-lifetime contracts. Kano boot605 remains rejected by the full
projectile-body release-pose contract: its third knife at frame8996 takes native
22-damage at9010 and displays hurt poses instead of finishing the release list.
The independent child was already created at8999, before that hit, and native
ready occurs at9031. This requires instruction-backed interruption/cancellation
review, not blindly forcing uninterrupted poses after damage or weakening the
gate. The 19-test suite deliberately remains failed on that actual-case check;
its corrupted-record rejections do not establish acceptance of a failing base.
At that checkpoint, knife cancellation and natural CPU ring were the next work;
their fresh bounded evidence is now described in v539 above.

The earlier 95-second `audit_v531_cpu_kano_boot605` never reached Kano (actual
opponents Baraka/Reptile); its zero CPU entry count was an insufficient window,
not a softlock. All four short runs remain diagnostic. Both subsequent longer
processes completed normally; no CPU job remains running. Gameplay code/build
and the clearly labeled latest-test launcher are unchanged by these probes.

## Current cannonball flight/rebound correction

Executable SHA256: `8E11915DC9DD1DE17616FD15034D6B9D7656091BDFA9B545942F73222942779E`.
Gameplay source SHA256: `B8542F4777E4F100EC4E86771AD70EC867522FE106DD51E6F164E408489722D3`.
Payload remains `82FE153FB56B46A6F9D42F493451AC3D59AD61713433714ACA7704E2881F8951`.
Video, artwork, audio, floor parameters and the cannonball descriptor are
unchanged from v500. The emitted-code comparison limits the change to Kano's
own flight/rebound handoff; strike/block collision is still native and active.

Real instruction/velocity observations identified MKII's body mover at FF8285B0
halving a close roll or pushing a passing roll at three pixels per field. Kano
now refreshes the game's short repel counter during flight and native rebound.
The native away helper updates both desired player VX and actual actor VX;
the fling's D sentinel preserves that signed vector. Otherwise the suppressed
mover can leave the old ten-pixel roll VX in the rebound. v512/v514 demonstrated
that failure and are retained as rejected diagnostics, not passing fidelity.

`audit_v519_cannonball_velocity_checked_inputs/result.json` verifies nine current
targeted cases, 8,420 paired fields, eight contract/corruption tests and 130 pinned
inputs. Hits still deal 24 and blocks 5; recoil is five/one pixels per field,
with twenty actual coordinate/velocity/gravity fields checked in both slots.
Sub-Zero and Kung Lao duck misses complete all 26 ten-pixel rolling fields and
20 actual rectangle comparisons. Liu P2 also passes that miss path. Native
recovery, counter expiry and real walk/jump/punch follow-up are checked.

The overall gate deliberately remains false: Liu P1 still takes 24 damage while
ducking (`audit_v518_cannonball_duck_p1_liu_kang`). Six original MK3 Liu/Sub-Zero
ground/block/duck captures were extended beyond the formerly truncated window
and now include full flight/contact/recovery. Eight additional real Liu duck-start
phases also miss in the original. This supports further collision-fidelity work,
not a rule to make every crouching/airborne actor artificially immune.

`audit_v521_sonya_smoke_checked_inputs/result.json` separately passes four current
ring/leg-grab cases: both slots, actual Sonya ID18/Main ownership, native 22/35
damage, recovery and ordinary controls; 2,618 paired fields and 91 pinned inputs.
This is not complete current Sonya, CPU, UI, campaign or finisher acceptance.

Historical v510 preserves the v500 matrix: 18 positive and 34 defensive Sub-Zero
cases, 46,178 paired fields, 20 tests and 560 pinned inputs. Its 28 wider duck
probes exposed eight contacts and four kinematic counterexamples. It is not
automatically current after the v517 gameplay edit. v491's ten interruption/retry
and four KO/round-two cases are likewise historical v471 evidence.

Remaining: resolve the crouch-contact geometry; broader victims, arenas,
interruption/KO points and CPU collision/choreography; full tower/continue/boss/
finisher/ending/audio acceptance; and the final matching production CMD/release
ZIP. Current bounded human, interruption/KO and selection-to-first-match checks
are above; they do not replace these broader requirements. No release promotion
occurred.
Original v471/v500/v512/v514 sources and failed tests are retained. No material
data was deleted in this continuation.

## Historical v471 continued-arena palette correction

Executable SHA256: `5A33F3368E1AD975ED5FF72EC2E0C6EA74F2BF5BCB4CCD7B2F8338E24E22F01F`.
Video source SHA256: `1DB05087A5562DCC6C03241A744542168FF2D64FF0C5301FCAABB2F10E0E44EC`.
Gameplay source, payload and original video-header ABI are unchanged.

After an actual paid two-human continue, the next arena allocates fighter
palette banks 0400/0500. The old shadow pass incorrectly protected 0200/0300,
which now belonged to scenery: it omitted floor shadow pixels and could erase
pixels at a fighter's feet. v471 protects the two actual live Main-owned actor
palette banks instead. It does not change character IDs, health, physics or
guest memory. The existing projection formula is retained, not newly proven
universally equivalent to original native row-DMA geometry.

`audit_v479_continue_palette_floor_checked_inputs/result.json` passes its
bounded check with 5,534 rechecked inputs and 13 contract/counterexample tests.
Four matched v472/v474 before/after runs cover Kano and Sonya in both slots.
All 72 post-ready Courtyard stance/walk/jump/landing screenshots have complete
expected visible silhouettes, and changed body pixels only restore previously
black pixels to their independently decoded original colors. No other pixels
change in those 72 images. The stationary sole row is 236 for both players,
matching actual Kitana. Inputs, native gameplay records and body-DMA observations
are unchanged. Earlier ground/continue/reselect screenshots also remain exact.
Arena-intro images are retained but are not included in the 72-image shadow
contract; jump decoder correlation is diagnostic, not complete body decoding.

Both stock Sub-Zero controls preserve every pixel in all 900 screenshots, plus
their actual inputs/game records. P2 uses the complete separate v476 retry;
the disk-full partial v474 Sub-Zero P2 run is retained and rejected.
The v477 checker attempt had a truncated hash constant; v478 correctly stopped
at an old live-source hash. Neither is acceptance evidence. v479 uses only the
exact named original frozen build source when that deliberately edited live
source no longer matches, and rechecks every tracked input.

The real-input probes include ten ordinary uppercuts, two genuine round losses,
the native two-credit continue, reselecting the opposite added character, both
human confirmations, entry into a new fight and normal walking/jumping.
This is two-human versus continuation, not a CPU tower or a native ladder replay.
The v17 observer's old fixed palette assumptions are diagnostic only; v18 reads
the actual actor palettes/owners. No fresh full selection-border/number/backdrop,
ladder, name-shadow, foreground-occlusion or all-arena acceptance is claimed by
v479. The prior v465/v454 checks below remain frozen historical checkpoints.

Run `diagnostic_v471_owned_palette_floor_shadow/PLAY_TEST_BUILD.cmd` for this
unpromoted candidate. Its actual CMD `-verifyroms` invocation passes. No final
release ZIP or root production launcher has been replaced.

## v484 current human special activation/contact/recovery matrix

The unchanged v471 build now has fresh input-only coverage of all eight specials
from both controller slots: Kano knife, cannonball, blade and choke; Sonya ring,
square wave, bicycle and leg grab. `audit_v482_human_special_*` contains 18
independent cold two-human launches, with Sub-Zero standing for the basic matrix
and genuinely jumping for two additional square-wave hit cases. No guest health,
position, identity, stage, CPU/RNG or input-history assistance is used.

`audit_v484_human_special_matrix_checked_inputs/result.json` passes with 174
rechecked inputs, 18 reference/corruption tests and 12,838 actual paired fields.
Every callback retains the true native actor/roster ID, human controller and
Main ownership. Every input command reaches exactly one correct owned native
special instruction. Original collision stores explain every health change;
the special contacts deal knife/ring 22, ball 24, blade 26, choke 32, bicycle 22,
and leg 35 damage. The ordinary kick during the held-LK cannonball command is
accounted separately from the special's own 24 damage. Square wave's standing
miss is expected original anti-air behavior, not an activation failure; actual
jumping Sub-Zero takes 27 damage in both slots.

All cases reach the original individual ready continuation, then both actors
actually return to grounded idle action 0303 with no busy flags, gravity, motion
or attachments. Real follow-up walking, jumping and high-punch actions succeed
and end cleanly. Crossed/opposite-side geometry correctly distinguishes native
two-pixel backwalk from 2.5-pixel forward walk; actual coordinates agree with
those velocities. Native body pose pointers advance during each special.

The earlier v480 observer was diagnostic: physics alone admitted a victim's
brief action-zero transition before grounded idle. v482 explicitly waits for
both idle actions. The v483 checker attempt incorrectly required only forward
walking after a crossing/leg flip; its failure remains preserved. v484 accepts
the appropriate original forward/back velocity AND checks actual coordinate
steps. Corruption tests reject lost fields, wrong IDs/owners/buttons, missing
native entry/ready or collision stores, damaged health provenance, frozen poses,
missing airborne input, stalled/teleporting walk, frozen jump/punch and false
phase summaries. No frozen capture was edited to make the checks pass.

This is positive human command/contact/recovery and ordinary-follow-up coverage,
not every authored hold/component, projectile child field, every rendered pixel,
all victims, every rejected command, block/miss/interruption/KO, CPU, campaign,
finisher, ending or audio acceptance. The 54 native-size screenshots are retained
for inspection; their dimensions and hashes do not prove complete artwork QA.
No game source/build/payload or production launcher changed in this pass.

## Historical v456 KO/round-two checkpoint

Executable SHA256: `2731D2D965477251F19E1E8496480588C59BA521DDC3DD4AE55C3FD14D7DDB0A`.
Video source SHA256: `9C81FD1251615DD10B6E544F33D126A15DA80E8BB5D04AE8CA7D4FC2065A5464`.
Payload, gameplay source and original video-header ABI remain unchanged.
MKII switches to mode 5 immediately after a KO; v447 excluded that state,
so the imported floor silhouette disappeared while the same actual fighter
fell and remained in the winner scene. v456 admits mode 5 while retaining
true-ID, Main-owner, palette, source and bounds protections.

Fresh v457/v458 before/after captures cover Kano, Sonya and stock Sub-Zero
in both slots: five genuine uppercuts, native health writes, actual KO,
winner scene, native health refill and 61 grounded round-two fields.
The four v459 UI cases compare entire images against v450, not just HUD strips.
Independent v462/v464 read-only foreground observations record the palette
at each draw, including the KO blood's 0500 palette. v460's constant-palette
assumption was insufficient; the disk-full v462 Sub-Zero P2 log is incomplete
and is replaced by a separate full v464 launch, not overwritten.

`audit_v465_ko_round_floor_shadows_checked_inputs/result.json` passes all
22 new tests with 4,529 checked inputs. All 6,514 v454 and 4,838 v440 historical
inputs remain hash-identical, using their original frozen video-source copies
where the live source deliberately changed. Both stock controls are whole-image
bit-exact. All 688 native-size v459 selection/ladder/intro/name-shadow images
match v450 in full. Every expected visible KO silhouette pixel is black;
actual body pixels and independently identified foreground colors are preserved.
Counterexamples reject absent, shifted, miscolored and flickering KO shadows,
changed stock/UI/name pixels, proxy IDs, false damage provenance and lost round two.

Historical v466 two-round-loss observations extend to native match-ending/defeat flow:
ten real uppercuts, second KO at 4889, native finish-time/winner states and
mode-3 lost-controller transition at 5369. The imported identity/Main ownership
survives until original teardown. Kano's 5600 image shows the actual two-credit
continue screen. Those v466 diagnostic captures alone do not prove purchase/reselect,
complete finish-state pixels, fatalities, broader victims or a whole campaign.
Neither the production CMD nor the release ZIP has been promoted.

## Historical v447 identities and verification

- Executable SHA256: `8B4DA232C575F0983C17CDF5CEC3338C416765000718D28BBEBA3AA17102811B`
- Payload SHA256: `82FE153FB56B46A6F9D42F493451AC3D59AD61713433714ACA7704E2881F8951`
- Video source SHA256: `0BA09D7ECCE4651136DBC55F60007B542C6E91204E2D14F95A162C15401D26E3`
- Gameplay source remains `1F9E368A0763D63DF928D04E8A0CAE3B78A79DEC911FDB85308A92A99D0B1C97`.
- Video header remains the original ABI: `8BA30B7AA635EA1FD68CF46697560E58BA7E3FC7A2C760C0881414836FBFD4D5`.

## Changes and actual verification

v437 removed the cache race that made shadows disappear as animation advanced.
It derives the floor row from MKII's native camera/display transform and binds
the projection to the actual fighter Main owner, imported stream and palette.

The real uppercut captures then exposed two additional problems: short composite
heads and wide flat-fall poses failed the old dimension filter; VRAM-derived
masks omitted rows when a fighter flew partly off-screen. v447 accepts those
body dimensions and decodes the complete queued component directly from ROM,
with bounds checks, while retaining both fighter-palette protections. Detached
knife/ring/impact assets use separate native graphics and palettes.

The standalone new suite passes **32 tests**, including deliberately missing,
shifted, miscolored and flickering shadows, overwritten foreground chains,
changed stock images, changed selection/ladder art, changed lifebar-name shadows,
the earlier off-screen mask and the earlier absent flat-fall shadow. Older
verifiers, launches and snapshots were not edited to obtain this result.
The completed v454 checked-input audit also passes: **6,514 inputs frozen**,
with all 4,838 prior inputs preserved. The intentionally changed live video
source is verified against the original v440 frozen copy for the old checkpoint;
it is not misrepresented as unchanged. Full-port acceptance remains false.

Current real-input observations cover both player slots:

- Six mobility cases: 117 native-size images and 962 participant fields each.
  Kano/Sonya stance, genuine jumps, crouch and walking retain all expected
  visible shadow pixels and share Kitana's rendered ground contact. The
  two Sub-Zero controls are whole-image identical to their originals.
- Six actual uppercut cases: 211 images and 882 participant fields each.
  A stock Kitana uppercut causes exactly 40 damage, a high airborne launch,
  an actual flat fall and physical recovery. Both Kano/Sonya identities remain
  17/18 with their own Main ownership. All observed input, health, pose and
  physics fields match before the rendering changes; sampled opaque body and
  foreground positions remain bit-exact. Stock controls are whole-image exact.
- Four current selection/ladder/first-match cases retain the entire verified
  pre-match images, actual selection and ladder records, identity and lifebar
  name shadows. Mode 7 is classified from the original arena lifebar signature,
  since it spans both ladder and arena setup.

For uppercut scenes, independent supplemental DMA/ROM observations identify
foreground chains and blood using the actual large MKII graphics region,
palette colors and draw order. Those observations have identical original
gameplay/body-DMA records and do not replace the actual snapshots. Foreground
occlusion is verified from the frozen original image, never inferred from a
candidate or a mutated test image. The body decoder's correlation scores are
diagnostic only: whole-image stock comparisons and before/after body comparisons
are the relevant preservation checks, not a claim that every stock DMA decodes
perfectly in the older inspection tool.

Evidence: `audit_v448_unclipped_reaction_*`, `audit_v449_unclipped_ground_*`
(Sonya's exact mobility replay is v451), `audit_v450_unclipped_ui_*`, and
`audit_v453_foreground_*`. The checked-input checkpoint is v454. Earlier misses,
the partial v444 mask, the wrong-boot Sonya replay and the incorrect-bank v452
observer are retained as rejected/diagnostic attempts, not green evidence.

## Still required for the full goal

The historical v447 checkpoint proves one real uppercut and regular mobility
in Goro's Lair, not every arena or every reaction. v456 expands to KO and round
two there; v471 checks dynamic palette silhouettes after a versus continue in
the Courtyard. Other arenas, camera transitions, full
match-ending/finish states, attacks/throws and ground contact need broader runs.
Rotated/composite-pose shape and parallax also need direct comparison with the
original native row-DMA geometry: the current pixel checks validate the retained
projection formula, not universal native-equivalence for every pose.
Complete human/CPU moves, hit/block/miss/recovery/interruption/KO and victim
coverage, whole towers and campaign losses/continues/reselection, bosses, finishers, endings
and audio remain part of the original natural-character goal. Prior narrower
suites are historical evidence, not automatically current full acceptance.
A final matching production launcher and release ZIP must follow acceptance;
neither has been promoted by this checkpoint.

## Historical storage notes

A current read-only check observed 480,873,967,616 bytes free on C:. That large
external storage recovery is not attributed to this continuation. The low-space
figures below describe the earlier compression checkpoints, not current capacity.

No material data was deleted in this floor-shadow work. Compiler caches and
trace logs were transparently compressed in earlier passes. A further eight
historical executables were compressed with Windows LZX, reclaiming
**197,697,536 allocated bytes**; all eight before/after SHA256 checks pass.
See `WORKSPACE_LZX_COMPACTION_2026-10-01.json`. This is reversible, leaves paths
usable, and preserves the existing evidence archive. Drive free space remains
low and is affected by work outside this folder; those other projects were not
touched.

Subsequent LZX compaction/retry brings the total to **608,313,344 bytes** across
22 historical executables, every hash preserved. The separate `_v2.json` report
retains the 11 initial low-space failures; `_v3.json` records their successful
retries. Ordinary NTFS compression of the old v277 production executable also
preserves its matched build bytes. No production launcher or release promotion
occurred. C: briefly had about 515 MiB free after the compression pass; a later
read-only verification observed about 291 MiB. Unrelated storage pressure is
not solved, and those other projects remain outside this cleanup.
