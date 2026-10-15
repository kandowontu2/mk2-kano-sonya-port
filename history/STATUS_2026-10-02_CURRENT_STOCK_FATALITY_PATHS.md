# Owned torso sections and invariant blood; natural-character goal incomplete

Current experimental build: diagnostic_v978_owned_torso_invariant_blood.
EXE SHA256: 885B1A50DB68F6806C8A3B32DA329CAA87CCAC7636ADDB3D0283D83850023D1D.
Payload SHA256: 2679C041539C99F917CE1A9AAADAE455859A20DA5F5CC8AF9FB6013DB6A79F79.
Driver SHA256: DF26C6EADA53FF4D6A1AD48D37C4F2112310F8E1C643B0336999A854A40B0AA8.
This candidate is NOT ready for release: broader integration remains unfinished.
The installed executable, existing play CMDs and release ZIP have not been updated.

## Current owned Cage torso-rip implementation and evidence

v958 replaced the owned main57 substitutions with six dedicated upper-body
assets and an independent standing lower stump for each real character.
Selected transparent assets and complete built-in image_gen prompts are in
art_native_torso_v951. The native 52-word grammar, function tokens, five
actually dispatched upper poses, component counts, scheduling and cleanup
are preserved. Native pose4 is encoded but is not dispatched by this action;
it is NOT runtime-accepted. No Liu body sections or intact whole fighters
remain after the split.

The original native action raises the victim's floor by 80. Correct asset
anchors account for it: both lower stumps end at 141; upper landing anchors
are 59/60. The original failed v954 floating/buried sections remain preserved.
Earlier frame-callback snapshots showed the prior rendered page; v963 moved
capture to register_frame_done after native presentation without changing
the game. Rejected old pictures and failed checks are preserved, not waived.

v978 fixes Kano's torso blood turning blue in his alternate costume. Two
built-in image_gen edits identify ONLY cut-waist blood in cyan semantic guides
in art_native_torso_blood_v976. The encoder uses original immutable source
pixels/silhouettes, not the edited guide's redrawn body. Only classified blood
indices use native red pens48/46/63, invariant in both costumes. Every alpha
pixel and non-blood index stays exactly unchanged; Sonya stays unchanged.
The v978 payload differs from v958 in only 1,029 packed Kano graphics bytes.
No guest code, descriptor, geometry, palette record or costume selector changes.
The guides are never displayed cyan in-game. tools/build_native_torso_art_v977.py
and audit_v977_owned_torso_blood_encoding preserve the exact conversion.

audit_v979_cage_{kano,sonya}_p{1,2}_owned_torso are four unassisted real-input
games on this current build. Each earns 322 real collision damage, two KOs,
uses original Down Down Forward Forward LP, completes at native age185 and
reaches the continue screen at field5198. All four have 2,236 owned section
DMA passes (8,944 total), including 4,368 grounded lower-stump passes and
3,644 grounded upper passes. No post-gameplay reset/cache overrun occurs.

tools/verify_native_torso_art_v980.py independently proves source conversion,
costume-invariant red pens, unchanged alpha/nonblood indices, native control
grammar, whole 1MiB guest equality, FIFO/DMA ownership/true IDs, physical
command/damage/completion/continue, exact floor projection and displayed pixels.
audit_v980_owned_torso_blood_runtime_checked passes; actual 24 presented pose
matches in audit_v981_actual_presented_torso_blood_pixels_checked have minimum
0.736673 (Cage arm occlusion; unoccluded poses match1.0). All 32 actual scenes
were reviewed in audit_v986_owned_torso_blood_visual_review. Acceptance is
normal costumes, both characters/slots, Dead Pool only. The 23 corruption
methods in audit_v982_owned_torso_blood_corruption_units pass.

audit_v983_cage_kano_p{1,2}_alt_diagnostic deliberately makes ONE explicitly
logged flag-6 write before the original command. Both native part objects
then select the actual alternate palette via original FF90C800; true IDs,
native command, collision damage, choreography and cleanup remain unchanged.
audit_v985_controlled_native_alt_blood_checked proves actual hardware alternate
pens, blue outfit trim, red blood, native geometry/floor/pixels and continue.
Both 16-scene contact sheets were manually reviewed in
audit_v984_controlled_alt_blood_visual_review. This is controlled native
alternate-branch proof ONLY, NOT natural alternate-selection acceptance or
all alternate costume/death-path acceptance. The assist is not hidden inside
the normal unassisted matrix.

## Current same-build Kitana and Reptile regressions

audit_v987_kitana_{kano,sonya}_p{1,2}_owned_inflation pass
tools/verify_native_inflation_art_v989.py on the SAME v978 EXE/payload:
700 owned DMA passes, 24 hardware palette dumps, 268 selected actual pictures,
normal Dead Pool native timing/control/table/floor and continue retained.
audit_v991_current_inflation_corruption_units passes 39 methods.

audit_v988_{kano,sonya}_p{1,2}_native_death_grounding pass
tools/verify_native_death_grounding_v990.py on that SAME build. Original
scenario records and all 124 PNGs are byte-identical to accepted v904 runs;
1,950 body +104 head DMA passes and all three native raster floor phases
remain correct. audit_v992_current_reptile_corruption_units checks 25 methods.
This is not rolling-head/alternate-palette/all-finisher acceptance.

Latest scoped checkpoint: audit_v995_owned_torso_blood_checkpoint/checkpoint.json.
The first v994 save stopped on a mistyped observer filename before producing
a checkpoint; its partial source snapshot/tool are preserved. No game/test
failure was waived. v995 uses the actual v904 grounding observer filename.
All 12 normal physical cases plus two explicitly assisted alternate diagnostics
are kept distinct. Full-port acceptance remains false; goal stays active.

## Historical v936 inflation implementation (superseded candidate)

Historical EXE: FBD133DEDAAF7DF242D52A38638143F1EA61AE2214599A4F536F07936C26D6D0.
Historical payload: 6482D45F2105D9E6410C9CCE3AE64B6C5A28671972F8F7EDD3F7B54F3A42F637.
Its accepted inflation assets remain part of v978, but v936 is NOT current.

Kitana's native kiss-explosion command is held Low Kick, Forward, Forward,
Down, Forward, release Low Kick. The observer begins the button hold in real
ordinary combat, earns two KOs through native collisions, and releases after
the actual direction inputs. No actor, health, position, state, timer or RNG
write is used. This is not her fan-decapitation animation.

The original short timing table FF8CD3B0 and position table FF8CD2F0 are now
independent 19-row tables at FFFEB400/FFFEB600. Both added main-40 streams
retain the original seven-frame/control-token grammar, so their timing offset
is 40h; relative X is -73. All bytes indexed by existing IDs 0..16 are retained.
Only operands FF8CC790 and FF8CCC80 are redirected.

That two-table candidate, v915, still reset: the shared native inflation task
indexed three more short tables, loading executable words as stream/palette
pointers. FF838860 then wrote unmapped descriptors through the player globals.
The actual failed runs audit_v913_kitana_sonya_p2_forward_scout and
audit_v916_kitana_sonya_p2_parameters remain preserved, including cache writes.

v918 extends the three native pointer tables to 19 rows, preserving every
existing ID result. The added IDs have separate 8-word stream copies and two
separate palette records each. Original inflation, burst, scheduler, cleanup,
palette loaders and physical character IDs remain unchanged.

v918 was a crash-only intermediate: its private streams still referenced stock
Liu/Kitana artwork. That build, source/status and failed runs are preserved,
including audit_v934_pre_owned_inflation/input_sources.

v936 replaces ONLY those private streams/palettes and adds 12 dedicated native
body descriptors/groups and 162,308 packed graphics bytes. Built-in image_gen
used authentic Kano/Sonya costume references and decoded original MKII poses.
Selected transparent PNGs and every prompt are in art_native_inflation_v933.
Sonya's incorrect first-draft white trouser panels/bib were rejected and
corrected with image_gen. Encoding is alpha isolation, one uniform fighter
scale, owned palette quantization and six-bit packing, not Python painting.

KIF1 allocation is payload180000..1BFFFF, descriptors FB040..FB12F,
groups FB180..FB1DF and graphics 1EE0000..1F07A03. Previously used payload
bytes, all stock rows and guest code are preserved. The original phase
separators, native scheduler, true IDs, timing/position, palette switches,
generic gib emitter and retirement are unchanged. Burst blood ramps use
pens59..62. No stock Liu/Kitana bodies remain in these added inflation poses.

Normal-costume inflation presentation is accepted ONLY for both characters
in both physical slots in Dead Pool after all 24 actual displayed poses were
reviewed. This is not all death-art, alt-costume, all-arena or full-port acceptance.

## Preserved v918 state-repair evidence

audit_v921_kitana_{kano,sonya}_p{1,2}_native_gore are four cold physical-input
two-human games. All exit0 at field5198, earn 322 native damage and two KOs,
activate the original Kitana action and call original FF8CDC40 at age276.
All reach the real continue screen. No post-gameplay reset or body-cache
overwrite occurs. Two word reads and all six bus halves of the three pointer
reads are bound to the true physical victim, its real ID and original CPU PC.
There are 244 real 400x254 snapshots through action age600.

tools/verify_native_gore_victim_tables_v924.py independently passed all four
cases. It verifies actual physical command/hold/release, original collision
health writers, native completion, continue screen, every table consumer,
full snapshot chronology, immutable inputs, and entire 1MiB guest equality
against v901 plus only these five intended table extensions.
audit_v924_native_gore_victim_tables_checked stores the report.
audit_v925_native_gore_victim_table_units passed 25 corruption methods.

## Historical v936 genuine runtime evidence

audit_v939_kitana_{kano,sonya}_p{1,2}_owned_inflation pass
tools/verify_native_inflation_art_v941.py. All reach field5198, earn 322 real
damage/two KOs, preserve original native action/completion ages and continue.
Every owned pose dispatches through native FIFO/DMA: 175 passes per case,
700 total. Actual initialized graphics equal selected PNG conversions; all
hardware costume/blood pens match native RGB555 records. Every pose contacts
raster row228 while this task holds cameraY=-8. Burst lasts the original three
fields then retires. There are 244 periodic and 24 next-field pose snapshots.
Entire guest equality permits only the specific private owned art changes.
audit_v943_owned_inflation_visual_review contains all actual contact sheets
and the scoped manual review. audit_v942_owned_inflation_corruption_units
passes 39 methods, including proxy IDs, foreign graphics, floating feet,
bad palette banks, missing burst pictures and unretired native artwork.

Preserved v938 first-DMA snapshots showed the prior native page. v939 waits
its original one-field presentation; executable/payload were unchanged.
Failed v940 incorrectly demanded Reptile-only camera phases {228,233,238};
actual Kitana queues/DMA prove cameraY=-8 and row228. v941 fixes that test
assumption, not the game, retaining every stage/page/camera projection check.

Reptile was rerun on the SAME v936 executable/payload, rather than assuming
historical acceptance carries forward. audit_v944_{kano,sonya}_p{1,2}_native_death_grounding
all pass tools/verify_native_death_grounding_v945.py. All 124 rendered PNGs
and original scenario records are byte-identical to the accepted v904 runs.
There are still 1,950 owned body DMA passes and 104 owned head DMA passes,
correct physical floor and camera/page projection, and original completion
age187. audit_v945_current_reptile_after_inflation_checked stores that proof;
audit_v946_current_reptile_after_inflation_units passes 25 methods.

## Historical defect discoveries (Cage normal sections now corrected above)

Johnny Cage's Down Down Forward Forward LP torso rip activates and completes
at age185 against BOTH true added IDs in BOTH physical slots in the unchanged
v901 build: audit_v913_cage_{kano,sonya}_p{1,2}_torso. Native lookup uses owned
main57, but its relocated full-body substitutions and remaining original Liu
body-section descriptors are visibly incompatible. Dedicated upper/lower-body
severing poses are required; the Reptile headless art does not solve this path.
Sonya's actual age40/100/150/180 screenshots show the wrong sections/costume.

Baraka's Back Back Back Back HP decapitation genuinely activates when Block
is held during the direction inputs and released for HP, keeping the native
distance gate satisfied. audit_v913_baraka_sonya_p2_scout completes at age174
and actually exercises all seven current head frames and all seven body poses.
Only this normal-costume Sonya P2 diagnostic has been exercised here. Head
rotation ordering/art fidelity, the other slots/costumes and broader acceptance
remain unproven. Do not treat this single scout as an all-finisher acceptance.

The initial v911/v912 failures were test-input failures (unreachable spacing,
wrong direction or holding a button only after the victim was already dizzy).
Their process exit0 is not a gameplay pass. The v922 verifier also falsely
rejected all four good runs by conflating the header's victim name with the
FIRST_LIVE actor-address field of the same name. Its failed report is retained;
v924 binds the header separately. No actual game failure was waived.

## Remaining full objective

Correct rolling-head artwork/order, other stock fatalities and character-state
consumers, natural alternate selection and other alternate death-art colors,
alternate costumes,
arena/state/cinematic/audio variants, genuine Kintaro/Shao Kahn/tower/continue/
ending runs, and final combined UI/shadow/move/human/CPU combat regressions.
Then update actual play CMD/release ZIP and clean obsolete build data.
Native table stability, normal Dead Pool inflation and Cage torso art, Cage's
controlled native alternate blood branch, and current normal Reptile grounding
are proved at those scopes; full art, all stock fatalities,
alternate-palette runtime and the full
port remain explicitly incomplete. Goal stays active.
