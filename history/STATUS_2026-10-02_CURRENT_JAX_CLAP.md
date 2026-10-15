# Jax head-clap position/floor repair; full natural-character goal incomplete

Current experimental candidate: diagnostic_v1028_native_jax_clap_grounding.
EXE SHA256: 563389383E109BCCB6DF53C72F4A059951868C3DBB2E0DBEBCEE8D07F0224136.
Payload SHA256: 56B3D09C3EF398DE8CEDF11832732D3F2AE517A592CACFFDFB3346BDD497C4B9.
Driver SHA256: 98F825FEABEB33141C103C86CB84D8B71EDAD5BF362EEFAA914BA3FD5D32E863.
Installed EXE, existing play CMDs, and release ZIP are not updated.
This is NOT a completed/release-ready port.

## Genuine defects identified before editing

The initial audit_v1018 inputs did not establish activation. The old observer
watched only the primary fatality. New physical-only observers1020/1021 watch
both original action-table entries and the real native pointer consumers.
The original ROM input handlers establish these commands:

- Kung Lao split: three Forward taps, LK; native gap96..128.
- Kung Lao hat: hold LP, Back Forward, release LP; native gap>=256.
- Jax clap: hold LP>=64 fields, three Forward taps, release LP; gap<=83.
- Jax arms: four Block taps, LP; native gap69..128.

audit_v1021 runs physically select Sonya and earn322 collision damage/two KOs.
Kung Lao split enters FF8C6040, then at native age77 reads ID18 from FF8CF110
as FF8CF550, an unrelated existing composite list. The renderer overruns the
player globals at that same field and the action never completes.
Jax arms enters FF8BE240. At age41 FF9F57B0 returns FF9F5B90 and FF8BEF70
returns executable FF83B7F0 instead of a packed position. Its renderer also
overruns player globals and the action never completes.
Matching physical stock-Liu reference runs complete these original actions:
Kung Lao split age179; Jax arms age147. No proxy is used: Liu is genuinely
selected only for original-game reference runs.
audit_v1022_native_split_arm_references decodes original Liu/Kitana split,
arm-body and detached-arm sequences and all five affected short tables.
These are references, NOT replacement artwork or accepted port mappings.
The hat scout activates the secondary action but does not establish a
successful hat kill; its completion branch/physical steering still need work.

## Implemented Jax primary table repair

Native FF8C7FF0 ends before the added IDs; their former reads were executable
Reptile instructions. The head clap could finish while sending fighters out
of view. Extend the actual table to unused ROM FB600; preserve all original
indexed bytes0..16; append independent true-ID rows17/18; relocate only the
original operand FF8C7B50. The native action, actor IDs, renderer, timing,
continuation, all prior graphics/palettes and payload bytes remain unchanged.

Added packed signed offsets: Kano(-96,+5), Sonya(-96,+4).
FF841F20 aligns the victim to Jax; FF842A40 then moves the VICTIM, not Jax.
Positive Y restores its own native stage-relative floor134/135 versus Jax139.
The first negative-Y candidate1024 and its four actual runs1025 are REJECTED:
it removed the teleport but left the victims floating. Its source/binary/raw
evidence are retained. Candidate1028 corrects the offset sign.

## Current evidence and exact acceptance scope

Four audit_v1029 cold real-input cases cover both true victims/physical slots.
The native FFF parser and actual final LP hold/release are observed; each earns
322 real collision damage/two KOs; original Jax action wraps at age188; each
reaches the continue screen by field5198 without body-cache overruns.
The complete guest ROM differs from the previous candidate ONLY by the table
relocation/two rows. All initialized owned artwork is byte-identical.
2256 actual owned body DMA passes show all seven collapse poses grounded on
the native raster floor. All28 actual pose pictures match the encoded pixels
at exact measured DMA coordinates; minimum match0.680294 (native blood/actor
occlusion). All48 actual scene-review frames were viewed by the main agent.
audit_v1036_jax_clap_grounding_checked passes these independent checks.

Four fresh audit_v1034 Baraka games on this SAME candidate pass the full
original1014 head/body/DMA/palette/floor/position verifier, allowing ONLY the
intended Jax data extension in the guest.4364 owned DMAs remain correct.
All504 actual PNGs are byte-identical to their previously manually reviewed
audit_v1004 baselines. audit_v1034_baraka_after_jax_clap_checked passes.
This is eight focused CURRENT physical cases, not every finisher/arena/UI.

audit_v1039_jax_clap_proof_units passes seven corruption/real rejected-build
checks: identity, row value, wrap timing, collision chain, body floating,
missing final LP hold, and the actual negative-offset candidate1024.
The earlier1030 verifier wrongly required ten hits despite genuine LP contacts
and uninterrupted holds across a native actor rebuild between rounds;1036
requires the complete observed two-life collision chain and continuous final
>=64-field hold through the last KO. Earlier rejected reports remain saved.
Unit1037 removed only one duplicate hold-log record, leaving physical hold
evidenced;1039 removes every record for that field. Gameplay was unchanged.

## Historical checkpoint preservation and next work

All2542 checkpoint1017 pins were revalidated before source edits. The ONE
intentionally changed canonical driver is retained exactly in1017/input_sources;
all other historical pins remain unchanged. Old manifests/status are not
rewritten. The new compiled sources are frozen alongside candidate1028.
Checkpoint1040 records that explicit source transition; do not demand the live
driver still have its obsolete pre-fix hash when validating historical builds.

Next: own split halves/arm-rip bodies/arms and extend their actual ID tables,
including other-half selection and remaining packed-position consumers, while
preserving original native grammar and states. No Liu proxy or skipped death.
Then finish other stock fatalities, natural alternate costumes, arena/audio/
cinematic variants, full tower/bosses/continues/endings, and the final combined
selection/portrait cleanup/ladder/names/floor-shadow/moves/human/CPU regression.
Cage/Kitana/Reptile current-build replays beyond the historical proofs remain
to be run after this source change. Finally update actual CMDs/ZIP and safely
remove obsolete builds. Full-port acceptance remains false; goal stays active.
