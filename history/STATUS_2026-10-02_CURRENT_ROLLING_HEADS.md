# Native rolling-head repair; complete natural-character goal still incomplete

Current experimental candidate: diagnostic_v1002_owned_rolling_head_order.
EXE SHA256: 885B1A50DB68F6806C8A3B32DA329CAA87CCAC7636ADDB3D0283D83850023D1D.
Payload SHA256: 56B3D09C3EF398DE8CEDF11832732D3F2AE517A592CACFFDFB3346BDD497C4B9.
Compiled driver remains DF26C6EADA53FF4D6A1AD48D37C4F2112310F8E1C643B0336999A854A40B0AA8.
The unchanged verified binary is reused: only private asset payload data changes.
The installed EXE, existing play CMDs and release ZIP have NOT been updated.
This is not a complete/release-ready port.

## Repair and original native reference

audit_v997_native_rolling_head_references decodes the actual seven MKII
descriptors and externally owned palette, not an assumed embedded palette.
The original order is clockwise0,90,135,180,225,270,315: there is no45 pose.
Kano's existing sprites can be reused with source order0,6,3,4,5,2,1.
Simple reversal incorrectly interchanged135/225; its v1000 encoded preview
was rejected BEFORE creating a candidate. Its payload/review remain preserved.

Sonya's existing cardinal rotations are reused. Three missing diagonals were
produced with the built-in image-generation skill; rejected intermediate
orientations, selected transparent source, references and all exact prompts
are retained in art_native_rolling_heads_v998. The selected image is
sonya-diagonals-135-225-315.png, SHA256
3ABABEDEA62905D75B161DC2D26A8424EEC19280B2A6FB9560D10C57B226E17E.
The final source and decoded native palette preview were manually reviewed.

tools/build_rolling_head_order_v1001.py reorders only the twelve rotating-head
descriptor cells, appends three uniformly scaled/palette-quantized/six-bit
Sonya sprites, and updates the bounded packed length49228->51056.
Both tested upright heads, all prior graphics pixels/body artwork, all native
main60/main61 pointer/control words, original timing, palettes, IDs and game
code remain byte-identical. No Liu proxy or timing override is introduced.
Only1879 payload bytes differ from v978. New sprites are scaled uniformly per
sprite to the tested upright head's opaque area; there is no stretching.

## Genuine normal Dead Pool Baraka runtime proof

audit_v1004_baraka_{kano,sonya}_p{1,2}_owned_rolling_head contains four cold
physical-input games on the exact current candidate. Each earns322 native
collision damage/two KOs, enters the original Back Back Back Back HP action,
completes at native age174, and reaches the continue screen by field5198.
Block is physically held during the four Back taps and released for HP.
There are no health, actor-ID, state, position, timer, RNG or ROM writes.

All seven own head rotations and all seven own headless collapse poses render
in every case:4364 actual owned DMA passes, including2182 grounded body passes.
Head first-pose ages are59/64/68/72/76/80/84 in victimP1 and one field later
in victimP2. Original body collapse dispatch is also retained. There are56
actual hardware palette dumps,56 first-pose PNGs and244 periodic PNGs.

tools/verify_rolling_heads_v1014.py independently reconstructs the complete
intended payload from immutable sources and selected transparent pixels.
It checks entire guest ROM equality except the twelve intended descriptors,
actual initialized packed graphics, real two-KO inputs/command-table parsing,
native ownership/true IDs/FIFO/DMA/dimensions/palette/physical-side flips,
unchanged choreography/ground/retirement/continue, no foreign artwork after
decapitation, and exact presented pixel location. All56 pose PNGs match the
encoded native chromatic pixels; minimum score0.84375 (native blood occlusion),
many1.0. DMA VRAM-to-PNG projection is checked, not inferred from a green build.
audit_v1014_owned_rolling_head_position_checked passes.

All64 scene-review images and28 actual head closeups were viewed in
audit_v1011_owned_rolling_head_visual_review. Acceptance is normal costumes,
both true characters/physical slots, Dead Pool, original Baraka action only.
The five test methods/34 fixture-and-corruption checks in
audit_v1015_rolling_head_corruption_units pass, rejecting bad identity, foreign
art, wrong timing/ownership/palette/position, blank actual PNGs and corrupted
native ROM/graphics/palette data. These tests do not modify source/evidence.

## Same-candidate established death-path regressions

Four Cage cases in audit_v1005, four Kitana cases in audit_v1006 and four
Reptile cases in audit_v1008 all use this SAME current EXE/payload.
tools/verify_rolling_head_regressions_v1013.py freshly revalidates authoritative
v978 scoped proofs, then requires equality of every genuine input/native
observation, initialized graphics/hardware palette dump and presented PNG.
All764 actual PNGs are byte-identical to their accepted current baselines:
372 Cage (including the winner's extra poses),268 Kitana and124 Reptile.
Entire current guest equality allows only intended rotating-head descriptors.
Native wrap ages185/276/187 and original continuation remain unchanged.
audit_v1013_current_death_paths_after_rolling_heads_checked passes.
This is16 normal physical cases total, not all-finisher/all-arena acceptance.

## Retained failed inputs/check assumptions

The initial four audit_v1003 runs used an unreachable gap34 while native
collision separation stopped near63. They earned two KOs but never activated
the command: exit0 is NOT a finisher pass. The historical successful Baraka
scout explicitly used gap64; audit_v1004 corrects that input, not the game.
All failed runs remain preserved. No actual gameplay failure was waived.

The v1007 proof wrongly counted comparisons from an earlier rejected command;
v1009 then assumed the same Back token/table half in both physical directions.
v1014 binds the four accepted comparisons to the actual original ROM BBBB
table half and token7/8 for the corresponding direction. Earlier rejected
reports are retained; native game/payload were unchanged for these repairs.

## Checkpoint and full remaining objective

Current scoped checkpoint: audit_v1017_owned_rolling_heads_checkpoint/checkpoint.json.
The preceding audit_v995 checkpoint and its source/status evidence are retained
unchanged; STATUS_2026-10-02_CURRENT_STOCK_FATALITY_PATHS.md describes that
historical v978 checkpoint, not the newer candidate.

Still required: other stock fatalities and character-state consumers; natural
alternate costume selection and other alternate death-art colors (including
these rolling heads); arena/state/cinematic/audio variants; genuine full
Kintaro/Shao Kahn/tower/continue/ending runs; final combined selection/portraits/
ladder/names/floor-shadow/move/human/CPU regressions. Then update actual play
CMDs/release ZIP and safely remove obsolete build data. Existing scoped checks
are not substitutes for this complete natural-character objective.
Full-port acceptance remains false; goal stays active.
